import json
import boto3
import time

# Initialize AWS clients
s3 = boto3.client('s3')
transcribe = boto3.client('transcribe')

# S3 bucket and folder paths
BUCKET_NAME = "auto-caption-videos-123"
TRANSCRIPT_FOLDER = "transcriptions/"  # Destination for transcription results

def lambda_handler(event, context):
    """
    AWS Lambda function triggered when a new MP4 file is uploaded to S3.
    It starts an Amazon Transcribe job to generate captions.
    """
    try:
        # Extract file details from the event trigger
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        file_key = event['Records'][0]['s3']['object']['key']

        # Process only MP4 files
        if not file_key.lower().endswith(".mp4"):
            print(f"Skipping non-MP4 file: {file_key}")
            return {
                "statusCode": 400,
                "body": json.dumps({"message": f"File {file_key} is not an MP4, skipping."})
            }

        # Generate a unique transcription job name
        job_name = f"{file_key.replace('/', '-')}-{int(time.time())}"
        file_url = f"s3://{bucket_name}/{file_key}"

        print(f"Starting transcription for {file_key} with job name {job_name}...")

        # Start transcription job
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': file_url},
            MediaFormat='mp4',
            LanguageCode='en-US',
            OutputBucketName=bucket_name,
            OutputKey=TRANSCRIPT_FOLDER  # Store JSON results in /transcriptions/
        )

        print(f"Transcription job {job_name} started successfully.")

        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"Started transcription job: {job_name}"})
        }

    except Exception as e:
        print(f"Error starting transcription job: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Failed to start transcription: {str(e)}"})
        }
