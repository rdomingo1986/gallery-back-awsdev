import logging
import boto3
import os
from api_utils import api_response

logger = logging.getLogger()
logger.setLevel(logging.INFO)

if os.environ.get('ENV') == 'LOCAL':
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://172.17.0.2:8000')
    table = dynamodb.Table(os.environ['DYNAMODB_LOCAL'])
else:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def lambda_handler(event, context):
    try:
        print(event)
        # Obtener user_id del claim cognito:username
        user_id = event['requestContext']['authorizer']['claims']['cognito:username']
        
        logger.info(f"Listing images for user {user_id}")
        
        # Query por UserId para obtener todas las imágenes del usuario
        response = table.query(
            KeyConditionExpression='UserId = :user_id',
            ExpressionAttributeValues={
                ':user_id': user_id
            }
        )
        
        images = response.get('Items', [])
        
        logger.info(f"Found {len(images)} images for user {user_id}")
        
        return api_response(200, {"images": images})
        
    except KeyError as e:
        logger.error(f"Missing required parameter: {str(e)}")
        return api_response(400, f"Missing required parameter: {str(e)}")
    except Exception as e:
        logger.error(f"Error listing images: {str(e)}")
        return api_response(500, "Internal server error")
