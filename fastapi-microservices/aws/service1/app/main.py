import launchflow as lf
from fastapi import FastAPI

app = FastAPI()

# NOTE: the build directory is relative to the launchflow.yaml file
api = lf.aws.ECSFargate("fastapi-service1-service", build_directory="./service1")


@app.get("/")
async def read_root():
    return f"Hello from Service 1, running in {lf.environment}"


@app.get("/service_info")
async def service_info():
    if lf.is_deployment():
        # Return the Cloud Run service info for Service 1's deployment
        return {"Service 1 info": api.outputs().to_dict()}
    return {"message": "Service 1 running locally"}
