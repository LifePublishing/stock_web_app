import requests
from bs4 import BeautifulSoup
import pandas as pd

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

# データを格納するリスト
data = []

# テーブルが見つかった場合のみ処理
if table:
    for row in table.find_all("tr")[1:]:  # ヘッダー行を除く
        columns = row.find_all("td")

        if len(columns) < 9:  # データが少ない行はスキップ
            continue

        # 銘柄コード
        code = columns[0].text.strip()

        # 銘柄名
        name = columns[1].text.strip()

        # 対通期進捗率（数値変換を試みる）
        try:
            progress_rate = float(columns[7].text.strip())  # 数値型に変換
        except ValueError:
            continue  # 数値に変換できない場合はスキップ

        # 条件（対通期進捗率80%以上）を満たすものだけ追加
        if progress_rate >= 80.0:
            data.append([code, name, "上方修正狙い"])

# DataFrameに変換
df = pd.DataFrame(data, columns=["銘柄コード", "銘柄名", "何狙いなのか"])

# CSVファイルとして保存
df.to_csv("kabutan_top_stocks.csv", index=False, encoding="utf-8-sig")

# 結果を表示
print(df)
