import sqlite3


def connect():
    return sqlite3.connect("myDB.db")


# CREATE
def post(data):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (data["name"], data["email"])
        )
        conn.commit()
        conn.close()
        return True, None
    except sqlite3.IntegrityError:
        return False, "EMAIL_DUPLICADO"


# READ
def get():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()

    users = []
    for row in rows:
        users.append({
            "id": row[0],
            "name": row[1],
            "email": row[2]
        })

    return users


# UPDATE
def put(id, data):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET name = ?, email = ? WHERE id = ?",
        (data["name"], data["email"], id)
    )
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return False

    conn.close()
    return True


# DELETE
def delete(id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return False

    conn.close()
    return True
