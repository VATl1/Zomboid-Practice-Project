from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core import sql

app = FastAPI()

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Normalizer --------------------
def normalize_item_keys(item: dict):
    return {
        "name": item.get("name") or item.get("Name"),
        "type": item.get("type") or item.get("Type"),
        "condition": item.get("condition") or item.get("Condition"),
        "amount": item.get("amount") or item.get("Amount"),
    }

# -------------------- ROUTES --------------------

@app.get("/items")
def get_items():
    return sql.get_all_items()

@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = sql.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items")
def create_item(item: dict):
    item = normalize_item_keys(item)
    new_id = sql.create_item(item)
    return {"status": "ok", "id": new_id}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: dict):
    item = normalize_item_keys(item)
    if not sql.update_item(item_id, item):
        raise HTTPException(status_code=404, detail="Item not found")
    return {"status": "updated"}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if not sql.delete_item(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return {"status": "deleted"}

@app.get("/stats/condition")
def stats_condition():
    return sql.stats_condition()
