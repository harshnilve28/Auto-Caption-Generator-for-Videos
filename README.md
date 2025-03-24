# Auto-Caption Generator for Videos

## 📌 Overview
The **Auto-Caption Generator** is a serverless application that automatically generates captions for uploaded videos using AWS services. It transcribes speech using **Amazon Transcribe**, converts it to **SRT format**, and allows users to download the captions via a web interface.

## 🎯 Features
✅ Upload video files through a simple frontend.
✅ Automatic transcription using **Amazon Transcribe**.
✅ Converts JSON transcription into **SRT format**.
✅ Secure pre-signed URLs for file upload and download.
✅ API Gateway integration for managing endpoints.

## 🛠️ AWS Architecture

```mermaid
graph TD;
    A[User Requests Upload URL] -->|API Gateway| B[Lambda: GenerateUploadURL];
    B -->|Returns Pre-signed URL| C[Frontend Uploads Video to S3];
    C -->|Trigger Lambda| D[Lambda: ProcessVideoForTranscription];
    D -->|Send to Transcribe| E[Amazon Transcribe];
    E -->|Generate JSON Captions| F[Lambda: FetchCaptions];
    F -->|Convert JSON to SRT| G[Store SRT in S3];
    G -->|Generate Pre-signed URL| H[API Gateway];
    H -->|Provide SRT File to User| I[Frontend Download];

```

## 📂 Project Structure
```
/auto-caption-generator
│── /frontend               # HTML, JavaScript for UI
│── /backend                # Lambda functions
│   ├── GenerateUploadURL/   # Handles secure video upload URLs
│   ├── ProcessVideoForTranscription/  # Initiates transcription
│   ├── FetchCaptions/       # Fetches and provides SRT files
│── /screenshots            # Architecture and UI images
│── /scripts                # Deployment scripts (optional)
│── README.md               # Project documentation
│── .gitignore              # Ignore unnecessary files
│── requirements.txt        # Dependencies (if applicable)
```

## 🚀 How It Works
1️⃣ **Request Upload URL** – User requests a pre-signed URL for secure upload.  
2️⃣ **Upload Video** – The video is uploaded directly to S3.  
3️⃣ **Transcription Starts** – Video upload triggers a Lambda function.  
4️⃣ **JSON to SRT Conversion** – Another Lambda function processes the transcription.  
5️⃣ **Download Captions** – User retrieves the SRT file via API Gateway.

## 🔗 API Endpoints
| Action | Method | Endpoint |
|--------|--------|------------|
| Request Upload URL | GET | `/generate-upload-url` |
| Get Transcription Status | GET | `/transcription-status?file={filename}` |
| Download SRT File | GET | `/download-srt?file={filename}` |

## 🖼️ Screenshots
### **Architecture Diagram**
![Architecture](screenshots/architecture.png)

### **Frontend Upload Page**
![Upload Page](screenshots/upload-page.png)

## 📹 Video Demo
[![Watch Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

## 🛠️ Technologies Used
- **Amazon S3** – Stores videos and captions
- **AWS Lambda** – Handles processing tasks
- **Amazon Transcribe** – Converts speech to text
- **API Gateway** – Manages API requests
- **IAM Roles & Policies** – Secure access management

## 📌 Next Steps
- [ ] Improve error handling
- [ ] Implement batch processing for large files
- [ ] Add support for multiple languages

## 🤝 Contributing
Feel free to fork this repository, submit issues, or suggest improvements!

## 📝 License
This project is open-source under the MIT License.

