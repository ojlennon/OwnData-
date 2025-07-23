from fastapi import FastAPI
import sqlite3
from qdrant_client import QdrantClient

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

def fetch_api_key(api_key: str):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM keys WHERE api_key = ?", (api_key,))
    result = cursor.fetchone()
    conn.close()
    return result

def fetch_permission_string(api_key: str):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT permission_string FROM keys WHERE api_key = ?", (api_key,))
    if cursor.rowcount == 0:
        conn.close()
        return {"error": "API key not found"}, 404
    
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0].split(",")
    return []


@app.get("/field/{api_key}/{field_name}")
def read_field(api_key: str, field_name: str):
    # conn = sqlite3.connect("database.db")
    # cursor = conn.cursor()
    # cursor.execute("SELECT value FROM keys WHERE api_key = ?", (api_key,))
    # if cursor.rowcount == 0:
    #     conn.close()
    #     return {"error": "API key not found"}, 404
    # result = cursor.fetchone()
    # permission_string = result["permission_string"].split(",")
    try:
        permission_string = fetch_permission_string(api_key)
    except Exception as e:
        return {"error": str(e)}, 500

    if not permission_string:
        return {"error": "No permissions found for this API key"}, 403
    
    try:
        normalized_field_name = field_name.lower().replace(" ", "_")
    if field_name not in permission_string:
        return {"error": f"{api_key} not allowed to access field: {field_name}"}, 403
    conn.close()
    if result:
        return {"api_key": api_key, "field_name": field_name, "value": result[0]}
    else:
        return {"error": "Field not found"}, 404