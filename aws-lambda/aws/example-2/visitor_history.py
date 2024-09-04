import launchflow as lf

mysql_rds = lf.aws.RDS(
    "mysql-rds-private",
    publicly_accessible=False,  # Only accessible from within the VPC
    engine_version=lf.aws.rds.RDSEngineVersion.MYSQL8_0,
)

# Create the table at startup if it doesn't exist.
if lf.is_deployment():
    mysql_rds.query("CREATE DATABASE IF NOT EXISTS visitors;")
    mysql_rds.query(
        """
        CREATE TABLE IF NOT EXISTS visitors.visits (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ip_address VARCHAR(255),
            path VARCHAR(255),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_agent VARCHAR(255)
        );
        """
    )


def lambda_handler(event, context):
    # Insert the visitor information into the database
    mysql_rds.query(
        f"""
        INSERT INTO visitors.visits (ip_address, path, user_agent)
        VALUES (
            '{event['requestContext']['identity']['sourceIp']}',
            '{event["path"]}',
            '{event['headers']['User-Agent']}'
        );
        """
    )
    # Retrieve all visitor information from the database
    visitors = [
        f"{row[1]} visited {row[2]} at {str(row[3])} with user agent {row[4]}"
        for row in mysql_rds.query(
            "SELECT * FROM visitors.visits ORDER BY timestamp ASC;"
        )
    ]
    # Return the visitor information as a plain text response
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/plain"},
        "body": "\n".join(visitors),
    }


# Create / Deploy the Lambda function. Includes dependencies in requirements.txt
api = lf.aws.LambdaStaticService(
    "visitor-history-lambda",
    handler=lambda_handler,
    requirements_txt_path="requirements.txt",
    timeout=30,
)
