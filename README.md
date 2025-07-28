# Cloud-Cost-Dashboard
# Cloud Cost Monitoring with Steampipe, PostgreSQL, and Grafana

## 📌 Overview
This project provides a free and open-source way to monitor AWS cloud costs (GCP and Azure coming soon) using:

- **Steampipe**: For querying cloud APIs using SQL.
- **PostgreSQL**: For storing query results.
- **Grafana**: For visualizing costs in a dashboard.

You can easily extend this to monitor GCP and Azure costs as well.

---

## ✅ Features
- Unified dashboard for all cloud costs.
- No vendor lock-in.
- No cost (uses free-tier APIs and open-source tools).
- Easily customizable with SQL.

---

## 🔧 Prerequisites
Before starting, ensure you have the following tools installed and configured:

### 1. AWS Credentials
You need an AWS account with programmatic access set up. Store credentials as environment variables:
```bash
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
export AWS_DEFAULT_REGION=us-east-1  # or your preferred region
```
Alternatively, configure them using the AWS CLI:
```bash
aws configure
```

### 2. Installed Tools
You must have the following installed:

- [Steampipe](https://steampipe.io/downloads): Query cloud services using SQL.
- [PostgreSQL](https://www.postgresql.org/download/): Used for storing cost data.
- [Grafana](https://grafana.com/grafana/download): Dashboard visualization.
- [Python 3](https://www.python.org/downloads/) (for automation script).

Optional (but recommended):
- Docker & Docker Compose (to simplify deployment).

---

## 📁 Repository Structure
```
cloud-cost-dashboard/
├── dashboards/
│   └── aws_cloud_cost_dashboard.json     # Grafana dashboard JSON
├── queries/
│   └── aws_cost_queries.sql              # SQL queries for AWS billing
├── scripts/
│   └── insert_to_postgres.py             # Python script to insert data
├── .env                                  # Environment variables
└── README.md                             # This file
```

---

## 🛠️ Setup Steps

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/cloud-cost-dashboard.git
cd cloud-cost-dashboard
```

### Step 2: Configure AWS Credentials
Ensure your environment is configured with AWS credentials (see Prerequisites).

### Step 3: Install Steampipe & AWS Plugin
```bash
brew install steampipe  # macOS
steampipe plugin install aws
```
Test a query:
```bash
steampipe query
> select account_id, service, sum(unblended_cost) as cost from aws_billing_usage_by_service where usage_start_date >= current_date - interval '30 days' group by account_id, service;
```

### Step 4: Set Up PostgreSQL
Install PostgreSQL and create a new database:
```bash
createdb cloud_costs
```
Set credentials in `.env` file (based on `.env.example`).

### Step 5: Run the Python Script
Install dependencies and run the script to insert AWS cost data:
```bash
pip install psycopg2 python-dotenv
python scripts/insert_to_postgres.py
```
This fetches cost data using Steampipe and inserts it into PostgreSQL.

### Step 6: Import Dashboard to Grafana
1. Start Grafana.
2. Import the JSON from `dashboards/aws_cloud_cost_dashboard.json`.
3. Set PostgreSQL as the data source.

Done! 🎉 You should now see your AWS costs visualized.

---

## 🧠 What Each Component Does
- **Steampipe**: Pulls AWS billing and usage data with SQL.
- **Python Script**: Automates inserting that data into a structured DB.
- **PostgreSQL**: Stores cost history for long-term tracking.
- **Grafana**: Visualizes cost per service, region, etc.

---

## 📌 To Do / Coming Next
- Add support for GCP and Azure.
- Create Docker Compose setup.
- Add email/Slack alerts for cost thresholds.
- Add cron automation script.

---

## 🤝 Contributing
PRs welcome! Open an issue if you need support or want to contribute queries for other clouds.
