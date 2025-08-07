import json
import logging
import boto3
import os

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
        
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "DELETE,OPTIONS",
                "Access-Control-Allow-Headers": "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent,X-Requested-With'"
            },
            "body": json.dumps({"message": "Image deleted successfully"})
        }
        
    except KeyError as e:
        logger.error(f"Missing required parameter: {str(e)}")
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "DELETE,OPTIONS",
                "Access-Control-Allow-Headers": "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent,X-Requested-With'"
            },
            "body": json.dumps({"error": f"Missing required parameter: {str(e)}"})
        }
    except Exception as e:
        logger.error(f"Error deleting image metadata: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "DELETE,OPTIONS",
                "Access-Control-Allow-Headers": "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent,X-Requested-With'"
            },
            "body": json.dumps({"error": "Internal server error"})
        }
