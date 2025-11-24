import json
import os
import boto3

sns = boto3.client('sns')

# Put your SNS topic ARN here (copy from SNS console)
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")

def lambda_handler(event, context):
    # Log raw event
    print("Received event:")
    print(json.dumps(event))

    # This is the EventBridge event structure
    # S3 details are inside "detail"
    detail = event.get("detail", {})

    bucket = detail.get("bucket", {}).get("name")
    object_key = detail.get("object", {}).get("key")
    event_name = detail.get("eventName")

    message = {
        "message": "New S3 event received",
        "bucket": bucket,
        "object_key": object_key,
        "event_name": event_name
    }

    # Publish to SNS
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
