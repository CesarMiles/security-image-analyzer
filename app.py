import os
import sys
import logging
from rekognition_helper import analyze_image
from s3_helper import upload_to_s3


# Configuration to log globally for the entire application
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def main(image_path):
    logger = logging.getLogger(__name__)

    try:
        with open(image_path, 'rb') as image_file:
            image_bytes = image_file.read()
    except FileNotFoundError:
        logger.error(f'Error: The file {image_path} was not found. ')
        return
    
    analysis_result = analyze_image(image_bytes)
    if not analysis_result:
        return

    num_people = len(analysis_result['FaceDetails'])
    logger.info(f'Number of people detected: {num_people}')

    if num_people > 0:
        upload_to_s3(image_bytes, os.path.basename(image_path))
    else:
        logger.info('No people detected. Image not saved')
    

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    if len(sys.argv) != 2:
        logger.info('Usage: python app.py <path_to_image.jpg>')
    else:
        main(sys.argv[1])