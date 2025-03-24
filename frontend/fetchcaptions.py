import json
import boto3

# Initialize the S3 client
s3 = boto3.client('s3')

# Define S3 bucket and folder paths
BUCKET_NAME = "auto-caption-videos-123"
TRANSCRIPT_FOLDER = "transcriptions/"  # Where JSON transcripts are stored
SRT_FOLDER = "srt/"  # Where converted SRT files will be saved

def generate_srt(transcript_json):
    """
    Converts an Amazon Transcribe JSON transcript into SRT format.
    """
    captions = transcript_json.get("results", {}).get("items", [])
    srt_content = ""
    caption_index = 1
    start_time, end_time, text = None, None, ""

    for item in captions:
        if item["type"] == "pronunciation":  # Ignore punctuation marks
            if start_time is None:
                start_time = float(item["start_time"])
            end_time = float(item["end_time"])
            text += item["alternatives"][0]["content"] + " "

            # Create a new subtitle block every 5 words or at punctuation marks
            if len(text.split()) >= 5:
                srt_content += f"{caption_index}\n"
                srt_content += f"{format_time(start_time)} --> {format_time(end_time)}\n"
                srt_content += text.strip() + "\n\n"
                caption_index += 1
                start_time, text = None, ""

    return srt_content

def format_time(seconds):
    """
    Converts a timestamp in seconds to SRT format (hh:mm:ss,ms).
    """
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{int(seconds // 3600):02}:{int((seconds % 3600) // 60):02}:{int(seconds % 60):02},{milliseconds:03}"

def lambda_handler(event, context):
    """
    AWS Lambda function to process transcription files and generate SRT subtitles.
    """
    try:
        print("Fetching transcript files from S3...")

        # Retrieve a list of transcription files from S3
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=TRANSCRIPT_FOLDER)

        if 'Contents' not in response:
            print("No transcription files found.")
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "No JSON transcription files found."}),
                "headers": {"Access-Control-Allow-Origin": "*"}
            }

        for obj in response['Contents']:
            file_key = obj['Key']

            if file_key.endswith(".json"):
                print(f"Processing file: {file_key}")
                
                # Download the transcript file from S3
                json_response = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
                transcript_data = json.loads(json_response['Body'].read().decode('utf-8'))

                # Convert transcript JSON to SRT format
                srt_text = generate_srt(transcript_data)

                # Define SRT file location
                srt_file_key = SRT_FOLDER + file_key.replace(TRANSCRIPT_FOLDER, "").replace(".json", ".srt")

                # Upload the generated SRT file back to S3
                s3.put_object(Bucket=BUCKET_NAME, Key=srt_file_key, Body=srt_text, ContentType="text/plain")

                print(f"Successfully converted {file_key} to {srt_file_key}")

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "All transcription files processed successfully."}),
            "headers": {"Access-Control-Allow-Origin": "*"}
        }

    except Exception as e:
        print(f"Error processing files: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Access-Control-Allow-Origin": "*"}
        }
