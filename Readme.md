# AWS Weekly Cost Report Automation

This project automates sending a **weekly AWS cost report** via email using **AWS Lambda** and **SNS**.  
It tracks the top AWS services by cost, shows regions, compares current week vs last week, and delivers the report automatically every Monday.

---

## Features

- Fetches AWS cost data via **Cost Explorer**
- Generates a **neatly formatted plain-text table**
- Sends the report via **SNS** to your email
- Compares **current week vs previous week**
- Fully automated with **EventBridge schedule**

---

## Prerequisites

- AWS account with **Cost Explorer enabled**
- Verified email for SNS subscription
- IAM Role for Lambda with permissions:
  - `AWSLambdaBasicExecutionRole`
  - `AmazonCostExplorerReadOnlyAccess`
  - `AmazonSNSFullAccess` (or restricted to your topic)

---

## Setup Instructions

### 1️⃣ Create SNS Topic
1. Go to **AWS SNS → Topics → Create Topic**
2. Select **Standard**, give it a name
3. Add a **subscription** with your email and confirm it

### 2️⃣ Create IAM Role for Lambda
1. Go to **IAM → Roles → Create Role**
2. Select **Lambda** as the service
3. Attach policies:
   - `AWSLambdaBasicExecutionRole`
   - `AmazonCostExplorerReadOnlyAccess`
   - `AmazonSNSFullAccess`
4. Name the role (e.g., `LambdaCostReportRole`)

### 3️⃣ Create Lambda Function
1. Go to **Lambda → Create Function → Author from scratch**
2. Runtime: **Python 3.11**
3. Assign the **IAM role** created
4. Paste the Python code from `lambda_function.py`
5. Update `SNS_TOPIC_ARN` with your topic ARN

### 4️⃣ Test Lambda
- Click **Test** → use a simple event
- Check your email → the report should arrive

### 5️⃣ Automate with EventBridge
1. Go to **EventBridge → Rules → Create rule**
2. Select **Schedule → Cron expression**
   - Example: `cron(30 2 ? * MON *)` → every Monday 8:30 AM IST
3. Add **Lambda function** as target
4. Enable the rule

---

## Sample Report
