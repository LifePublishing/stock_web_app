import requests
from bs4 import BeautifulSoup
import sqlite3

# 取得対象URL（3Qの対通期進捗率ランキングページ）
url = "https://kabutan.jp/tansaku/?mode=1_funda_05&market=0&capitalization=-1&stc=&stm=0&page=1"

# ヘッダー情報（スクレイピング対策）
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

# ページ取得
response = requests.get(url, headers=headers)
response.encoding = response.apparent_encoding  # 文字コードを適切に設定

# HTML解析
soup = BeautifulSoup(response.text, "html.parser")

# テーブルを取得
table = soup.find("table", {"class": "stock_table"})

# データベースに接続
conn = sqlite3.connect("stocks.db")
cursor = conn.cursor()

# 既存のデータをクリア（毎回リフレッシュ）
cursor.execute("DELETE FROM stocks")

# テーブルが見つかった場合のみ処理
data = []
if table:
    for row in table.find_all("tr")[1:]:  # ヘッダー行を除く
        columns = row.find_all("td")

        if len(columns) < 9:  # データが少ない行はスキップ
            continue

        try:
            # 銘柄コード（数値のみ取得）
            code = columns[0].text.strip()
            if not code.isdigit():  # 銘柄コードが数字でない場合はスキップ
                continue

            # 銘柄名（余計なデータを取り除く）
            name = columns[1].text.strip()

            # 対通期進捗率（数値変換を試みる）
            progress_rate = float(columns[7].text.strip())

            # 条件（対通期進捗率80%以上）を満たすものだけ追加
            if progress_rate >= 80.0:
                data.append((code, name, "上方修正狙い"))

        except Exception as e:
            print(f"データ処理中にエラー: {e}")
            continue  # エラーがあっても処理を続行

# データベースに保存
cursor.executemany("INSERT INTO stocks (code, name, target) VALUES (?, ?, ?)", data)

# データベースの変更を保存
conn.commit()
conn.close()

print(f"{len(data)} 件のデータを取得し、保存しました！")
