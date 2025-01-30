from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# CSVファイルを読み込んでデータを取得する関数
def get_stock_data():
    try:
        df = pd.read_csv("kabutan_top_stocks.csv", encoding="utf-8-sig")
        return df.to_dict(orient="records")  # 辞書形式でデータを返す
    except FileNotFoundError:
        return []  # ファイルがない場合は空リストを返す

# ルートページ（メインページ）
@app.route("/")
def index():
    stocks = get_stock_data()
    return render_template("index.html", stocks=stocks)

if __name__ == "__main__":
    app.run(debug=True)
