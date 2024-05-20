import launchflow as lf
from fastapi import Depends, FastAPI
from mypy_boto3_s3.service_resource import Bucket

s3 = lf.aws.S3Bucket("launchflow-example-bucket")


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/bucket_example")
async def example_bucket_usage(
    file_name: str,
    file_contents: str,
    s3_client: Bucket = Depends(s3.bucket),
) -> str:
    s3_client.put_object(Key=file_name, Body=file_contents)
    return "OK"
