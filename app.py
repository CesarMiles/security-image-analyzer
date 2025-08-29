import boto3
import os

#Initialization of the clients to be used on the app
rekognition_client = boto3.client('rekognition')
s3_client = boto3.client('s3')

# Function to call the API for rekognition to process the image or to notify if there is any error
def analyze_image(image_bytes):
    print('Sending image to AWS Rekognition')
    try:
        response = rekognition_client.detect_faces(
            Image = {'Bytes' : image_bytes},
            Attributes = ['DEFAULT']
        )
        print('Analysis succesful')
        return response
    except Exception as e:
        print(f'Error with Rekognition: {e}')
        return None
    
#
def upload_to_s3(image_bytes, filename):
    bucket_name = os.environ.get('S3_BUCKET_NAME') #Update bucket name from eviorment
    if not bucket_name:
        print('Error: S3_BUCKET_NAME enviorment variable is not set.')
        return False
    
    try:
        s3_client.put_object(
            Bucket = bucket_name,
            Key = filename,
            Body = image_bytes
        )
        print(f'Image succesfully uploaded to S3 bucket: {bucket_name}')
        return True
    except Exception as e:
        print(f'Error uploading to S3: {e}')
        return False
    

def main(image_path):
    try:
        with open(image_path, 'rb') as image_file:
            image_bytes = image_file.read()
    except FileNotFoundError:
        print(f'Error: The file {image_path} was not found. ')
        return
    
    analysis_result = analyze_image(image_bytes)
    if not analysis_result:
        return[]

    num_people = len(analysis_result['FaceDetails'])
    print(f'Number of people detected: {num_people}')

    if num_people > 0:
        upload_to_s3(image_bytes, os.path.basename(image_path))
    else:
        print('No people detected. Image not saved')
    

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print('Usage: python app.py <path_to_image.jpg>')
    else:
        main(sys.argv[1])