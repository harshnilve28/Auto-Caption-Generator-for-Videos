import json
import boto3
import os
import time
import uuid

# Initialize the S3 client
s3 = boto3.client('s3')

# Get the S3 bucket name from environment variables (default provided)
BUCKET_NAME = os.environ.get("BUCKET_NAME", "auto-caption-videos-123")

def lambda_handler(event, context):
    """
    AWS Lambda function to generate a pre-signed URL for uploading videos.
    This URL allows users to upload an MP4 file directly to S3 without requiring AWS credentials.
    """
    try:
        # Generate a unique filename in the "videos/" folder
        unique_id = uuid.uuid4().hex  # Generate a random unique ID
        timestamp = int(time.time())  # Get the current timestamp
        file_name = f"videos/{timestamp}-{unique_id}.mp4"

        print(f"Generating upload URL for {file_name}...")

        # Generate a pre-signed URL valid for 1 hour (3600 seconds)
        upload_url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': file_name,
                'ContentType': 'video/mp4'
            },
            ExpiresIn=3600
        )

        print(f"Pre-signed URL generated successfully.")

        return {
            "statusCode": 200,
            "body": json.dumps({"uploadURL": upload_url, "fileName": file_name}),
            "headers": {"Access-Control-Allow-Origin": "*"}
        }

    except Exception as e:
        print(f"Error generating upload URL: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Failed to generate upload URL: {str(e)}"}),
            "headers": {"Access-Control-Allow-Origin": "*"}
        }
