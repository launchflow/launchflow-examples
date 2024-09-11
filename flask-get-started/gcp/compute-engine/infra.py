"""infra.py

This file is used to customize the infrastructure your application deploys to.

Create your cloud infrastructure with:
    lf create

Deploy your application with:
    lf deploy

For more information, visit https://docs.launchflow.com/docs/user-guides/project-structure
"""

import launchflow as lf

# Compute Engine Docs: https://docs.launchflow.com/reference/gcp-services/compute-engine-service
service = lf.gcp.ComputeEngineService(
    "my-compute-engine-service",
    dockerfile="Dockerfile",  # Path to your Dockerfile
)
