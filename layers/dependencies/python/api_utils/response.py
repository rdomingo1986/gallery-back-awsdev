import json

def api_response(status_code, data):
    body = {"message": data} if isinstance(data, str) else data
    
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "'*'",
            "Access-Control-Allow-Methods": "'GET,PUT,DELETE,OPTIONS'",
            "Access-Control-Allow-Headers": "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent,X-Requested-With'"
        },
        "body": json.dumps(body)
    }