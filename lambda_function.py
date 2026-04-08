# Inventory Tracking System v2
import json
import psycopg2
import os

def lambda_handler(event, context):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "content-type,x-amz-date,authorization,x-api-key",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
    }

    method = event.get('httpMethod') or event.get('requestContext', {}).get('http', {}).get('method', 'GET')

    if method == 'OPTIONS':
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps("OK")
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

        cur.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                quantity INTEGER NOT NULL,
                price DECIMAL(10,2) NOT NULL
            )
        """)
        conn.commit()

        if method == 'GET':
            cur.execute("SELECT id, name, quantity, price FROM inventory ORDER BY id DESC")
            rows = cur.fetchall()
            items = []
            for row in rows:
                items.append({
                    "id": row[0],
                    "name": row[1],
                    "quantity": row[2],
                    "price": float(row[3])
                })
            cur.close()
            conn.close()
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps(items)
            }

        elif method == 'POST':
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
                "headers": headers,
                "body": json.dumps("Item added successfully")
            }

        else:
            return {
                "statusCode": 405,
                "headers": headers,
                "body": json.dumps("Method not allowed")
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)})
        }
