import json
import sys

import launchflow as lf
import requests
from markdownify import markdownify as md

HTML = """
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Markdown Converter</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            .markdown-body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #f9f9f9;
                padding: 20px;
                border-radius: 5px;
            }
            .markdown-body h1, .markdown-body h2, .markdown-body h3 {
                margin-top: 1em;
                margin-bottom: 0.5em;
                font-weight: bold;
            }
            .markdown-body p {
                margin-bottom: 1em;
            }
            .markdown-body a {
                color: #3b82f6;
                text-decoration: none;
            }
            .markdown-body a:hover {
                text-decoration: underline;
            }
            .markdown-body ul, .markdown-body ol {
                padding-left: 1.5em;
            }
        </style>
    </head>
    <body class="bg-gray-100 text-gray-900">
        <div class="min-h-screen flex items-center justify-center">
            <div class="bg-white p-8 rounded shadow-md w-full max-w-5xl flex">
                <!-- Sidebar for History -->
                <div class="w-1/3 pr-6">
                    <h2 class="text-xl font-semibold mb-4">History</h2>
                    <button id="historyButton" class="w-full py-2 px-4 mb-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Load History</button>
                    <ul id="historyList" class="list-disc list-inside text-gray-700"></ul>
                </div>
                <!-- Markdown Converter Section -->
                <div class="w-2/3">
                    <h1 class="text-2xl font-semibold mb-6 text-center">Markdown Converter</h1>
                    <form id="markdownForm" class="space-y-4">
                        <div>
                            <label for="url" class="block text-sm font-medium text-gray-700">Enter website URL:</label>
                            <input type="text" id="url" name="url" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                        </div>
                        <div class="flex space-x-4 justify-center">
                            <button type="submit" class="w-full py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Convert to Markdown</button>
                            <button type="button" id="clearButton" class="w-full py-2 px-4 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Clear</button>
                        </div>
                    </form>
                    <div id="result" class="markdown-body mt-6"></div>
                </div>
            </div>
        </div>
        <script>
            document.getElementById('markdownForm').onsubmit = function(event) {
                event.preventDefault();
                const url = document.getElementById('url').value;
                fetch(`?url=${encodeURIComponent(url)}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (data.markdown) {
                            document.getElementById('result').innerHTML = data.markdown;
                        } else {
                            document.getElementById('result').innerText = "Error: Invalid response format";
                        }
                    })
                    .catch(error => {
                        document.getElementById('result').innerText = `Error: ${error.message}`;
                    });
            };

            document.getElementById('clearButton').onclick = function() {
                document.getElementById('url').value = '';
                document.getElementById('result').innerText = '';
            };

            document.getElementById('historyButton').onclick = function() {
                fetch('/history')
                    .then(response => response.json())
                    .then(data => {
                        const historyList = document.getElementById('historyList');
                        historyList.innerHTML = '';
                        if (Array.isArray(data.urls) && data.urls.length > 0) {
                            data.urls.forEach(url => {
                                const listItem = document.createElement('li');
                                listItem.textContent = url;
                                historyList.appendChild(listItem);
                            });
                        } else {
                            historyList.innerText = 'No history found.';
                        }
                    })
                    .catch(error => {
                        document.getElementById('historyList').innerText = `Error: ${error.message}`;
                    });
            };
        </script>
    </body>
</html>
"""

# mysql = lf.aws.EC2MySQL("mysql-vm")
# mysql_rds = lf.aws.RDS(
#     "mysql-rds",
#     publicly_accessible=False,
#     engine_version=lf.aws.rds.RDSEngineVersion.MYSQL8_0,
# )


def get_markdown(url: str) -> str:
    response = requests.get(url)
    if response.status_code != 200:
        return (
            f"Error: could not fetch markdown from {url}. Code: {response.status_code}"
        )
    return md(response.text)


def lambda_handler(event, context):
    # Serve the history endpoint
    if event.get("path", "/") == "/history" and event.get("httpMethod", "GET") == "GET":
        urls = mysql.query("SELECT url FROM markdown.conversions;")
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"urls": [url for url, in urls]}),
        }

    query_params = event.get("queryStringParameters", {}) or {}
    url = query_params.get("url")

    # Return the markdown content if a URL is provided
    if url:
        markdown_content = get_markdown(url)
        mysql.query(
            f"INSERT INTO markdown.conversions (url, markdown) VALUES ('{url}', '{markdown_content}');"
        )
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"markdown": markdown_content}),
        }

    # Serve the HTML page on the root path
    if event.get("path", "/") == "/" and event.get("httpMethod", "GET") == "GET":
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": HTML,
        }

    # Return a 404 error for all other paths
    return {
        "statusCode": 404,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"error": "Not found"}),
    }


# api_gateway = lf.aws.APIGateway("tanke-api-gateway")


if __name__ == "__main__":
    mysql.query("Select 1;")
    print("MySQL connection successful.")

    mysql.query("CREATE DATABASE IF NOT EXISTS markdown;")
    mysql.query(
        """
        CREATE TABLE IF NOT EXISTS markdown.conversions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            url VARCHAR(255) NOT NULL,
            markdown TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    # to clear the table, run `python convert_to_markdown.py clear`
    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        mysql.query("TRUNCATE TABLE markdown.conversions;")
        print("Table cleared.")

    # to ssh into the database, run `python convert_to_markdown.py ssh`
    if len(sys.argv) > 1 and sys.argv[1] == "ssh":
        mysql.ssh()
