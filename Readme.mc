# AWS Weekly Cost Report Automation

This project automates sending a **weekly AWS cost report** via email using **AWS Lambda** and **SNS**. The report lists **top AWS services by cost**, regions, and weekly comparisons.

## Features
- Fetches AWS cost data via **Cost Explorer**
- Generates a **plain-text table** for email
- Sends the report automatically via **SNS**
- Compares **current week vs previous week**
- Fully automated with **EventBridge schedule**

## Prerequisites
- AWS account with **Cost Explorer** enabled
- Verified email for SNS subscription
- IAM role with permissions:
  - `AWSLambdaBasicExecutionRole`
  - `AmazonCostExplorerReadOnlyAccess`
  - `AmazonSNSFullAccess` (or restricted to your topic)

## Setup Steps

1. **Create SNS Topic**
   - Go to AWS SNS → Topics → Create Topic
   - Add a subscription with your email → confirm

2. **Create IAM Role for Lambda**
   - Go to AWS IAM → Roles → Create Role
   - Assign Lambda service + permissions listed above

3. **Create Lambda Function**
   - Runtime: Python 3.11
   - Paste `lambda_function.py` code
   - Assign the IAM role created

4. **Update SNS Topic ARN**
   - Replace `SNS_TOPIC_ARN` in `lambda_function.py` with your topic ARN

5. **Test Lambda**
   - Run a test event → check your email for report

6. **Automate with EventBridge**
   - Schedule Lambda to run every Monday using a cron expression
   - Example: `cron(30 2 ? * MON *)` → every Monday 8:30 AM IST

## Sample Report
