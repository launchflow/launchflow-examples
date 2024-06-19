import launchflow as lf

# Docs: https://docs.launchflow.com/reference/gcp-resources/gcs-bucket
bucket = lf.gcp.GCSBucket(
    f"launchflow-bucket-for-quickstart-{lf.environment}", force_destroy=True
)
ar = lf.gcp.ArtifactRegistryRepository("launchflow-quickstart", "DOCKER")
service_container = lf.gcp.cloud_run_container.CloudRunServiceContainer(
    name="my-service-container"
)
custom_domain_mapping = lf.gcp.custom_domain_mapping.CustomDomainMapping(
    "domain-mapping", domain="caleb.test.launchflow.com", cloud_run=service_container
)
# service = lf.gcp.CloudRun("launchflow-quickstart", publicly_accessible=False)
