import logging
import boto3
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        for record in event.get('Records', []):
            if record.get('eventName') == 'REMOVE' and record.get('eventSource') == 'aws:dynamodb':
                old_image = record['dynamodb'].get('OldImage', {})
                image_url = old_image.get('ImageUrl', {}).get('S', '')
                
                if image_url:
                    bucket, key = extract_s3_info(image_url)
                    
                    if bucket and key:
                        s3_client.delete_object(Bucket=bucket, Key=key)
                        logger.info(f"Deleted S3 object: {bucket}/{key}")
                    else:
                        logger.warning(f"Could not extract bucket/key from URL: {image_url}")
                        
        return True
        
    except Exception as e:
        logger.error(f"Error processing DynamoDB stream event: {str(e)}")
        raise

def extract_s3_info(image_url):
    match = re.match(r'https://([^.]+)\.s3\.([^.]+)\.amazonaws\.com/(.+)', image_url)
    if match:
        bucket = match.group(1)
        key = match.group(3)
        return bucket, key
    return None, None
