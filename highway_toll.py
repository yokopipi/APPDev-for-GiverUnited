#############
#【関数名】
#高速料金計算（highway_toll）
#【処理内容】
#パラメータには高速IN/OUTの座標情報があるので、ICリストから最も近い座標のIC名称を取得する
#高速IN/OUT名が取得できたら、ドラぷらサイトのスクレイピングから高速料金を求め、リストに追加する。


#【パラメータ】
# ・ルートサマリ情報：リストのリスト ※リストの内容については、route_search.py参照
# ・ICリスト：データフレーム
#【返り値】
# ・高速乗降リスト（金額付）：リストのリスト
#############

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import datetime
import requests

def highway_toll(routes_overview,ic_list_df):
    # スクレイピングする先のドラぷらHPのURL
    REQUEST_URL = "https://www.driveplaza.com/dp/SearchQuick"

    # 時間情報
    dt = datetime.datetime.now()
    year = str(dt.year)
    month = str(dt.month)
    day = str(dt.day)

    # 出発/到着時間はルート検索側から持ってくればいいがとりあえず現在時刻で代替
    hour = str(dt.hour)
    minute = str(dt.minute) 

    # 高速料金情報を格納する配列を用意
    highway_toll_List = []

    # 無駄にfor分使ってしまったが、、サブモジュール中の関数の扱いわからんのでとりあえずこのまま
    for i in range(len(routes_overview)):
        for highway in routes_overview[i]['highway']:
            # 出発/到着IC名を取得
            ic_set = ["",""]
            for j in range(len(highway)):
                df_ic_temp = pd.DataFrame()
                df_ic_temp['d_lat'] = ic_list_df['latitude'].apply(lambda x: abs(x-highway[j][0]))
                df_ic_temp['d_long'] = ic_list_df['longitude'].apply(lambda x: abs(x-highway[j][1]))
                df_ic_temp['dist'] = (df_ic_temp['d_lat']**2 + df_ic_temp['d_long']**2)**0.5
                ic_set[j] = ic_list_df.loc[df_ic_temp['dist'].idxmin()]['ic_name']

            # 各高速区間に対して料金を取得し、リストに格納する。
            parameters = {
                'startPlaceKana': ic_set[0],
                'arrivePlaceKana': ic_set[1],
                'searchHour': hour,
                'searchMinute': minute,
                'kind': "1", # 今回は出発時で固定
                'carType': "1", # 今回は普通車で固定
                'priority': "2", # 今回はルート最適化のため時間順で固定
                'searchYear': year,
                'searchMonth': month,
                'searchDay': day,
                'selectickindflg': '0'
            }
            res = requests.get(REQUEST_URL, params=parameters)

            # こっからスクレイピング
            soup = BeautifulSoup(res.text, "html.parser")
            fee_etc = int(soup.find(id="fee_etc1").text.replace(",", "")) #ETC前提で料金取得
            highway_toll_List.append([ic_set[0], ic_set[1], fee_etc])

    # highway_toll_List =  [['都筑','港北',1000],['用賀','渋谷',500],['渋谷','柏',2000]]

    return  highway_toll_List

