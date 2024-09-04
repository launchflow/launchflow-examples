import launchflow as lf


def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/plain"},
        "body": f"Hello from {lf.environment}!",
    }


# Create / Deploy the Lambda function. Includes dependencies in requirements.txt
api = lf.aws.LambdaStaticService(
    "basic-lambda",
    handler=lambda_handler,
    requirements_txt_path="requirements.txt",
)
