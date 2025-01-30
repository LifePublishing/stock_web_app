from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# 📌 データベースから銘柄情報を取得する関数
def get_stocks():
    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()

    cursor.execute("SELECT code, name, target FROM stocks")
    stocks = cursor.fetchall()

    conn.close()
    return stocks

# 📌 Webページを表示するルート
@app.route('/')
def index():
    stocks = get_stocks()
    return render_template('index.html', stocks=stocks)

if __name__ == '__main__':
    app.run(debug=True)
