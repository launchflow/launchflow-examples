import launchflow as lf
from fastapi import FastAPI

bucket = lf.gcp.GCSBucket(f"my-get-started-bucket-{lf.environment}")

app = FastAPI()


@app.get("/")
def index():
    bucket.upload_from_string(f"Hello from {lf.environment}", "hello_world.txt")
    contents = bucket.download_file("hello_world.txt")
    return contents


cloud_run = lf.gcp.CloudRun("my-cloud-run", region="us-central1")
