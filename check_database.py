import sqlite3

conn = sqlite3.connect('stocks.db')
cursor = conn.cursor()

# **📌 データベースのテーブル一覧**
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(f"\n📌 データベースにあるテーブル一覧: {tables}")

# **📌 各テーブルの構造を確認**
for table in ["share_buyback", "upward_revision", "stock_split"]:
    print(f"\n📌 {table} のカラム構造:")
    cursor.execute(f"PRAGMA table_info({table});")
    columns = cursor.fetchall()
    for col in columns:
        print(col)

conn.close()
