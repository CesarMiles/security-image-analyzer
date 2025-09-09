import boto3
import logging
from botocore.exceptions import ClientError, BotoCoreError

#Initialization of the clients to be used on the app
rekognition_client = boto3.client('rekognition')

#Set up logging variable
logger = logging.getLogger()

# Function to call the API for rekognition to process the image or to notify if there is any error
def analyze_image(image_bytes):
    logger.info("Sending image to AWS Rekognition")
    try:
        response = rekognition_client.detect_faces(
            Image = {'Bytes' : image_bytes},
            Attributes = ['DEFAULT']
        )
        logger.info("Analysis succesful")
        return response
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logger.error(f"AWS Rekognition service error({error_code}): {error_message}")
        return None
    
    except BotoCoreError as e:
        logger.error(f"Network or core error calling Rekognition: {e}")
        return None
    
    except Exception as e:
        logger.critical(f"An unexpected error ocurred: {e}")
        return None