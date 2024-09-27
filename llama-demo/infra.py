"""infra.py

This file is used to customize the infrastructure your application deploys to.

Create your cloud infrastructure with:
    lf create

Deploy your application with:
    lf deploy

"""

import launchflow as lf

if lf.environment == "lf-llama-gcp":
    llama_service = lf.gcp.ComputeEngineService(
        "launchflow-llama-service",
        dockerfile="Dockerfile.gcp",  # Path to your Dockerfile
        machine_type="e2-standard-4",
        build_directory="llama_server",
        disk_size_gb=50,
    )
    model_bucket = lf.gcp.GCSBucket("launchflow-llama-demo")
elif lf.environment == "lf-llama-aws":
    llama_service = lf.aws.ECSFargateService(
        "launchflow-llama-service",
        dockerfile="Dockerfile.aws",  # Path to your Dockerfile
        build_directory="llama_server",
        cpu=8192,  # 8 cpus are required for GPU support
        memory=16384,  # 16 GB of memory are required for GPU support
        # load_balancer=lf.aws.alb.InternalHTTP(),
    )
    serving_service = lf.aws.LambdaService(
        "launchflow-llama-serving-demo",
        handler="main.handler",
        build_ignore=[
            "llama_server",
            "Dockerfile.*",
            "requirements*",
            "launchflow.yaml",
        ],
        runtime=lf.aws.lambda_service.PythonRuntime(
            requirements_txt_path="requirements-aws.txt"
        ),
        timeout_seconds=900,
        env={"LLAMA_SERVER_ADDRESS": lf.Depends(llama_service).service_url},  # type: ignore
    )
    model_bucket = lf.aws.S3Bucket("launchflow-llama-demo")
else:
    raise ValueError(f"Unknown environment: {lf.environment}")
