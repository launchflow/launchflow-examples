# Simple CRUD API on FastAPI

This is a simple crud API that allows users to be created and upload a profile picture. It uses a Postgres SQL database hosted on GCP to hold user information, and a GCS storage bucket to hold the profile pictures.

## Running the application

### Install the dependencies

```bash
pip install -r requirements.txt
```

### Login

To get started run login to LaunchFlow:

```bash
launchflow login
```

### Connect GCP

If you haven't connected your LaunchFlow account to GCP, you can do so by running:

```bash
launchflow cloud connect --provider=GCP
```

### Create Resources

NOTE: Before running make sure you update the bucket name in `infra.py` to be unique.

To create the resources needed to run the application, run:

```bash
launchflow create
```

This will prompt you to create a LaunchFlow project and environment to hold the resources. It takes GCP several minutes to provision your Cloud SQL database.

### Run the application

```
uvicorn main:app
```

Once running you can visit http://localhost:8000/docs to see the API documentation, and send requests.
