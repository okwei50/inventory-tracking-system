# Safety Stock Optimizer v1
import json
import psycopg2
import os
import math
from datetime import datetime

def lambda_handler(event, context):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "content-type,x-amz-date,authorization,x-api-key",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
    }

    method = event.get('httpMethod') or event.get('requestContext', {}).get('http', {}).get('method', 'GET')

    if method == 'OPTIONS':
        return {"statusCode": 200, "headers": headers, "body": json.dumps("OK")}

    try:
        conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            database="postgres",
            user="postgres",
            password=os.environ['DB_PASSWORD'],
            connect_timeout=5
        )
        cur = conn.cursor()

        if method == 'GET':
            cur.execute("""
                SELECT i.id, i.name, i.quantity, i.reorder_point,
                       i.lead_time_days, i.category,
                       ss.optimal_quantity, ss.calculated_at
                FROM inventory i
                LEFT JOIN safety_stock ss ON ss.inventory_id = i.id
                AND ss.calculated_at = (
                    SELECT MAX(calculated_at)
                    FROM safety_stock
                    WHERE inventory_id = i.id
                )
                ORDER BY i.id DESC
            """)
            rows = cur.fetchall()
            results = []
            for row in rows:
                results.append({
                    "id": row[0],
                    "name": row[1],
                    "current_stock": row[2],
                    "current_reorder_point": row[3],
                    "lead_time_days": row[4],
                    "category": row[5],
                    "optimal_safety_stock": row[6],
                    "calculated_at": str(row[7]) if row[7] else None
                })
            cur.close()
            conn.close()
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({"version": "v1", "safety_stock": results})
            }

        elif method == 'POST':
            body = json.loads(event.get('body') or '{}')
            service_level = body.get('service_level', 0.95)
            z_scores = {0.90: 1.28, 0.95: 1.65, 0.99: 2.33}
            z = z_scores.get(service_level, 1.65)

            cur.execute("SELECT id, name, lead_time_days FROM inventory ORDER BY id")
            items = cur.fetchall()

            results = []
            for item in items:
                inventory_id = item[0]
                name = item[1]
                lead_time = item[2] or 7

                cur.execute("""
                    SELECT DATE(timestamp) as sale_date, SUM(quantity) as daily_qty
                    FROM inventory_transactions
                    WHERE inventory_id = %s
                    AND transaction_type = 'sale'
                    AND timestamp >= NOW() - INTERVAL '90 days'
                    GROUP BY DATE(timestamp)
                    ORDER BY sale_date
                """, (inventory_id,))
                transactions = cur.fetchall()

                if len(transactions) >= 3:
                    daily_demands = [float(t[1]) for t in transactions]
                    avg_demand = sum(daily_demands) / len(daily_demands)
                    variance = sum((d - avg_demand) ** 2 for d in daily_demands) / len(daily_demands)
                    std_demand = math.sqrt(variance)
                    safety_stock = round(z * std_demand * math.sqrt(lead_time))
                    reorder_point = round((avg_demand * lead_time) + safety_stock)
                    confidence = min(95, 40 + (len(transactions) * 3))
                else:
                    avg_demand = 0.5
                    std_demand = 0.2
                    safety_stock = round(z * std_demand * math.sqrt(lead_time))
                    reorder_point = round((avg_demand * lead_time) + safety_stock)
                    confidence = 25

                cur.execute("""
                    INSERT INTO safety_stock (inventory_id, optimal_quantity, calculated_at)
                    VALUES (%s, %s, NOW())
                """, (inventory_id, safety_stock))

                cur.execute("""
                    UPDATE inventory SET reorder_point = %s, last_updated = NOW()
                    WHERE id = %s
                """, (reorder_point, inventory_id))

                results.append({
                    "id": inventory_id,
                    "name": name,
                    "avg_daily_demand": round(avg_demand, 2),
                    "demand_std_dev": round(std_demand, 2),
                    "lead_time_days": lead_time,
                    "safety_stock": safety_stock,
                    "reorder_point": reorder_point,
                    "service_level": str(int(service_level * 100)) + "%",
                    "confidence": confidence
                })

            conn.commit()
            cur.close()
            conn.close()

            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({
                    "message": "Safety stock calculated successfully",
                    "service_level": str(int(service_level * 100)) + "%",
                    "items_optimized": len(results),
                    "results": results
                })
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)})
        }
