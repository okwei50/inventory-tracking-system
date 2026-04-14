# Purchase Order Auto Generator v1
import json
import psycopg2
import os
from datetime import datetime, timedelta

def lambda_handler(event, context):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "content-type,x-amz-date,authorization,x-api-key",
        "Access-Control-Allow-Methods": "GET,POST,PUT,OPTIONS"
    }
    method = event.get("httpMethod") or event.get("requestContext", {}).get("http", {}).get("method", "GET")
    path = event.get("path") or event.get("rawPath", "/")

    if method == "OPTIONS":
        return {"statusCode": 200, "headers": headers, "body": json.dumps("OK")}

    try:
        conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            database="postgres",
            user="postgres",
            password=os.environ["DB_PASSWORD"],
            connect_timeout=5
        )
        cur = conn.cursor()

        if "/Suppliers" in path:
            if method == "GET":
                cur.execute("SELECT id, name, email, phone, lead_time_days FROM suppliers ORDER BY id DESC")
                rows = cur.fetchall()
                suppliers = [{"id": r[0], "name": r[1], "email": r[2], "phone": r[3], "lead_time_days": r[4]} for r in rows]
                cur.close()
                conn.close()
                return {"statusCode": 200, "headers": headers, "body": json.dumps({"suppliers": suppliers})}
            elif method == "POST":
                body = json.loads(event["body"])
                cur.execute("INSERT INTO suppliers (name, email, phone, lead_time_days) VALUES (%s, %s, %s, %s) RETURNING id",
                    (body["name"], body.get("email", ""), body.get("phone", ""), body.get("lead_time_days", 7)))
                new_id = cur.fetchone()[0]
                conn.commit()
                cur.close()
                conn.close()
                return {"statusCode": 200, "headers": headers, "body": json.dumps({"message": "Supplier added", "id": new_id})}

        elif "/PurchaseOrders" in path:
            if method == "GET":
                sql = "SELECT po.id, po.inventory_id, po.supplier_id, po.quantity, po.status, po.created_at, po.expected_delivery, po.notes, i.name, i.price, s.name, s.email FROM purchase_orders po JOIN inventory i ON i.id = po.inventory_id JOIN suppliers s ON s.id = po.supplier_id ORDER BY po.created_at DESC"
                cur.execute(sql)
                rows = cur.fetchall()
                orders = [{"id": r[0], "inventory_id": r[1], "supplier_id": r[2], "quantity": r[3], "status": r[4], "created_at": str(r[5]), "expected_delivery": str(r[6]) if r[6] else None, "notes": r[7], "item_name": r[8], "item_price": float(r[9]), "supplier_name": r[10], "supplier_email": r[11], "total_value": round(float(r[9]) * r[3], 2)} for r in rows]
                cur.close()
                conn.close()
                return {"statusCode": 200, "headers": headers, "body": json.dumps({"purchase_orders": orders})}

            elif method == "POST":
                body = json.loads(event["body"])
                if body.get("auto_generate", False):
                    sql = "SELECT i.id, i.name, i.quantity, i.reorder_point, i.lead_time_days, i.price, i.supplier_id, ss.optimal_quantity FROM inventory i LEFT JOIN safety_stock ss ON ss.inventory_id = i.id AND ss.calculated_at = (SELECT MAX(calculated_at) FROM safety_stock WHERE inventory_id = i.id) WHERE i.quantity <= i.reorder_point"
                    cur.execute(sql)
                    low_stock = cur.fetchall()
                    cur.execute("SELECT id FROM suppliers ORDER BY id LIMIT 1")
                    default_sup = cur.fetchone()
                    if not default_sup:
                        cur.close()
                        conn.close()
                        return {"statusCode": 400, "headers": headers, "body": json.dumps({"error": "No suppliers found. Add a supplier first."})}
                    default_sup_id = default_sup[0]
                    generated = []
                    for item in low_stock:
                        inv_id, name, qty, reorder, lead = item[0], item[1], item[2], item[3], item[4]
                        price, sup_id, ss = item[5], item[6] or default_sup_id, item[7] or item[3]
                        order_qty = max(ss * 2, reorder * 3, 10)
                        delivery = datetime.now().date() + timedelta(days=lead)
                        cur.execute("SELECT id FROM purchase_orders WHERE inventory_id = %s AND status = 'pending'", (inv_id,))
                        if not cur.fetchone():
                            cur.execute("INSERT INTO purchase_orders (inventory_id, supplier_id, quantity, status, created_at, expected_delivery, notes) VALUES (%s, %s, %s, 'pending', NOW(), %s, %s) RETURNING id",
                                (inv_id, sup_id, order_qty, delivery, "Auto-generated: " + name + " at " + str(qty) + " units"))
                            po_id = cur.fetchone()[0]
                            generated.append({"po_id": po_id, "item": name, "quantity": order_qty, "expected_delivery": str(delivery), "total_value": round(float(price) * order_qty, 2)})
                    conn.commit()
                    cur.close()
                    conn.close()
                    return {"statusCode": 200, "headers": headers, "body": json.dumps({"message": "Generated " + str(len(generated)) + " purchase orders", "orders": generated})}
                else:
                    cur.execute("INSERT INTO purchase_orders (inventory_id, supplier_id, quantity, status, created_at, expected_delivery, notes) VALUES (%s, %s, %s, 'pending', NOW(), %s, %s) RETURNING id",
                        (body["inventory_id"], body["supplier_id"], body["quantity"], body.get("expected_delivery"), body.get("notes", "Manual PO")))
                    po_id = cur.fetchone()[0]
                    conn.commit()
                    cur.close()
                    conn.close()
                    return {"statusCode": 200, "headers": headers, "body": json.dumps({"message": "Purchase order created", "id": po_id})}

            elif method == "PUT":
                body = json.loads(event["body"])
                path_parts = path.strip("/").split("/")
                po_id = path_parts[-1] if len(path_parts) > 1 else None
                if po_id:
                    cur.execute("UPDATE purchase_orders SET status = %s WHERE id = %s", (body.get("status", "pending"), po_id))
                    conn.commit()
                cur.close()
                conn.close()
                return {"statusCode": 200, "headers": headers, "body": json.dumps("Purchase order updated")}

        return {"statusCode": 404, "headers": headers, "body": json.dumps("Route not found")}

    except Exception as e:
        return {"statusCode": 500, "headers": headers, "body": json.dumps({"error": str(e)})}
