# サブモジュールをインポートする
import golfcourse_search
import route_search
import highway_toll
import cost_calculation

import streamlit as st
import pandas as pd
import numpy as np

set_prefecture_list = {
    "東京都":1,
    "埼玉県":2
}

set_starttime_list = {
    "~5時台":1,
    "6時台":2,
    "7時台":3,
    "8時台":4,
    "9時台":5,
    "10時台":6,
    "11時台":7,
    "12時台~":8
}

tab1, tab2 = st.tabs(["main", "member"])

with tab1:
    st.title("ワイヤーフレーム")
    st.sidebar.write("＜対象ゴルフ場＞")
    st.sidebar.selectbox("月", np.arange(1,13))
    st.sidebar.selectbox("日", np.arange(1,32))
    st.sidebar.selectbox("日間", np.arange(1,32))

    st.sidebar.selectbox("エリア", set_prefecture_list.keys())
    st.sidebar.selectbox("スタート時間", set_starttime_list.keys())

    st.sidebar.button("検索")

    st.sidebar.text_input("ゴルフ場名検索")

    st.sidebar.button("検索２")

    st.sidebar.write("＜ピックアップ情報＞")
    st.sidebar.selectbox("出発地", set_prefecture_list.keys())
    st.sidebar.selectbox("1人目", set_prefecture_list.keys())
    st.sidebar.selectbox("2人目", set_prefecture_list.keys())
    st.sidebar.selectbox("3人目", set_prefecture_list.keys())

    st.sidebar.write("＜交通費情報＞")
    st.sidebar.text_input("燃費[L/km]")
    st.sidebar.text_input("ガソリン代[円]")

    df_Gcourse = pd.DataFrame(np.arange(12).reshape(3, 4))

    st.table(df_Gcourse)

    col1, col2 = st.columns(2)

    with col1:
        st.write("＜移動情報＞")
        st.write("出発")

        st.write("1人目")
        st.write("2人目")
        st.write("3人目")
        st.write("目的")

        st.write("総距離")
        st.write("総時間")

    with col2:
        st.write("＜交通費＞")
        st.write("高速料金")
        st.write("ガソリン代")
        st.write("1人あたり交通費")

with tab2:
    st.write("メンバー登録？")


#ゴルフ場検索--------------------------
###関数：ゴルフ場検索（golfcourse_search）をコールし、検索結果のゴルフ場一覧をデータフレームに格納する。

#エリア
area = ['東京都','千葉県']
#プレイ日
play_date = 2024/4/20
#最低金額
min_fee = 8000
#最高金額
max_fee = 12000
#スタート時間
start_times = ['7:00','8:00','9:00']

golfcourse_df = golfcourse_search(area,play_date,min_fee,max_fee,start_times)
#ゴルフ場検索--------------------------


#以下、ゴルフ指定がされた後の処理。

#ルート検索--------------------------
###関数：ルート検索（route_search）をコールし、ルート情報（概要）とルート情報（詳細）を格納する

#出発値
starting_point = '神奈川県横浜市都筑区新栄町15-1'
first_person_address = '東京都渋谷区道玄坂２丁目２９−１'
second_person_address = '東京都日野市大坂上４丁目１−１'
third_person_address = '千葉県柏市柏１丁目１−１'
destination = '茨城県取手市稲１３４０'
estimated_arrival_time = '7:00'

routes_overview,routes_details = route_search(starting_point,first_person_address,second_person_address,third_person_address,destination,estimated_arrival_time)
#ルート検索--------------------------



#高速料金計算--------------------------
###関数：高速料金計算（highway_toll）をコールし、高速料金を計算する
highway_List = [['都筑','港北'],['用賀','渋谷'],['渋谷','柏']]

highway_toll_List = highway_toll(highway_List)
#高速料金計算--------------------------


#交通費計算--------------------------
###関数：費用計算（cost_calculation）をコールし、総距離と交通量情報、高速料金から交通費、1人あたりの交通費を算出する

#ガソリン代（1Lあたり）
price_per_liter = 150

#燃費（L/KM）
fuel_efficiency = 23 

#人数
cnt_people = 3

total_cost,per_cost = cost_calculation(highway_toll_List,price_per_liter, fuel_efficiency,cnt_people)
#コスト計算--------------------------