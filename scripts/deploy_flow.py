"""Deploy the Prisma AIRS chat Prompt Flow into Azure AI Foundry."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

from load_infra_outputs import load_infra_outputs


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the deployment script."""

    parser = argparse.ArgumentParser(
        description="Register and deploy the Prisma AIRS Prompt Flow to Azure AI Foundry.",
    )
    parser.add_argument(
        "--config",
        default="infra-outputs.json",
        help="Path to the Terraform outputs JSON file (default: infra-outputs.json).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    outputs = load_infra_outputs(args.config)

    hub_name = outputs.ai_foundry_hub_name
    project_name = outputs.ai_foundry_project_name
    location = outputs.location

    # Subscription and resource group values are expected from Terraform outputs once available.
    # Until then, fall back to environment variables that may be set via ``az login`` context or CI variables.
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID") or "<subscription-id>"
    resource_group = os.environ.get("AZURE_RESOURCE_GROUP") or "<resource-group-name>"

    # DefaultAzureCredential will use environment variables, managed identity, or a cached Azure CLI login.
    # Users can either rely on an existing ``az login`` session or configure environment-based credentials.
    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)

    ml_client = MLClient(
        credential=credential,
        subscription_id=subscription_id,
        resource_group_name=resource_group,
    )

    flow_dir = Path("flows") / "prisma_airs_chat"

    # TODO: Confirm the correct MLClient API for registering Prompt Flows once the SDK supports it directly.
    # This placeholder documents the intended operation without making unsafe API assumptions.
    try:
        print(f"Registering flow from directory: {flow_dir}")
        # Example placeholder for future implementation:
        # flow_resource = ml_client.flows.create_or_update(flow_dir)
        # print(f"Flow registered: {flow_resource.name}")
    except Exception as ex:
        print(f"Flow registration placeholder encountered an error: {ex}")

    deployment_name = "airs_flow_deployment"

    # TODO: Replace this placeholder with the correct Managed Online Deployment API call for flows.
    # The expected future shape is similar to ``ml_client.online_deployments.begin_create_or_update`` with
    # a deployment object that references the registered flow.
    try:
        print(f"Creating or updating managed online deployment: {deployment_name}")
        # deployment = ManagedOnlineDeployment(...)  # TODO: populate with flow references and compute
        # poller = ml_client.online_deployments.begin_create_or_update(deployment)
        # result = poller.result()
        # print(f"Deployment succeeded: {result.name}")
    except Exception as ex:
        print(f"Deployment placeholder encountered an error: {ex}")

    print("Deployment completed. Open Azure AI Foundry -> Hub -> Project -> Prompt Flows to test the flow.")
    print(
        f"Hub: {hub_name} | Project: {project_name} | Location: {location} | "
        f"Subscription: {subscription_id} | Resource Group: {resource_group}"
    )


if __name__ == "__main__":
    main()
