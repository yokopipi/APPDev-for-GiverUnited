# サブモジュールをインポートする
from create_iclist import create_iclist
from golfcourse_search import golfcourse_search
from route_search import route_search
from highway_toll import highway_toll
from cost_calculation import cost_calculation


import streamlit as st
import pandas as pd
import numpy as np
import datetime
import streamlit as st
from streamlit_folium import st_folium 
import folium

# ページの設定：広いレイアウトを使用
st.set_page_config(layout="wide")

##関数：IC一覧作成（create_iclist）をコールして、IC一覧をデータフレームに格納する。
ic_list_df = create_iclist()

set_area_list = {
    "東京都":13,
    "埼玉県":11,
    "神奈川県":14,
    "千葉県":12,
    "山梨県":19,
    "栃木県":9,
    "群馬県":10,
    "茨城県":8
}

set_starttime_list = {
    "指定しない":0,
    "4時台":4,
    "5時台":5,
    "6時台":6,
    "7時台":7,
    "8時台":8,
    "9時台":9,
    "10時台":10,
    "11時台":11,
    "12時台":12,
    "13時台":13,
    "14時台":14,
    "15時台以降":15
}


# サイドバー設定
with st.sidebar:
    st.markdown("**【ゴルフ場検索条件】**")
    # エリア選択
    area_ = st.selectbox("エリア", set_area_list.keys())
    area = set_area_list[area_]

    # プレイ日選択
    today = datetime.date.today()  # 今日の日付をデフォルト値として設定
    play_date = str(st.date_input("プレー日", today))  # デフォルト値として今日の日付を使用
    input_date = datetime.datetime.strptime(play_date, "%Y-%m-%d").date()
    weekday = input_date.weekday()
    if weekday ==5 or weekday == 6:
        Holidayflg = 1
    else:
        Holidayflg = 0

    # プレイ料金選択
    if 'max_fee_setting' not in st.session_state:
        st.session_state.max_fee_setting = True
    if st.session_state.max_fee_setting:
        min_fee, max_fee = st.slider("プレー料金", 0, 25000, (0, 25000), 1000)
    else:
        min_fee = st.slider("プレー料金", 0, 25000, 0, 1000)
        max_fee = None
    st.session_state.max_fee_setting = st.checkbox('最高金額を指定する', True)

    # スタート時間選択
    start_times_ = st.selectbox("スタート時間", set_starttime_list.keys())
    start_times = set_starttime_list[start_times_]

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
    if 'df_members' not in st.session_state:
        columns = ["No", "名前", "住所"]
        df_members = pd.DataFrame(columns=columns)
        df_members.set_index("No", inplace=True)
        # デフォルト値
        df_members.loc[1] = ['ダル君', '東京都渋谷区道玄坂２丁目２９−１']
        df_members.loc[2] = ['山本君', '東京都日野市大坂上４丁目１−１']
        df_members.loc[3] = ['大谷さん', '千葉県柏市柏１丁目１−１']
        st.session_state.df_members = df_members
    if 'my_address' not in st.session_state:
        st.session_state.my_address = '神奈川県横浜市都筑区新栄町15-1'
    starting_point = st.session_state.my_address
    st.write("出発地")
    st.write(starting_point)
    first_person = st.selectbox("1人目", st.session_state.df_members['名前'])
    first_person_address = st.session_state.df_members[st.session_state.df_members['名前']==first_person].reset_index(drop=True).at[0,"住所"]
    st.write(first_person_address)
    second_person = st.selectbox("2人目", st.session_state.df_members['名前'])
    second_person_address = st.session_state.df_members[st.session_state.df_members['名前']==second_person].reset_index(drop=True).at[0,"住所"]
    st.write(second_person_address)
    third_person = st.selectbox("3人目", st.session_state.df_members['名前'])
    third_person_address = st.session_state.df_members[st.session_state.df_members['名前']==third_person].reset_index(drop=True).at[0,"住所"]
    st.write(third_person_address)
    estimated_arrival_time = st.time_input("到着予定時間")

    st.markdown("**【交通費情報】**")
    price_per_liter = st.text_input("燃費[km/L]",14)
    fuel_efficiency = st.text_input("ガソリン代[円]",169)
    cnt_people = 4

tab_main, tab_members = st.tabs(["メイン画面", "メンバー設定"])

