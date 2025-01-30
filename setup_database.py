import sqlite3

# データベースを作成または接続
conn = sqlite3.connect('stocks.db')
cursor = conn.cursor()

# 📌 stocks テーブルの作成（このテーブルが fetch_stock_data.py で使用される）
cursor.execute('''
CREATE TABLE IF NOT EXISTS stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    target TEXT NOT NULL
)
''')

# 📌 自社株買いテーブルの作成（カラム名を統一）
cursor.execute('''
CREATE TABLE IF NOT EXISTS share_buyback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    rate TEXT NOT NULL,
    period TEXT NOT NULL
)
''')

# 📌 上方修正テーブルの作成
cursor.execute('''
CREATE TABLE IF NOT EXISTS upward_revision (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    progress_rate REAL NOT NULL
)
''')

# 📌 株式分割テーブルの作成
cursor.execute('''
CREATE TABLE IF NOT EXISTS stock_split (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    stock_price INTEGER NOT NULL,
    last_split_date TEXT NOT NULL
)
''')

# データベースを保存して接続を閉じる
conn.commit()
conn.close()

print("✅ データベースが作成されました！（修正済み）")
