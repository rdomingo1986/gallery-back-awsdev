import json
import logging
import boto3
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def lambda_handler(event, context):
    try:
        # Procesar registros de S3
        for record in event.get('Records', []):
            if record.get('eventSource') == 'aws:s3':
                bucket = record['s3']['bucket']['name']
                key = record['s3']['object']['key']
                event_name = record['eventName']
                
                logger.info(f"Processing {event_name} for {key} in {bucket}")
                
                # Leer metadata del objeto S3
                response = s3_client.head_object(Bucket=bucket, Key=key)
                metadata = response.get('Metadata', {})
                
                user_id = metadata.get('user_id')
                image_id = metadata.get('image_id')
                description = metadata.get('description', '')
                
                if user_id and image_id:
                    # Obtener región del bucket
                    bucket_location = s3_client.get_bucket_location(Bucket=bucket)
                    region = bucket_location['LocationConstraint'] or 'us-east-1'
                    image_url = f"https://{bucket}.s3.{region}.amazonaws.com/{key}"
                    
                    # Guardar en DynamoDB
                    table.put_item(
                        Item={
                            'UserId': user_id,
                            'ImageId': image_id,
                            'ImageUrl': image_url,
                            'Description': description
                        }
                    )
                    
                    logger.info(f"Metadata saved for user {user_id}, image {image_id}")
                else:
                    logger.warning(f"Missing user_id or image_id in metadata for {key}")
                    raise Exception(f"Missing required metadata for {key}")
                
        return True
        
    except Exception as e:
        logger.error(f"Error processing S3 event: {str(e)}")
        raise
