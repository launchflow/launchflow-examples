import sys

import launchflow as lf

# mysql = lf.aws.EC2MySQL("mysql-vm")
# mysql_rds = lf.aws.RDS(
#     "mysql-rds",
#     publicly_accessible=False,
#     engine_version=lf.aws.rds.RDSEngineVersion.MYSQL8_0,
# )


def lambda_handler(event, context):
    mysql.query(
        f"""
        INSERT INTO visitors.visits (ip_address, user_agent, path)
        VALUES (
            '{event['requestContext']['identity']['sourceIp']}',
            '{event['headers']['User-Agent']}',
            '{event["path"]}'
        );
        """
    )
    visitors = [
        f"{row[1]} visited {row[4]} at {str(row[2])} with user agent {row[3]}"
        for row in mysql.query("SELECT * FROM visitors.visits ORDER BY timestamp ASC;")
    ]
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/plain"},
        "body": "\n".join(visitors),
    }


# api = lf.aws.LambdaStaticService(
#     "tanke-lambda",
#     handler=lambda_handler,
#     requirements_txt_path="requirements.txt",
# )

if __name__ == "__main__":
    mysql.query("Select 1;")
    print("MySQL (VM) connection successful.")

    # to create the table, run `python visitor_history.py create`
    if len(sys.argv) > 1 and sys.argv[1] == "create":
        mysql.query("CREATE DATABASE IF NOT EXISTS visitors;")
        mysql.query(
            """
            CREATE TABLE IF NOT EXISTS visitors.visits (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ip_address VARCHAR(255),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_agent VARCHAR(255),
                path VARCHAR(255)
            );
            """
        )
        print("Table is ready.")

    # to drop the table, run `python visitor_history.py drop`
    if len(sys.argv) > 1 and sys.argv[1] == "drop":
        mysql.query("DROP TABLE visitors.visits;")
        print("Table dropped.")

    # to clear the table, run `python visitor_history.py clear`
    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        mysql.query("TRUNCATE TABLE visitors.visits;")
        print("Table cleared.")

    # to ssh into the database, run `python visitor_history.py ssh`
    if len(sys.argv) > 1 and sys.argv[1] == "ssh":
        mysql.ssh()
