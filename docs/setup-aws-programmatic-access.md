# Setup AWS Programmatic Access (Updated for 2025 IAM UI)

This guide helps you create an IAM user with access to AWS billing data via the AWS CLI and API, using the **new IAM user flow**.

---

## ✅ Step 1: Create IAM User (without Access Keys initially)

1. Go to [AWS IAM Console](https://console.aws.amazon.com/iamv2/home#/users)
2. Click **"Create User"**
3. Set a username:  
   → Example: `cloud-cost-monitor`
4. Leave "Management Console access" **unchecked**
5. Click **Next**

---

## ✅ Step 2: Attach Billing Permissions

1. Choose **"Attach policies directly"**
2. Since **`AmazonCostExplorerReadOnlyAccess`** is missing, click:
   → `Create policy`
3. Switch to the **JSON tab** and paste:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ce:Get*",
        "ce:List*",
        "billing:Get*",
        "cur:Get*",
        "organizations:Describe*",
        "organizations:List*"
      ],
      "Resource": "*"
    }
  ]
}
```
4. Click Next, give it a name like:
→ CustomCostExplorerReadOnly

5. Click Create policy

6. Back in the IAM user creation screen, refresh the policy list, and search for CustomCostExplorerReadOnly

7. Select the policy and proceed → click Next, then Create user

---

## ✅ Step 3: Generate Access Keys for Programmatic Access

1. After the user is created, go to:
   → IAM → Users → Click `cloud-cost-monitor`
2. Go to **Security Credentials** tab
3. Scroll to **Access Keys**
4. Click **"Create access key"**
5. Choose:
   - ✅ "Application running outside AWS"
6. Click **Next** → then **Create access key**
7. Copy the:
   - Access Key ID
   - Secret Access Key

> ⚠️ Store these safely. You won’t be able to view the secret key again later.

---

## ✅ Step 4: Configure the AWS CLI on Your VM

Run:

```bash
aws configure
```
Enter the credentials above:

- Access Key ID

- Secret Access Key

- Default region (e.g., us-east-1)

- Output format (e.g., json)

Done! You’re now ready to run Steampipe and query AWS billing data
