
import json
import os
import psycopg2

def handler(request):
    if request["method"] != "POST":
        return {"statusCode": 200, "body": "Send a POST request"}

    body = json.loads(request["body"])
    username = body.get("username", "").strip()
    password = body.get("password", "").strip()

    if not username or not password:
        return {"statusCode": 400, "body": "Fill all fields"}

    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return {"statusCode": 200, "body": "Registered successfully"}
    except Exception as e:
        return {"statusCode": 400, "body": str(e)}
    finally:
        cur.close()
        conn.close()