# メイン表示
with tab_main:
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
        title_cols = st.columns([2, 2, 0.5, 2, 1, 0.5])
        title_cols[0].write('**ゴルフ場名**')
        title_cols[1].write('**最低価格**')
        title_cols[2].write('**評価**')
        title_cols[3].write('**住所**')
        title_cols[4].write('**高速からの距離**')

        for i, row in displayed_df.iterrows():
            index = start_index + i  # 元のデータフレームでのインデックス位置
            cols = st.columns([2, 2, 0.5, 2, 1, 0.5])
            cols[0].markdown(f"**[{row['golf_course_name']}]({row['url']})**", unsafe_allow_html=True)
            if Holidayflg == 1:
                cols[1].write(row['min_price_Holiday'])
            else:
                cols[1].write(row['min_price_Weekday'])
            cols[2].write(str(row['rating']))
            cols[3].write(row['address'])
            cols[4].write(row['distance_from_highway'])
            if cols[5].button("選択", key=f"select_{index}"):  # キーにインデックスを追加
                st.session_state.selected_address = row['address']
                st.session_state.selected_golf_course_name = row['golf_course_name']
        

        if 'selected_address' in st.session_state:
            destination = st.session_state.selected_address
            st.write("")
            st.markdown(f"##### 選択ゴルフコース　:　{st.session_state.selected_golf_course_name}")
            st.write("--------")

            ###関数：ルート検索（route_search）をコールし、ルート情報（概要）とルート情報（詳細）を格納する
            routes_overview,routes_details,total_time,total_distance,arrival_time,waypoint_list= route_search(starting_point,first_person_address,second_person_address,third_person_address,destination,play_date,estimated_arrival_time)
            print("ルート概要",routes_overview)
            print("ルート詳細",routes_details)
            print("合計時間", total_time)
            print("合計距離", total_distance)
            ###関数：高速料金計算（highway_toll）をコールし、高速料金を計算する
            highway_toll_List = highway_toll(routes_overview,ic_list_df)

            ###関数：費用計算（cost_calculation）をコールし、総距離と交通量情報、高速料金から交通費、1人あたりの交通費を算出する
            total_cost,per_cost,total_highway_cost,fuel_cost = cost_calculation(highway_toll_List,price_per_liter, fuel_efficiency,cnt_people)

            #結果表示
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**【移動情報】**")
                title_route_cols = st.columns([3,1,1])
                title_route_cols[0].write('＜経路＞')
                title_route_cols[1].write('＜時刻＞')
                title_route_cols[2].write('＜距離＞')
                route_cols = st.columns([3,1,1])
                route_cols[0].write("出発地(" + starting_point + ")")
                route_cols[1].write(routes_overview[0]["time"])
                route_cols[2].write("ー")
                for i in range(len(routes_overview)-1):
    #                route_cols[0].write(f"{i+1}人目")
                    route_cols[0].write(waypoint_list[i])
                    route_cols[1].write(routes_overview[i+1]["time"])
                    route_cols[2].write(str(routes_overview[i]["distance"])+" km")
                route_cols[0].write("目的地")
                route_cols[1].write(arrival_time)
                route_cols[2].write(str(routes_overview[-1]["distance"])+" km")
                route_cols[0].write("**合計**")
                route_cols[1].write(f"**{total_time}**")
                route_cols[2].write(str( "**{:.1f}**".format(total_distance))+" km")
        
            with col2:
                st.markdown("**【交通費】**")
                price_cols = st.columns([2, 1, 3])
                price_cols[0].write("高速料金:")
                price_cols[1].write(str(total_highway_cost))
                price_cols[2].write("円")
                price_cols[0].write("ガソリン代:")
                price_cols[1].write(str(int(fuel_cost)))
                price_cols[2].write("円")
                price_cols[0].write("交通費合計:")
                price_cols[1].write(str(int(total_cost)))
                price_cols[2].write("円")
                price_cols[0].write("1人当たり交通費:")
                price_cols[1].write(str(int(round(per_cost, -2))))
                price_cols[2].write("円/人")

            map = folium.Map(location=[35.5378631,139.5951104], zoom_start=10)

            line_points = list()
            for point in routes_details:
                line_points.append([point["lat"], point["lng"]])
                if point["waypoint"] == 1:
                    icon = folium.Icon(color="red")  # 赤色のアイコン
                    folium.Marker(location=[point["lat"], point["lng"]], icon=icon).add_to(map)
                else:
                    folium.CircleMarker(location=[point["lat"], point["lng"]], radius=1, color="blue", fill=True, fill_color="blue").add_to(map)
            folium.PolyLine(locations=line_points, color="gray", weight=2.5, opacity=0.8).add_to(map)
            st_folium(map, width = 1000, height = 500)
    else:
        st.write(f"## ピックアップルート検索アプリ")
        st.image("teamflag.png")

with tab_members:
    st.markdown(f"##### メンバー情報　:")

    with st.form("my address"):
        my_address = st.text_input(f"##### 出発地住所", '神奈川県横浜市都筑区新栄町15-1')
        ma_submitted = st.form_submit_button("登録")
    
    if ma_submitted:
        st.session_state.my_address = my_address

    # 登録フォーム
    with st.popover(f"## ゴルフ仲間登録フォーム"):
        with st.form("my form", clear_on_submit=True):
            name = st.text_input("名前")
            address = st.text_input("住所")
            submitted = st.form_submit_button("登録")

    if submitted:
        st.session_state.df_members.loc[len(st.session_state.df_members)+1] = [name, address]

    st.write(f"##### ゴルフ仲間")
    st.dataframe(st.session_state.df_members)