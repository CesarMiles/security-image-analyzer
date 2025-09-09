# Security Image Analyzer

A containerized Python application that uses AWS Rekognition to detect faces in an image. If people are detected, the image is securely uploaded to an S3 bucket. This project demonstrates modern DevOps practices including containerization, secure configuration management, and cloud automation.

## Architecture & Flow

1.  **Input:** User provides a path to an image file.
2.  **Processing:** The application sends the image to AWS Rekognition via the `detect_faces` API.
3.  **Decision:** If faces are detected (`FaceDetails` > 0), the image is uploaded to a predefined S3 bucket.
4.  **Logging:** The application logs each step of the process with timestamps and log levels for observability.

## Technology Stack

*   **Language:** Python 3.11
*   **Containerization:** Docker
*   **Cloud Provider:** AWS
*   **AWS Services:**
    *   AWS Rekognition (for face detection analysis)
    *   Amazon S3 (for secure image storage)
    *   AWS IAM (for secure access management)
*   **Key Libraries:**
    *   `boto3` (AWS SDK for Python)
    *   `logging` (Python standard library for application logging)

## Project Structure

This project is structured modularly to promote separation of concerns and maintainability.
security-image-analyzer/
├── app.py # Main application orchestrator
├── rekognition_helper.py # Module for AWS Rekognition interactions
├── s3_helper.py # Module for AWS S3 interactions
├── Dockerfile # Definition for building the Docker image
├── requirements.txt # Python project dependencies
├── .env # Environment configuration (gitignored)
├── .gitignore # Specifies intentionally untracked files
└── README.md # This file

## Security Considerations

*   **Least Privilege IAM:** The application uses a dedicated IAM user with a policy granting only the necessary permissions: `rekognition:DetectFaces` and `s3:PutObject` on a specific bucket.
*   **Environment-Based Configuration:** Sensitive configuration (AWS credentials, bucket name) is managed through environment variables loaded from a `.env` file at runtime using Docker's `--env-file` flag. This file is excluded from version control via `.gitignore`.
*   **Input Validation:** The application validates the existence of the input image file before processing.
*   **Error Handling:** Granular exception handling captures specific AWS service errors (`ClientError`) and network errors (`BotoCoreError`) for robust debugging.

## Development Practices

This project implements several professional development practices:

*   **Modular Design:** Code is separated into logical modules for Rekognition and S3 interactions.
*   **Professional Logging:** Uses the Python `logging` module with formatted output instead of `print` statements.
*   **Defensive Programming:** Includes input validation and specific error handling for reliability.

## Local Development

### Prerequisites
*   Docker
*   AWS Account with configured credentials
*   An S3 bucket

### 1. Build the Docker Image
```bash
docker build -t security-image-analyzer .

### 2. Configure Environment
Create a `.env` file in the project root (see `.env.example` for format):
```bash
# .env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name

### 3. Run the Container
docker run --rm -it \
  -v "$(pwd):/data" \
  --env-file .env \
  security-image-analyzer \
  python app.py /data/your-image.jpg