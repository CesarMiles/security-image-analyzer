import os
import boto3
import logging
from botocore.exceptions import ClientError, BotoCoreError

#Initialization of the clients to be used on the app
s3_client = boto3.client('s3')

#Set up logging variable
logger = logging.getLogger()

# Function to upload the image to S3 once its verified.
def upload_to_s3(image_bytes, filename):
    bucket_name = os.environ.get('S3_BUCKET_NAME') 
    if not bucket_name:
        logger.error('Error: security-image-analyzer-cm enviorment variable is not set.')
        return False
    
    try:
        s3_client.put_object(
            Bucket = bucket_name,
            Key = filename,
            Body = image_bytes
        )
        logger.info(f'Image succesfully uploaded to S3 bucket: {bucket_name}')
        return True
    
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logger.error(f"AWS S3 service error ({error_code}): {error_message}")
        return False
    
    except BotoCoreError as e:
        logger.error(f"Network or core error uploading to S3: {e}")
        return False
    
    except Exception as e:
        logger.critical(f"An unexcpeted error ocured during S3 upload: {e}")
        return False