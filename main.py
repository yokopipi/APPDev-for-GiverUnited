# サブモジュールをインポートする
from create_iclist import create_iclist
from golfcourse_search_ import golfcourse_search
from route_search import route_search
from highway_toll import highway_toll
from cost_calculation_ import cost_calculation
from route_display_ import route_display

import streamlit as st
import pandas as pd
import numpy as np
import datetime

# ページの設定：広いレイアウトを使用
st.set_page_config(layout="wide")

##関数：IC一覧作成（create_iclist）をコールして、IC一覧をデータフレームに格納する。
ic_list_df = create_iclist()

set_area_list = {
    "東京都":1,
    "埼玉県":2
}

set_friend_list = {
    "ダル君":1,
    "山本君":2,
    "大谷さん":3,
    "鈴木センパイ":4
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

set_address_list = {
    "東京都":1,
    "埼玉県":2
}

# サイドバー設定
with st.sidebar:
    st.markdown("**【ゴルフ場検索条件】**")
    area = st.selectbox("エリア", set_area_list.keys())
    # 今日の日付をデフォルト値として設定
    today = datetime.date.today()  # 今日の日付を取得
    play_date = str(st.date_input("プレー日", today))  # デフォルト値として今日の日付を使用
    min_fee = st.number_input("最低金額", value=8000,step=1000)
    max_fee = st.number_input("最高金額", value=12000,step=1000)
    start_times = st.selectbox("スタート時間", set_starttime_list.keys())
    if st.button("ゴルフ場検索"):
        # 検索実行
        golfcourse_df = golfcourse_search(area, play_date, min_fee, max_fee, start_times)
        # セッション状態に保存
        st.session_state.golfcourse_df = golfcourse_df
        st.session_state.selected_golf_course_name = ""
    if 'selected_golf_course_name' in st.session_state:
        st.text_input("ゴルフ場名",st.session_state.selected_golf_course_name)
    else:
        st.text_input("ゴルフ場名")
    st.markdown("**【ピックアップ情報】**")
    starting_point = st.text_input("出発地",'神奈川県横浜市都筑区新栄町15-1')
    st.selectbox("1人目", set_friend_list.keys())
    first_person_address = st.text_input("1人目住所",'東京都渋谷区道玄坂２丁目２９−１')
    st.selectbox("2人目", set_friend_list.keys())
    second_person_address = st.text_input("2人目住所",'東京都日野市大坂上４丁目１−１')
    st.selectbox("3人目", set_friend_list.keys())
    third_person_address = st.text_input("3人目住所",'千葉県柏市柏１丁目１−１')
    estimated_arrival_time = st.time_input("到着予定時間")

    st.markdown("**【交通費情報】**")
    price_per_liter = st.text_input("燃費[L/km]",14)
    fuel_efficiency = st.text_input("ガソリン代[円]",169)
    cnt_people = 3

# メイン表示
if 'golfcourse_df' in st.session_state:
    st.write("### ゴルフコース一覧:")  # タイトル行

    # ページネーションを設定
    page_size = 5
    total_pages = (len(st.session_state.golfcourse_df) + page_size - 1) // page_size
    page_number = st.number_input('ページ番号', min_value=1, max_value=total_pages, value=1, step=1) - 1
    start_index = page_number * page_size
    end_index = min(start_index + page_size, len(st.session_state.golfcourse_df))
    displayed_df = st.session_state.golfcourse_df.iloc[start_index:end_index]

    # タイトル行の常時表示
    title_row = st.session_state.golfcourse_df.iloc[0]
    title_cols = st.columns([2, 0.5, 0.5, 0.5, 2, 1, 0.5])
    title_cols[0].write('**ゴルフ場名**')
    title_cols[1].write('**最低価格**')
    title_cols[2].write('**最高価格**')
    title_cols[3].write('**評価**')
    title_cols[4].write('**住所**')
    title_cols[5].write('**高速からの距離**')

    for i, row in displayed_df.iterrows():
        index = start_index + i  # 元のデータフレームでのインデックス位置
        cols = st.columns([2, 0.5, 0.5, 0.5, 2, 1, 0.5])
        cols[0].markdown(f"**[{row['golf_course_name']}]({row['url']})**", unsafe_allow_html=True)
        cols[1].write(row['min_price'])
        cols[2].write(row['max_price'])
        cols[3].write(row['rating'])
        cols[4].write(row['address'])
        cols[5].write(row['distance_from_highway'])
        if cols[6].button("選択", key=f"select_{index}"):  # キーにインデックスを追加
            st.session_state.selected_address = row['address']
            st.session_state.selected_golf_course_name = row['golf_course_name']
    

    if 'selected_address' in st.session_state:
        destination = st.session_state.selected_address
        st.write("")
        st.markdown(f"##### 選択ゴルフコース　:　{st.session_state.selected_golf_course_name}")
        st.write("--------")

        ###関数：ルート検索（route_search）をコールし、ルート情報（概要）とルート情報（詳細）を格納する
        routes_overview,routes_details,total_time,total_distance= route_search(starting_point,first_person_address,second_person_address,third_person_address,destination,play_date,estimated_arrival_time)
        
        ###関数：高速料金計算（highway_toll）をコールし、高速料金を計算する
        highway_toll_List = highway_toll(routes_overview,ic_list_df)

        ###関数：費用計算（cost_calculation）をコールし、総距離と交通量情報、高速料金から交通費、1人あたりの交通費を算出する
        total_cost,per_cost,total_highway_cost,fuel_cost = cost_calculation(highway_toll_List,price_per_liter, fuel_efficiency,cnt_people)

        #結果表示
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**【移動情報】**")
            st.write("出発 　　　",routes_overview[0]['time'],"　　　　","")
            st.write("1人目　　　",routes_overview[1]['time'],"　　　　",routes_overview[0]['distance'])
            st.write("2人目　　　",routes_overview[2]['time'],"　　　　",routes_overview[1]['distance'])
            st.write("3人目　　　",routes_overview[3]['time'],"　　　　",routes_overview[2]['distance'])
            st.write("目的 　　　",estimated_arrival_time,"　　　　",routes_overview[3]['distance'])
            st.write("--------")
            st.write("総距離：",total_distance)
            st.write("総時間：",total_time)

        with col2:
            st.markdown("**【交通費】**")
            st.write("高速料金：",total_highway_cost) 
            st.write("ガソリン代:",fuel_cost)
            st.write("--------")
            st.write("交通費計：",total_cost,)
            st.write("1人あたり交通費:",per_cost)