# Demand Forecasting System v1
import json
import psycopg2
import os
from datetime import datetime, timedelta

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
                SELECT 
                    i.id,
                    i.name,
                    i.quantity,
                    i.reorder_point,
                    i.lead_time_days,
                    f.predicted_demand,
                    f.forecast_date,
                    f.confidence_score
                FROM inventory i
                LEFT JOIN forecasts f ON f.inventory_id = i.id
                AND f.forecast_date = (
                    SELECT MAX(forecast_date) 
                    FROM forecasts 
                    WHERE inventory_id = i.id
                )
                ORDER BY i.id DESC
            """)
            rows = cur.fetchall()
            forecasts = []
            for row in rows:
                inventory_id = row[0]
                name = row[1]
                quantity = row[2]
                reorder_point = row[3] or 5
                lead_time_days = row[4] or 7
                predicted_demand = row[5]
                confidence = float(row[7]) if row[7] else None

                days_until_stockout = None
                reorder_needed = False
                urgency = 'ok'

                if predicted_demand and predicted_demand > 0:
                    days_until_stockout = round(quantity / predicted_demand)
                    reorder_needed = days_until_stockout <= lead_time_days
                    if days_until_stockout <= 3:
                        urgency = 'critical'
                    elif days_until_stockout <= lead_time_days:
                        urgency = 'warning'
                    else:
                        urgency = 'ok'

                forecasts.append({
                    "id": inventory_id,
                    "name": name,
                    "current_stock": quantity,
                    "reorder_point": reorder_point,
                    "lead_time_days": lead_time_days,
                    "daily_demand": round(float(predicted_demand), 2) if predicted_demand else None,
                    "days_until_stockout": days_until_stockout,
                    "reorder_needed": reorder_needed,
                    "urgency": urgency,
                    "confidence": confidence,
                    "forecast_30_days": round(float(predicted_demand) * 30) if predicted_demand else None,
                    "forecast_60_days": round(float(predicted_demand) * 60) if predicted_demand else None,
                    "forecast_90_days": round(float(predicted_demand) * 90) if predicted_demand else None
                })

            cur.close()
            conn.close()
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({"version": "v1", "forecasts": forecasts})
            }

        elif method == 'POST':
            cur.execute("SELECT id, name, quantity, lead_time_days FROM inventory ORDER BY id")
            items = cur.fetchall()

            results = []
            for item in items:
                inventory_id = item[0]
                name = item[1]
                quantity = item[2]
                lead_time_days = item[3] or 7

                cur.execute("""
                    SELECT 
                        DATE(timestamp) as sale_date,
                        SUM(quantity) as daily_qty
                    FROM inventory_transactions
                    WHERE inventory_id = %s
                    AND transaction_type = 'sale'
                    AND timestamp >= NOW() - INTERVAL '90 days'
                    GROUP BY DATE(timestamp)
                    ORDER BY sale_date
                """, (inventory_id,))
                transactions = cur.fetchall()

                if len(transactions) >= 2:
                    total_qty = sum(t[1] for t in transactions)
                    days_with_sales = len(transactions)
                    avg_daily = total_qty / days_with_sales

                    if len(transactions) >= 4:
                        first_half = sum(t[1] for t in transactions[:len(transactions)//2])
                        second_half = sum(t[1] for t in transactions[len(transactions)//2:])
                        if second_half > first_half * 1.1:
                            avg_daily = avg_daily * 1.1
                            trend = 'increasing'
                        elif second_half < first_half * 0.9:
                            avg_daily = avg_daily * 0.9
                            trend = 'decreasing'
                        else:
                            trend = 'stable'
                    else:
                        trend = 'stable'

                    confidence = min(95, 50 + (days_with_sales * 2))
                else:
                    avg_daily = 0.5
                    trend = 'insufficient_data'
                    confidence = 30

                forecast_date = datetime.now().date()
                cur.execute("""
                    INSERT INTO forecasts 
                    (inventory_id, forecast_date, predicted_demand, confidence_score)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, (inventory_id, forecast_date, avg_daily, confidence))

                days_until_stockout = round(quantity / avg_daily) if avg_daily > 0 else 999

                results.append({
                    "id": inventory_id,
                    "name": name,
                    "daily_demand": round(avg_daily, 2),
                    "trend": trend,
                    "confidence": confidence,
                    "days_until_stockout": days_until_stockout,
                    "reorder_needed": days_until_stockout <= lead_time_days
                })

            conn.commit()
            cur.close()
            conn.close()

            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({
                    "message": "Forecasts generated successfully",
                    "items_forecast": len(results),
                    "results": results
                })
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)})
        }
