import json

def api_response(status_code, message):
    """
    Genera una respuesta API estándar con headers CORS
    
    Args:
        status_code (int): Código de estado HTTP
        message (str): Mensaje de respuesta
    
    Returns:
        dict: Respuesta formateada para API Gateway
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "DELETE,OPTIONS",
            "Access-Control-Allow-Headers": "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent,X-Requested-With'"
        },
        "body": json.dumps({"message": message})
    }