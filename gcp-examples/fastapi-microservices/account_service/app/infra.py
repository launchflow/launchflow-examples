import launchflow as lf

# Use the generic Postgres class that deploys to GCP, AWS, or Docker
postgres = lf.Postgres("account-service-db")


# Optionally use the cloud-specific classes for more control
# postgres = lf.gcp.CloudSQLPostgres("account-service-db")
# postgres = lf.aws.RDSPostgres("account-service-db")
