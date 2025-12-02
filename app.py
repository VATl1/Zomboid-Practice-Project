from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from core import sql

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


sql.init_db()


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
    new_id = sql.create_item(item)
    return {"status": "ok", "id": new_id}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: dict):
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
