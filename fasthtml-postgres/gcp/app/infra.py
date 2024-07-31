import launchflow as lf

postgres = lf.gcp.CloudSQLPostgres("fasthtml-example")

cloud_run = lf.gcp.CloudRun("fasthtml-service")
