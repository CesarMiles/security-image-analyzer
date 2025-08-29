# Security Image Analyzer

A containerized Python application that uses AWS Rekognition to detect faces in an image. If people are detected, the image is securely uploaded to an S3 bucket.

## Architecture & Flow

1.  User provides an image path.
2.  Application sends the image to AWS Rekognition via the `detect_faces` API.
3.  If faces are detected (`FaceDetails` > 0), the image is uploaded to a predefined S3 bucket.
4.  The application logs each step of the process.

## Technology Stack

*   **Language:** Python 3.11
*   **Containerization:** Docker
*   **Cloud Provider:** AWS
*   **AWS Services:**
    *   AWS Rekognition (for face detection analysis)
    *   Amazon S3 (for secure image storage)
    *   AWS IAM (for secure access management)

## Security Considerations

*   Uses a dedicated IAM user with a custom policy following the principle of least privilege.
*   The policy only grants permissions for `rekognition:DetectFaces` and `s3:PutObject` on a specific bucket.
*   S3 Block Public Access is enabled. Objects are not publicly accessible.
*   AWS credentials are passed to the Docker container securely via a read-only volume mount.

## Local Development

### Prerequisites
*   Docker
*   AWS CLI configured with appropriate credentials
*   An AWS S3 bucket

### Build the Docker Image
```bash
docker build -t security-image-analyzer .