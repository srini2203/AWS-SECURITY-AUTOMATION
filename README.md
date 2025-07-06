# AWS Security Automation: Auto-Block Failed Console Logins

This project shows a simple **AWS security automation workflow**:

- Detects failed AWS console login attempts in real time with CloudTrail and CloudWatch Logs.
- Automatically blocks suspicious IP addresses by updating your security group using Lambda.
- Sends email alerts via SNS to keep you informed of security actions.

It demonstrates a lightweight, serverless SOAR (Security Orchestration, Automation, and Response) pipeline using AWS services.

## Features
- Real-time detection of failed console login attempts.
- Automatic blocking of suspicious IPs in your security group.
- Email alerts with details of blocked IPs for transparency.
- Fully serverless, cost-effective, and scalable.

## How it works
1. A user (or attacker) tries and fails to log in to the AWS console.
2. CloudTrail records the failed login event.
3. The event is sent to a CloudWatch Log Group.
4. A Lambda function is triggered by the new log entry.
5. Lambda extracts the attacker’s IP address, blocks it in your security group, and sends an SNS email alert.

## Technologies Used
- AWS CloudTrail
- AWS CloudWatch Logs
- AWS Lambda (Python)
- AWS SNS
- AWS EC2 Security Groups
- AWS IAM


## Setup Guide
1. **Enable CloudTrail** and configure it to send logs to a CloudWatch Log Group (e.g., 'cloudtrail-logs').
2. **Create an SNS topic** (e.g., 'security-alerts') and subscribe your email to receive alerts.
3. **Create a Lambda function** with:
   - Runtime: Python 3.12
   - Attached IAM policies:
      - AWSLambdaBasicExecutionRole
      - AmazonEC2FullAccess
      - AmazonSNSFullAccess
      - CloudWatchLogsFullAccess
4. **Add a trigger** to your Lambda function for the CloudWatch Log Group.
5. **Deploy the Lambda code** from 'lambda_function.py' in this repository.


## Testing the Setup
1. Try a failed login to your AWS account (use wrong credentials).
2. Check that:
   - The Lambda function runs.
   - The attacker’s IP is added as a deny rule in your security group.
   - You get an SNS email with details of the blocked IP.


## Future Enhancements
- Add IP allow-lists to avoid blocking trusted IPs.
- Block only after multiple failed attempts.
- Integrate with AWS Security Hub for centralized security insights.
- Detect suspicious API calls and unusual IAM activity.



## Author

Srini Vasan

