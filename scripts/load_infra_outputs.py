"""Utilities to load and validate Terraform outputs for deployment scripts.

This module bridges Terraform output (via ``terraform output -json``) and
Python-based deployment helpers. It provides a strongly-typed container for the
outputs alongside a loader that validates presence of required values.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class InfraOutputs:
    """Typed representation of the infrastructure outputs produced by Terraform."""

    ai_foundry_hub_name: str
    ai_foundry_project_name: str
    location: str
    ai_services_name: str
    ai_services_endpoint: Optional[str]
    storage_account_name: str
    search_service_name: Optional[str]


def _extract_value(outputs: Dict[str, Any], key: str) -> Any:
    """Extract the ``value`` field for ``key`` from Terraform JSON output."""

    if key not in outputs:
        raise RuntimeError(f"Missing required output: {key}")

    value_container = outputs[key]
    if not isinstance(value_container, dict) or "value" not in value_container:
        raise RuntimeError(f"Output '{key}' is malformed; expected an object with a 'value' field.")

    return value_container.get("value")


def load_infra_outputs(path: str) -> InfraOutputs:
    """Load Terraform outputs from ``path`` and return a typed ``InfraOutputs`` instance."""

    file_path = Path(path)
    if not file_path.exists():
        raise RuntimeError(f"Terraform outputs file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        outputs: Dict[str, Any] = json.load(f)

    ai_foundry_hub_name = _extract_value(outputs, "ai_foundry_hub_name")
    ai_foundry_project_name = _extract_value(outputs, "ai_foundry_project_name")
    location = _extract_value(outputs, "location")
    ai_services_name = _extract_value(outputs, "ai_services_name")
    storage_account_name = _extract_value(outputs, "storage_account_name")

    # Optional outputs: missing keys will return ``None`` instead of failing.
    ai_services_endpoint = outputs.get("ai_services_endpoint", {}).get("value")
    search_service_name = outputs.get("search_service_name", {}).get("value")

    return InfraOutputs(
        ai_foundry_hub_name=ai_foundry_hub_name,
        ai_foundry_project_name=ai_foundry_project_name,
        location=location,
        ai_services_name=ai_services_name,
        ai_services_endpoint=ai_services_endpoint,
        storage_account_name=storage_account_name,
        search_service_name=search_service_name,
    )


def _parse_args() -> argparse.Namespace:
    """Parse CLI arguments for the module."""

    parser = argparse.ArgumentParser(
        description=(
            "Load Terraform outputs (as JSON) and print a short summary."
        )
    )
    parser.add_argument(
        "--config",
        default="infra-outputs.json",
        help="Path to the JSON file produced by 'terraform output -json'.",
    )
    return parser.parse_args()


def _format_summary(outputs: InfraOutputs) -> str:
    """Create a concise human-readable summary of the key outputs."""

    parts = [
        f"Hub: {outputs.ai_foundry_hub_name}",
        f"Project: {outputs.ai_foundry_project_name}",
        f"Location: {outputs.location}",
        f"AI Services: {outputs.ai_services_name}",
        f"Storage Account: {outputs.storage_account_name}",
    ]

    if outputs.ai_services_endpoint:
        parts.append(f"AI Services Endpoint: {outputs.ai_services_endpoint}")
    if outputs.search_service_name:
        parts.append(f"Search Service: {outputs.search_service_name}")

    return " | ".join(parts)


if __name__ == "__main__":
    args = _parse_args()
    infra_outputs = load_infra_outputs(args.config)
    print(_format_summary(infra_outputs))
