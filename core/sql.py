import sqlite3


DB_PATH = "zomboid.db"


def connect():

    return sqlite3.connect(DB_PATH)




def get_all_items():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, name, type, condition, amount FROM items")
    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "name": r[1],
            "type": r[2],
            "condition": r[3],
            "amount": r[4],
        }
        for r in rows
    ]


def get_item(item_id: int):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, type, condition, amount FROM items WHERE id = ?",
        (item_id,),
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "type": row[2],
        "condition": row[3],
        "amount": row[4],
    }


def create_item(item: dict):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO items (name, type, condition, amount)
        VALUES (?, ?, ?, ?)
        """,
        (item["name"], item["type"], item["condition"], item["amount"]),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def update_item(item_id: int, item: dict):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE items
        SET name=?, type=?, condition=?, amount=?
        WHERE id=?
        """,
        (item["name"], item["type"], item["condition"], item["amount"], item_id),
    )
    conn.commit()
    updated = cur.rowcount
    conn.close()
    return updated > 0


def delete_item(item_id: int):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    deleted = cur.rowcount
    conn.close()
    return deleted > 0


def stats_condition():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT condition FROM items")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return {}

    total = len(rows)
    stats = {}

    for (cond,) in rows:
        stats[cond] = stats.get(cond, 0) + 1

    for cond in stats:
        stats[cond] = round(stats[cond] / total * 100, 2)

    return stats
