import json
import boto3
import os

# IMPORTANT: always set region explicitly
ses = boto3.client("ses", region_name="us-west-1")


def lambda_handler(event, context):

    try:
        # Get S3 event data
        record = event["Records"][0]

        bucket_name = record["s3"]["bucket"]["name"]
        file_name = record["s3"]["object"]["key"]

        # Environment variables
        sender_email = os.environ["SENDER_EMAIL"]
        receiver_email = os.environ["RECEIVER_EMAIL"]

        subject = "🚀 New File Uploaded to S3"

        body = f"""
A new file has been uploaded to your S3 bucket.

Bucket: {bucket_name}
File: {file_name}

This is an automated notification from AWS Lambda.
"""

        # Send email using SES
        response = ses.send_email(
            Source=sender_email,
            Destination={
                "ToAddresses": [receiver_email]
            },
            Message={
                "Subject": {
                    "Data": subject,
                    "Charset": "UTF-8"
                },
                "Body": {
                    "Text": {
                        "Data": body,
                        "Charset": "UTF-8"
                    }
                }
            }
        )

        print("Email sent successfully:", response)

        return {
            "statusCode": 200,
            "body": json.dumps("Email sent successfully")
        }

    except Exception as e:
        print("Error occurred:", str(e))

        return {
            "statusCode": 500,
            "body": json.dumps(f"Error: {str(e)}")
        }