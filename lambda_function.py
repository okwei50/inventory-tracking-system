# Inventory Tracking System v3
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

        cur.execute("""
            ALTER TABLE inventory
            ADD COLUMN IF NOT EXISTS sku VARCHAR(100),
            ADD COLUMN IF NOT EXISTS reorder_point INTEGER DEFAULT 5,
            ADD COLUMN IF NOT EXISTS lead_time_days INTEGER DEFAULT 7,
            ADD COLUMN IF NOT EXISTS supplier_id INTEGER,
            ADD COLUMN IF NOT EXISTS last_updated TIMESTAMP DEFAULT NOW(),
            ADD COLUMN IF NOT EXISTS category VARCHAR(100)
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS suppliers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255),
                phone VARCHAR(50),
                lead_time_days INTEGER DEFAULT 7,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS inventory_transactions (
                id SERIAL PRIMARY KEY,
                inventory_id INTEGER REFERENCES inventory(id),
                transaction_type VARCHAR(50),
                quantity INTEGER,
                timestamp TIMESTAMP DEFAULT NOW(),
                notes TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS forecasts (
                id SERIAL PRIMARY KEY,
                inventory_id INTEGER REFERENCES inventory(id),
                forecast_date DATE,
                predicted_demand INTEGER,
                confidence_score DECIMAL(5,2),
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS safety_stock (
                id SERIAL PRIMARY KEY,
                inventory_id INTEGER REFERENCES inventory(id),
                optimal_quantity INTEGER,
                calculated_at TIMESTAMP DEFAULT NOW()
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS purchase_orders (
                id SERIAL PRIMARY KEY,
                inventory_id INTEGER REFERENCES inventory(id),
                supplier_id INTEGER REFERENCES suppliers(id),
                quantity INTEGER,
                status VARCHAR(50) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT NOW(),
                expected_delivery DATE,
                notes TEXT
            )
        """)

        conn.commit()

        if method == 'GET':
            cur.execute("""
                SELECT id, name, quantity, price, sku,
                       reorder_point, lead_time_days, category
                FROM inventory
                ORDER BY id DESC
            """)
            rows = cur.fetchall()
            items = []
            for row in rows:
                items.append({
                    "id": row[0],
                    "name": row[1],
                    "quantity": row[2],
                    "price": float(row[3]),
                    "sku": row[4],
                    "reorder_point": row[5],
                    "lead_time_days": row[6],
                    "category": row[7]
                })
            cur.close()
            conn.close()
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({
                    "version": "v3",
                    "items": items
                })
            }

        elif method == 'POST':
            body = json.loads(event['body'])
            cur.execute(
                """INSERT INTO inventory
                   (name, quantity, price, sku, reorder_point, lead_time_days, category)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (
                    body['name'],
                    body['quantity'],
                    body['price'],
                    body.get('sku', None),
                    body.get('reorder_point', 5),
                    body.get('lead_time_days', 7),
                    body.get('category', None)
                )
            )
            cur.execute("""
                INSERT INTO inventory_transactions
                (inventory_id, transaction_type, quantity, notes)
                VALUES (currval('inventory_id_seq'), 'restock', %s, 'Initial stock')
            """, (body['quantity'],))
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
