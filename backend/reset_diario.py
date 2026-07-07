import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "tickets.db")

def reset_diario():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Apagar todos os tickets (reset total)
    cursor.execute("DELETE FROM tickets")

    conn.commit()
    conn.close()

    print("Reset diário concluído.")

if __name__ == "__main__":
    reset_diario()
