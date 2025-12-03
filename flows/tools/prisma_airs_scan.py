"""Prisma AIRS scanning hooks used by Prompt Flow nodes.

This module integrates the Prisma AIRS Python SDK as inline guards around
LLM input and output. It is designed to be called from Azure AI Prompt Flow
Python nodes.

Environment variables:
    PANW_AI_SEC_API_KEY      or PRISMA_AIRS_API_KEY  - Prisma AIRS API key
    PANW_AI_SEC_API_TOKEN    (optional alternative)
    PANW_AI_SEC_PROFILE_NAME - AI Security Profile name (default: "Secure-AI")
    PANW_AI_SEC_API_ENDPOINT - Optional custom API endpoint (EU/US, etc.)
"""

import logging
import os

import aisecurity
from aisecurity.generated_openapi_client.models.ai_profile import AiProfile
from aisecurity.scan.inline.scanner import Scanner
from aisecurity.scan.models.content import Content

# Lightweight logging so operators can see scan behavior in logs.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Support both the official PANW_* env var and the earlier PRISMA_AIRS_* naming.
_API_KEY = os.getenv("PRISMA_AIRS_API_KEY") or os.getenv("PANW_AI_SEC_API_KEY")
_API_TOKEN = os.getenv("PANW_AI_SEC_API_TOKEN")
_PROFILE_NAME = os.getenv("PANW_AI_SEC_PROFILE_NAME", "Secure-AI")
_API_ENDPOINT = os.getenv("PANW_AI_SEC_API_ENDPOINT")

_SCANNER = None
_AI_PROFILE = None


def _init_sdk():
    """Initialize the Prisma AIRS SDK exactly once.

    Uses the official aisecurity.init(...) pattern from the Python SDK docs.
    Prefers API token over API key if both are configured.
    """

    global _SCANNER, _AI_PROFILE  # noqa: PLW0603

    if _SCANNER is not None and _AI_PROFILE is not None:
        return

    if not (_API_KEY or _API_TOKEN):
        logger.warning(
            "No Prisma AIRS credentials found "
            "(PANW_AI_SEC_API_KEY / PANW_AI_SEC_API_TOKEN / PRISMA_AIRS_API_KEY). "
            "Scanning will be skipped (fail-open).",
        )
        return

    init_kwargs = {}
    if _API_TOKEN:
        init_kwargs["api_token"] = _API_TOKEN
    elif _API_KEY:
        init_kwargs["api_key"] = _API_KEY

    if _API_ENDPOINT:
        init_kwargs["api_endpoint"] = _API_ENDPOINT

    try:
        aisecurity.init(**init_kwargs)
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to initialize Prisma AIRS SDK: %s", exc)
        return

    try:
        _AI_PROFILE = AiProfile(profile_name=_PROFILE_NAME)
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to construct AiProfile with name '%s': %s", _PROFILE_NAME, exc)
        return

    try:
        _SCANNER = Scanner()
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to construct Prisma AIRS Scanner: %s", exc)
        _SCANNER = None


def _run_scan(direction, content, user_id=None):
    """Shared helper to invoke Prisma AIRS scanning with safe, structured fallbacks.

    Returns a dict with at least:
        direction: "input" | "output"
        original_content: str
        scanned_content: str (may be redacted by policy, or unchanged)
        status: "skipped" | "pending" | "scanned" | "error"
        user_id: optional user identifier
        reason: optional high-level reason ("missing_credentials", "scan_error", ...)
        result: raw Prisma AIRS SDK response (to_dict() if available)
    """

    response = {
        "direction": direction,
        "original_content": content,
        "scanned_content": content,
        "status": "pending",
        "user_id": user_id,
        "reason": None,
        "result": None,
    }

    # Initialize SDK / Scanner lazily.
    _init_sdk()

    if _SCANNER is None or _AI_PROFILE is None:
        # Fail-open behavior when Prisma AIRS cannot be used.
        response["status"] = "skipped"
        response["reason"] = "missing_credentials_or_init_failed"
        return response

    # Map direction to the Content model expected by the SDK.
    # For input scans we primarily set "prompt", for output scans "response".
    if direction == "input":
        content_obj = Content(prompt=content, response=None)
    elif direction == "output":
        content_obj = Content(prompt=None, response=content)
    else:
        # Fallback: treat unknown direction as prompt.
        content_obj = Content(prompt=content, response=None)

    metadata = {
        "direction": direction,
        "app_user": user_id or "anonymous",
    }

    try:
        scan_resp = _SCANNER.sync_scan(
            ai_profile=_AI_PROFILE,
            content=content_obj,
            metadata=metadata,
        )

        # Prisma AIRS SDK returns a typed object; convert it to dict when possible.
        if hasattr(scan_resp, "to_dict"):
            result_dict = scan_resp.to_dict()
        elif isinstance(scan_resp, dict):
            result_dict = scan_resp
        else:
            result_dict = {"raw": str(scan_resp)}

        response["result"] = result_dict
        response["status"] = "scanned"

        # Heuristik: versuche redaktierte/angepasste Inhalte zu übernehmen.
        # Die exakte Struktur hängt von deinem Profil / aktivierten Detections ab.
        # Häufige Varianten:
        #   - result["sanitized_content"]
        #   - result["content"]["prompt"] / ["content"]["response"]
        sanitized = None

        sanitized = result_dict.get("sanitized_content") if isinstance(result_dict, dict) else None

        if not sanitized and isinstance(result_dict, dict):
            # Versuche verschachtelte Struktur
            content_block = result_dict.get("content") or {}
            if isinstance(content_block, dict):
                if direction == "input":
                    sanitized = content_block.get("prompt")
                elif direction == "output":
                    sanitized = content_block.get("response")

        # Fallback: wenn nichts gefunden, nutze Originalinhalt.
        response["scanned_content"] = sanitized or content

    except Exception as exc:  # noqa: BLE001
        # Defensive fallback: loggen und Fail-Open.
        logger.warning("Prisma AIRS %s scan failed: %s", direction, exc)
        response["status"] = "error"
        response["reason"] = "scan_error"
        response["result"] = None

    return response


def scan_input(content, user_id=None):
    """Scan user-provided content before invoking the model.

    Designed to be called from a Prompt Flow Python node for input filtering.
    """

    return _run_scan("input", content, user_id)


def scan_output(content, user_id=None):
    """Scan model-generated content before returning it to the user.

    Designed to be called from a Prompt Flow Python node for output filtering.
    """

    return _run_scan("output", content, user_id)
