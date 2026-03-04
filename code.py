import boto3
from datetime import datetime, timedelta

# AWS clients
ce = boto3.client('ce', region_name='us-east-1')
sns = boto3.client('sns', region_name='us-east-1')

# Replace with your SNS topic ARN
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:123456789012:YourSNSTopic'

# Get date ranges for this week and last week
def get_dates():
    today = datetime.utcnow()
    end = today
    start = end - timedelta(days=7)
    prev_start = start - timedelta(days=7)
    prev_end = end - timedelta(days=7)
    return start, end, prev_start, prev_end

# Fetch AWS cost data
def get_cost(start_date, end_date):
    resp = ce.get_cost_and_usage(
        TimePeriod={'Start': start_date.strftime('%Y-%m-%d'),
                    'End': end_date.strftime('%Y-%m-%d')},
        Granularity='DAILY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'},
                 {'Type': 'DIMENSION', 'Key': 'REGION'}]
    )
    return resp['ResultsByTime']

# Format report as plain-text table
def format_report(current, previous):
    service_cost = {}
    for day in current:
        for item in day['Groups']:
            key = f"{item['Keys'][0]} ({item['Keys'][1]})"
            service_cost[key] = service_cost.get(key, 0) + float(item['Metrics']['UnblendedCost']['Amount'])

    top_services = sorted(service_cost.items(), key=lambda x: x[1], reverse=True)[:10]

    total_curr = sum(service_cost.values())
    total_prev = sum(float(item['Metrics']['UnblendedCost']['Amount'])
                     for day in previous for item in day['Groups'])
    diff = total_curr - total_prev
    diff_sign = "↑" if diff >= 0 else "↓"

    report = "AWS Weekly Cost Report\n\n"
    report += f"{'Service (Region)':40} {'Cost ($)':>10}\n"
    report += "-" * 52 + "\n"
    for svc, cost in top_services:
        report += f"{svc:40} {cost:10.2f}\n\n"

    report += f"{'Total Cost This Week:':40} {total_curr:10.2f}\n"
    report += f"{'Total Cost Last Week:':40} {total_prev:10.2f}\n"
    report += f"{'Difference:':40} {diff_sign} {abs(diff):.2f}\n"
    return report

# Lambda entry point
def lambda_handler(event, context):
    start, end, prev_start, prev_end = get_dates()
    current_cost = get_cost(start, end)
    prev_cost = get_cost(prev_start, prev_end)
    report = format_report(current_cost, prev_cost)
    
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject='AWS Weekly Cost Report',
        Message=report
    )
    
    return {"status": "success"}
