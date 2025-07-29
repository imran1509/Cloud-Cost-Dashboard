# Cloud-Cost-Dashboard
# Cloud Cost Monitoring with Steampipe, PostgreSQL, and Grafana

## 📌 Overview
This project provides a free and open-source way to monitor AWS cloud costs (GCP and Azure coming soon) using:

- **Steampipe**: For querying cloud APIs using SQL.
- **PostgreSQL**: For storing query results.
- **Grafana**: For visualizing costs in a dashboard.
- **Python**: Automate data extraction & loading.

You can easily extend this to monitor GCP and Azure costs as well.

---

## ✅ Features
- Unified dashboard for all cloud costs.
- No vendor lock-in.
- No cost (uses free-tier APIs and open-source tools).
- Easily customizable with SQL.
- Easily extensible to GCP, Azure, and others.

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
> :bulb: To see how to setup IAM, Policy and AWS access. see here [docs/setup-aws-programmatic-access.md](https://github.com/imran1509/Cloud-Cost-Dashboard/blob/main/docs/setup-aws-programmatic-access.md)

### 2. Installed Tools
You must have the following installed:

- Python (for automation script).
- Docker & Docker Compose (to simplify deployment).
---

## 🔑 Environment Configuration
Create a `.env` file in the project root:

```env
# AWS Credentials
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_DEFAULT_REGION=us-east-1

# PostgreSQL
DB_HOST=postgres
DB_PORT=5432
DB_NAME=cloud_costs
DB_USER=clouduser
DB_PASSWORD=cloudpass

# Steampipe (inside container)
STEAMPIPE_USER=steampipe
STEAMPIPE_HOME=/home/steampipe/.steampipe

```

🛑 Never commit your .env file.

---

## 📁 Repository Structure
```
cloud-cost-dashboard/
├── aws/
│   └── aws.spc                          # Steampipe connection profile
├── dashboards/
│   └── aws_cloud_cost_dashboard.json    # Grafana dashboard JSON
├── docker/
│   └── steampipe/
│       └── Dockerfile                   # Dockerfile for Steampipe (non-root)
├── docs/
│   ├── setup-aws-programmatic-access.md # AWS IAM setup guide
│   └── grafana-dashboard-preview.png    # Dashboard screenshot
├── queries/
│   └── aws_cost_queries.sql             # SQL queries for AWS billing
├── scripts/
│   └── insert_to_postgres.py            # Python script to insert data
├── .env                                 # Environment variables
├── docker-compose.yml                   # Docker Compose file for stack
├── requirements.txt                     # Python dependencies
├── .gitignore                           # Ignore venv, secrets, etc.
├── README.md                            # Project documentation
└── .venv/                               # (optional) Local virtual environment


```

---

## 🛠️ Setup Steps

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/cloud-cost-dashboard.git
cd cloud-cost-dashboard
```

### Step 2: Start Docker Stack

```bash
docker compose up --build -d
```

This will:
  - Build the non-root Steampipe image
  - Start PostgreSQL with credentials
  - Start Grafana (port 3000)   

### Step 3: Run Python Script to Insert Data
Install Python deps and run the ingestion script:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python scripts/insert_to_postgres.py

```
This will:
   - Run Steampipe inside Docker using docker exec
   - Fetch cost data using SQL (queries/aws_cost_queries.sql)
   - Insert the results into PostgreSQL using credentials from .env

You can confirm data exists by running:

```basd
docker exec -it postgres psql -U clouduser -d cloud_costs -c "SELECT * FROM aws_billing LIMIT 5;"
```

### Step 4: 📊 Import Grafana Dashboard
- Go to http://your-IP:3000
- Login: `admin / admin` (you'll be prompted to change password)
- Add PostgreSQL as a Data Source:
Host: postgres:5432
DB Name: cloud_costs
User: clouduser
Password: cloudpass
- Import dashboard from dashboards/aws_cloud_cost_dashboard.json

Done! 🎉 You should now see your AWS costs visualized.

---

## 🧠 What Each Component Does
- Steampipe: Uses SQL to query AWS billing APIs (via plugin)
- Dockerfile: Runs Steampipe as non-root for security
- Python script: Automates querying and inserts results into PostgreSQL
- PostgreSQL: Stores historical cost data
- Grafana: Reads data from PostgreSQL and renders cost dashboards

---

## 📌 To Do / Coming Next
- Add support for GCP and Azure.
- Add email/Slack alerts for cost thresholds.
- Add cron automation script.

---

## 🤝 Contributing
PRs welcome! Open an issue if you need support or want to contribute queries for other clouds.
