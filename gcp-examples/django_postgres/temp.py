import google.auth
import psycopg2
from google.auth.transport.requests import Request

# initialize ADC creds
creds, _ = google.auth.default(
    scopes=["https://www.googleapis.com/auth/sqlservice.login"]
)

# refresh credentials if expired (manage this code in your application)
request = Request()
creds.refresh(request)


# Cloud SQL Instance IP address
instance_ip = "34.71.50.100"

# interact with Cloud SQL database using psycopg2 connection
with psycopg2.connect(
    f"dbname=launchflow-sample-db-db user=launchflow@gcp-examples-dev-9472.iam password={str(creds.token)} host={instance_ip} sslmode=require sslrootcert=server-ca.pem sslcert=client-cert.pem sslkey=client-key.pem"
) as con:
    with con.cursor() as cur:
        cur.execute("SELECT * FROM test.table")
        rows = cur.fetchall()
        print(rows)
