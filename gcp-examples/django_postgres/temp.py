import google.auth
import psycopg2
from google.auth import impersonated_credentials
from google.auth.transport.requests import Request

# initialize ADC creds
source_credentials, _ = google.auth.default(
    scopes=["https://www.googleapis.com/auth/sqlservice.login"]
)


target_credentials = impersonated_credentials.Credentials(
    source_credentials=source_credentials,
    target_principal="**********@**********.iam.gserviceaccount.com",
    delegates=[],
    lifetime=3600,
    target_scopes=["https://www.googleapis.com/auth/sqlservice.login"],
)
refresh_request = Request()
target_credentials.refresh(refresh_request)


# Cloud SQL Public Instance IP address
instance_ip = "**.**.**.***"

# interact with Cloud SQL database using psycopg2 connection
with psycopg2.connect(
    dbname="postgres",
    user="**********@**********.iam",
    password=str(target_credentials.token),
    host=instance_ip,
    port="5432",
) as con:
    with con.cursor() as cur:
        cur.execute("SELECT * FROM test.table")
        rows = cur.fetchall()
        print(rows)
