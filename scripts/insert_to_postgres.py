import psycopg2
import subprocess
import json
from datetime import datetime

# PostgreSQL connection details (should match your docker-compose values)
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "cloud_costs"
DB_USER = "clouduser"
DB_PASSWORD = "cloudpass"

# SQL query to fetch AWS costs from Steampipe
STEAMPIPE_QUERY = """
SELECT
  linked_account_id,
  service,
  usage_type,
  product_name,
  usage_quantity,
  unblended_cost,
  usage_start_date,
  usage_end_date
FROM
  aws_billing_monthly_report;
"""

# Function to run Steampipe query inside the container and return JSON results
def run_steampipe_query(query):
    try:
        # Run Steampipe inside Docker and output JSON
        result = subprocess.run(
            ["docker", "exec", "steampipe", "steampipe", "query", "--output", "json", query],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running Steampipe query:", e.stderr)
        return []

# Function to insert data into PostgreSQL
def insert_to_postgres(data):
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()

        for row in data:
            # Prepare insert query
            cur.execute("""
                INSERT INTO aws_costs (
                    linked_account_id,
                    service,
                    usage_type,
                    product_name,
                    usage_quantity,
                    unblended_cost,
                    usage_start_date,
                    usage_end_date,
                    inserted_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row.get("linked_account_id"),
                row.get("service"),
                row.get("usage_type"),
                row.get("product_name"),
                row.get("usage_quantity"),
                row.get("unblended_cost"),
                row.get("usage_start_date"),
                row.get("usage_end_date"),
                datetime.utcnow()
            ))

        conn.commit()
        print(f"Inserted {len(data)} rows into PostgreSQL.")

    except Exception as e:
        print("Database error:", e)
    finally:
        if conn:
            conn.close()

# Entry point of the script
if __name__ == "__main__":
    print("Running Steampipe AWS cost query...")
    aws_cost_data = run_steampipe_query(STEAMPIPE_QUERY)
    if aws_cost_data:
        print("Inserting data into PostgreSQL...")
        insert_to_postgres(aws_cost_data)
    else:
        print("No data received from Steampipe.")

