import logging
import boto3
import os
from api_utils import api_response

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def lambda_handler(event, context):
    try:
        print(event)
        # Obtener user_id del claim cognito:username
        user_id = event['requestContext']['authorizer']['claims']['cognito:username']
        
        # Obtener image_id del path parameter
        image_id = event['pathParameters']['id']
        
        logger.info(f"Deleting image {image_id} for user {user_id}")
        
        # Eliminar registro de DynamoDB
        table.delete_item(
            Key={
                'UserId': user_id,
                'ImageId': image_id
            }
        )
        
        logger.info(f"Image metadata deleted for user {user_id}, image {image_id}")
        
        return api_response(200, "Image deleted successfully")
        
    except KeyError as e:
        logger.error(f"Missing required parameter: {str(e)}")
        return api_response(400, f"Missing required parameter: {str(e)}")
    except Exception as e:
        logger.error(f"Error deleting image metadata: {str(e)}")
        return api_response(500, "Internal server error")
