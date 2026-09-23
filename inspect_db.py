import sqlite3

conn = sqlite3.connect('prisma/dev.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '_prisma_migrations';")
tables = [r[0] for r in cursor.fetchall()]
print('Tables in DB:', tables)

for t in tables:
    cursor.execute(f'SELECT count(*) FROM "{t}"')
    cnt = cursor.fetchone()[0]
    cursor.execute(f'PRAGMA table_info("{t}")')
    cols = [f"{c[1]} ({c[2]})" for c in cursor.fetchall()]
    print(f"\n--- {t} ({cnt} rows) ---")
    print("Columns:", ", ".join(cols))
    cursor.execute(f'SELECT * FROM "{t}" LIMIT 5')
    rows = cursor.fetchall()
    for row in rows:
        print("  ", row)
