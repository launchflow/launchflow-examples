import launchflow as lf
from fastapi import FastAPI

# TODO(developer): Rename the bucket (needs to be globally unique)
bucket = lf.aws.S3Bucket(name=f"my-get-started-bucket-{lf.environment}")

app = FastAPI()


@app.get("/")
def index():
    # Upload a file to the bucket to test the connection
    bucket.upload_from_string(f"Hello from {lf.environment}", "hello_world.txt")
    # Download the file from the bucket and return its contents
    contents = bucket.download_file("hello_world.txt")
    return contents


# Build / Deploy this app to ECS Fargate
ecs_fargate = lf.aws.ECSFargate("my-ecs-fargate")
