import os

def lambda_handler(event, context):
    token = event.get("headers", {}).get("x-api-key", "")
    valid_key = os.environ.get("API_KEY", "")
    if token == valid_key and token != "":
        return {"isAuthorized": True, "context": {"user": "authorized"}}
    else:
        return {"isAuthorized": False}
