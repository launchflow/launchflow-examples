import launchflow as lf

from fasthtml import *

# Deploy to this FastHTML app to ECS Fargate by running `lf deploy`
cloud_run = lf.aws.ECSFargate("fasthtml-service")


app = FastHTML()


@app.get("/")
def home():
    if lf.is_deployment():
        return f"<h1>Hello from {lf.environment}</h1>"
    return "<h1>Hello from localhost</h1>"
