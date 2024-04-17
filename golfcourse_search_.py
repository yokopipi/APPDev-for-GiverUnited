#############
#【関数名】
#ゴルフ場検索（golfcourse_search）
#【処理内容】
#楽天GORAのAPIを利用して検索結果となるゴルフ場一覧を作成する。

#【パラメータ】
# ・エリア：文字列[リスト]
# ・プレー日：日付
# ・プレー料金（最低値）：数字
# ・プレー料金（最高値）：数字
# ・スタート時間：文字列[リスト]
#【返り値】
# ・ゴルフ場一覧：データフレーム
#############

def golfcourse_search(area,play_date,min_fee,max_fee,start_times):
    import pandas as pd

    # 空のデータフレームを定義するための列名
    columns = ['golf_course_name', 'min_price', 'max_price', 'rating', 'address', 'distance_from_highway', 'url']

    # 空のデータフレームを作成
    df = pd.DataFrame(columns=columns)

    # 追加するサンプルデータ
    sample_data = [
        ["アジア取手カントリークラブ", 8000, 11000, 4.0, "茨城県取手市稲１３４０", "10km以内", "https://search.gora.golf.rakuten.co.jp/cal/disp/c_id/120080"],
        ["千葉新日本ゴルフ倶楽部", 9000, 15000, 4.5, "千葉県市原市新巻850", "20km以内", "https://search.gora.golf.rakuten.co.jp/cal/disp/c_id/120080"]
    ]

    # サンプルデータをデータフレームに追加
    df = pd.DataFrame(sample_data, columns=columns)
    # タイトル行を追加
    df = pd.concat([pd.DataFrame([["**ゴルフコース名**", "**最低価格**", "**最高価格**", "**評価**", "**住所**", "**高速からの距離**", "**選択**"]], columns=df.columns), df], ignore_index=True)

    return df