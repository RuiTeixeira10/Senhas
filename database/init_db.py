import sqlite3
import os

# Diretório onde o script está
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminho completo para schema.sql
schema_path = os.path.join(BASE_DIR, "schema.sql")

# Caminho completo para tickets.db
db_path = os.path.join(BASE_DIR, "tickets.db")

# Criar/abrir BD
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Ler e executar schema.sql
with open(schema_path, 'r', encoding='utf-8') as f:
    cursor.executescript(f.read())

conn.commit()
conn.close()

print("Base de dados criada com sucesso (com suporte a ordem_chamada).")

