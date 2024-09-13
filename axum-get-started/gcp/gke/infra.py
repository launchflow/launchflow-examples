"""infra.py

This file is used to customize the infrastructure your application deploys to.

Create your cloud infrastructure with:
    lf create

Deploy your application with:
    lf deploy

For more information, visit https://docs.launchflow.com/docs/user-guides/project-structure
"""

import launchflow as lf

# GKE Docs: https://docs.launchflow.com/reference/gcp-services/gke-service
cluster = lf.gcp.GKECluster("my-gke-cluster")
service = lf.gcp.GKEService(
    "my-gke-service",
    cluster=cluster,
    dockerfile="Dockerfile",  # Path to your Dockerfile
)
