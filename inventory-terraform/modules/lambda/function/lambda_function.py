import json
import psycopg2
import os

def lambda_handler(event, context):
    if event.get('httpMethod') == 'GET' or not event.get('body'):
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps("Humanizer API is live!")
        }

    try:
        conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            database="postgres",
            user="postgres",
            password=os.environ['DB_PASSWORD'],
            connect_timeout=5
        )
        cur = conn.cursor()
        body = json.loads(event['body'])
        cur.execute(
            "INSERT INTO inventory (name, quantity, price) VALUES (%s, %s, %s)",
            (body['name'], body['quantity'], body['price'])
        )
        conn.commit()
        cur.close()
        conn.close()
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps("Item added successfully")
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
