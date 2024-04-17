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


##
columns = {0:'ic_name', 1:'latitude', 2:'longitude'}
ic_list_df = pd.read_csv("IC_list.csv", header=None)
ic_list_df.rename(columns=columns, inplace=True)

routes_overview =[
        #Start⇒1人目の情報　※1人目が存在しない場合は、全てNULLにする
        {
            'time':'1:00', 
            'distance':5.5,
            'highway':[
                # サンプル　岩槻→出流原
                [[35.94008341359999, 139.68642821481032],[36.366717621461305, 139.54766439501492]],
            ]
        },
        #1人目⇒2人目の情報　※2人目が存在しない場合は、全てNULLにする
        {
            'time':'0:10', 
            'distance':1.5,
            'highway':[]
        },
        #2人目⇒3人目の情報　※3人目が存在しない場合は、全てNULLにする
        {
            'time':'0:45', 
            'distance':100,
            'highway':[
                # サンプル　神田橋→谷田部
                [[35.68963925847578, 139.76431663106163],[36.0220312773855, 140.07615420908513]]
            ]
        },
        #3人目⇒到着地の情報　※到着値が入力されていないときは、全てNULLにする
        {
            'time':'0:20', 
            'distance':10,
            'highway':[
                # サンプル　浦安→茂原長南
                [[35.652513846314235, 139.9051748523011],[35.4057177657481, 140.25291602525198]],
                # サンプル　葛西→市原舞鶴
                [[35.64267684309367, 139.86712917897262],[35.356219750119195, 140.1778814526718]]
            ]
        },
    ]

print(highway_toll(routes_overview,ic_list_df))

##