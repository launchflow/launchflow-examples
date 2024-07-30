import launchflow as lf
from fastapi import FastAPI

bucket = lf.aws.S3Bucket(f"my-get-started-bucket-{lf.environment}")

app = FastAPI()


@app.get("/")
def index():
    bucket.upload_from_string(f"Hello from {lf.environment}", "hello_world.txt")
    contents = bucket.download_file("hello_world.txt")
    return contents


ecs_fargate = lf.aws.ECSFargate("my-ecs-fargate")
