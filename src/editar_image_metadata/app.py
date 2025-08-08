import logging
import boto3
import os
import json
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

        # Obtener image_id del pathParameters
        image_id = event['pathParameters']['id']
        
        # Parse JSON body
        body = json.loads(event['body'])
        
        logger.info(f"Updating image for user {user_id}")
        
        # Get por UserId e ImageId para obtener todas las imágenes del usuario
        response = table.update_item(
            Key={
                'UserId': user_id,
                'ImageId': image_id
            },
            UpdateExpression="SET #Description = :val",
            ExpressionAttributeNames={
                "#Description": "Description"
            },
            ExpressionAttributeValues={
                ":val": body['Description']
            },
            ReturnValues="ALL_NEW"
        )
        
        logger.info(f"Updated image for user {user_id}")
        
        return api_response(200, "Image description updated successfully")
        
    except KeyError as e:
        logger.error(f"Missing required parameter: {str(e)}")
        return api_response(400, f"Missing required parameter: {str(e)}")
    except Exception as e:
        logger.error(f"Error update image: {str(e)}")
        return api_response(500, "Internal server error")
