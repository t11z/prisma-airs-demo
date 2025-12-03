"""Prisma AIRS scanning hooks used by Prompt Flow nodes."""

import os
import logging

import aisecurity
from aisecurity import AISecurity, Scanner, AiProfile

# Configure lightweight logging so flow operators can trace scan behavior.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Prisma AIRS client using the configured API key.
API_KEY = os.getenv("PRISMA_AIRS_API_KEY")
ais_client = AISecurity(api_key=API_KEY) if API_KEY else None


def _run_scan(direction, content, user_id=None):
    """Shared helper to invoke Prisma AIRS scanning with safe fallbacks."""

    # Base payload returned even when scanning is skipped or fails.
    response = {
        "direction": direction,
        "original_content": content,
        "scanned_content": content,
        "status": "skipped" if not API_KEY else "pending",
        "user_id": user_id,
    }

    if not API_KEY:
        # Without credentials we cannot reach Prisma AIRS; keep content unchanged.
        response["reason"] = "missing_api_key"
        return response

    try:
        # AiProfile can hold policy configuration; default profile keeps this example minimal.
        profile = AiProfile(name="default")

        # Scanner.sync_scan performs the synchronous moderation/validation call.
        scanner = Scanner(ai_security=ais_client, ai_profile=profile)
        scan_result = scanner.sync_scan(
            content=content,
            metadata={"direction": direction, "user_id": user_id},
        )

        response.update(
            {
                "status": "scanned",
                "scanned_content": scan_result.get("content", content) if isinstance(scan_result, dict) else content,
                "result": scan_result,
            }
        )
    except Exception as exc:  # pragma: no cover - defensive fallback for runtime errors
        # Log the failure and return a structured error response instead of raising.
        logger.warning("Prisma AIRS %s scan failed: %s", direction, exc)
        response.update({"status": "error", "error": str(exc)})

    return response


def scan_input(content, user_id=None):
    """Scan user-provided content before invoking the model."""

    return _run_scan("input", content, user_id)


def scan_output(content, user_id=None):
    """Scan model-generated content before returning it to the user."""

    return _run_scan("output", content, user_id)
