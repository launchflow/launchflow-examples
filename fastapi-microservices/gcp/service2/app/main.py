import launchflow as lf
from fastapi import FastAPI

app = FastAPI()

# NOTE: the build directory is relative to the launchflow.yaml file
api = lf.gcp.CloudRun("fastapi-service2-service", build_directory="./service2")


@app.get("/")
async def read_root():
    return f"Hello from Service 2, running in {lf.environment}"


@app.get("/service_info")
async def service_info():
    if lf.is_deployment():
        # Return the Cloud Run service info for Service 2's deployment
        return {"Service 2 info": api.outputs().to_dict()}
    return {"message": "Service 2 running locally"}
