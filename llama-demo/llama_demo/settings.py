import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    context_window: int = int(os.environ.get("CONTEXT_WINDOW", 5000))
    llama_server_address: str = os.environ.get(
        "LLAMA_SERVER_ADDRESS",
        "http://launchflow-llama-service-l-79dfc-799820891.us-east-1.elb.amazonaws.com",
    )
    streaming: bool = os.environ.get("LAUNCHFLOW_ENVIRONMENT") == "lf-llama-gcp"


settings = Settings()
