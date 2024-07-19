import launchflow as lf
from fastapi import FastAPI

# Deploy and connect to a GCS bucket in the current environment
bucket = lf.gcp.GCSBucket(f"my-bucket-{lf.environment}")
other_bucket = lf.gcp.GCSBucket(f"my-other-bucket-{lf.environment}")
topic = lf.gcp.PubsubTopic(f"my-topic-{lf.environment}")
subscription = lf.gcp.PubsubSubscription(f"my-subscription-{lf.environment}", topic)
# Build and deploy a Cloud Run service to the current environment
service = lf.gcp.CloudRun(f"my-service-{lf.environment}")

# Works with any Python framework - FastAPI, Django, Flask, etc.
app = FastAPI()


@app.get("/")
def bucket_endpoint():
    # Auto configured client libraries for all Resources
    bucket.upload_from_string(f"Hello from {lf.environment}", "hello.txt")
    return bucket.download_file("hello.txt").decode("utf-8")


if __name__ == "__main__":
    print(f"Outputs: {bucket.outputs()}")
    print(f"Outputs: {other_bucket.outputs()}")
    print(f"Outputs: {topic.outputs()}")
    print(f"Outputs: {subscription.outputs()}")
