**Serverless S3 Event Notifier**
A fully serverless, event-driven architecture that detects new S3 object uploads, routes the event through EventBridge, processes it with a Lambda function, and delivers an instant notification via an SNS topic (email/SMS).🚀
**Project Overview**
This project showcases a modern, loosely-coupled AWS workflow suitable for cloud engineering, DevOps, serverless development, and event-driven architectures. It demonstrates best practices for clean event routing and minimal coupling between services.Key Features100% Serverless: No infrastructure to manage.Automatic Detection: Instantly detects new S3 object uploads (PutObject events).Clean Event Routing: Uses EventBridge as a central event bus, avoiding direct S3-to-Lambda coupling.Instant Notifications: SNS delivers notifications via email or SMS.Low Cost & Scalable: Pay-per-use model with automatic scaling.Production-Ready: Simple yet robust architecture pattern.💡
**ArchitectureThe workflow **is a classic example of event-driven design, ensuring high reliability and separation of concerns.$$S3 \text{ Bucket} \to \text{EventBridge Rule} \to \text{Lambda Function} \to \text{SNS Topic (Email Notification).
**Flow Explanation**
Object Upload: A new object is uploaded to the designated S3 Bucket.Event Capture: EventBridge automatically captures the S3 API event (Object Created) from the default event bus.Rule Match: A custom EventBridge Rule matches the specific S3 event pattern (e.g., bucket name, event type) and invokes the target.Event Processing: The Lambda Function is triggered, processes the event details (extracting bucket name, object key, etc.).Notification: Lambda publishes the structured message to the SNS Topic.Delivery: SNS instantly sends an email or SMS notification to all subscribed users.🛠️ DeploymentThis project is best deployed using a tool like AWS SAM or AWS CDK for defining the infrastructure as code (IaC).PrerequisitesAWS CLI configured with appropriate permissions.Node.js and npm (for CDK) or Python and pip (for SAM).Your preferred IaC framework (SAM, CDK, or Terraform).Step-by-Step Setup (Conceptual)Create SNS Topic: Create an SNS topic and subscribe your email address to it. Confirm the subscription via the email link you receive. Note the Topic ARN.Create Lambda:Create a Python 3.x Lambda function.Set an environment variable SNS_TOPIC_ARN to the ARN from step 1.Attach an IAM Role allowing s3:GetObject (if needed later) and sns:Publish to the specific SNS topic.Deploy the provided Lambda code.Create S3 Bucket: Create a new S3 bucket where uploads will occur.Create EventBridge Rule:Create an EventBridge Rule targeting the default event bus.Set the Event Pattern to capture S3 events from your specific bucket.JSON{
  "source": ["aws.s3"],
  "detail-type": ["AWS API Call via CloudTrail"],
  "detail": {
    "eventSource": ["s3.amazonaws.com"],
    "eventName": ["PutObject", "CopyObject"],
    "requestParameters": {
      "bucketName": ["YOUR-S3-BUCKET-NAME"]
    }
  }
}
Set the Target of the rule to the Lambda Function created in step 2.💻 Lambda Function Code (lambda_function.py)The Lambda function is responsible for parsing the complex EventBridge payload and sending a concise, readable message to SNS.Pythonimport json
import os
import boto3

sns = boto3.client('sns')

# SNS Topic ARN from environment variables
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")

def lambda_handler(event, context):
    print("Received event:")
    print(json.dumps(event))

    # EventBridge sends the S3 details inside the 'detail' key
    detail = event.get("detail", {})
    bucket = detail.get("requestParameters", {}).get("bucketName")
    object_key = detail.get("requestParameters", {}).get("key")
    event_name = detail.get("eventName")

    # Correcting structure to extract S3 details from CloudTrail structure
    if not bucket:
        bucket = detail.get("bucket", {}).get("name") # Alternative path if structure changes

    if not object_key:
         object_key = detail.get("object", {}).get("key") # Alternative path

    message = {
        "message": "New S3 event received",
        "bucket": bucket,
        "object_key": object_key,
        "event_name": event_name
    }

    if SNS_TOPIC_ARN:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="S3 Event via EventBridge → Lambda → SNS",
            Message=json.dumps(message, indent=2)
        )
    else:
        print("SNS_TOPIC_ARN not set!")

    return {
        "statusCode": 200,
        "body": json.dumps(message)
    }
