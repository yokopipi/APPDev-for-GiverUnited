# サブモジュールをインポートする
from create_iclist_ import create_iclist
from golfcourse_search_ import golfcourse_search
from route_search_ import route_search
from highway_toll_ import highway_toll
from cost_calculation_ import cost_calculation
from route_display_ import route_display

import streamlit as st
import pandas as pd
import numpy as np
import datetime

# ページの設定：広いレイアウトを使用
st.set_page_config(layout="wide")

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



# サイドバー設定
with st.sidebar:
    st.markdown("**【ゴルフ場検索条件】:**")
    area = st.selectbox("エリア", set_prefecture_list.keys())
    # 今日の日付をデフォルト値として設定
    today = datetime.date.today()  # 今日の日付を取得
    play_date = st.date_input("プレー日", today)  # デフォルト値として今日の日付を使用
    min_fee = st.number_input("最低金額", value=8000)
    max_fee = st.number_input("最高金額", value=12000)
    start_times = st.selectbox("スタート時間", set_starttime_list.keys())
    if st.button("ゴルフ場検索"):
        # 検索実行
        golfcourse_df = golfcourse_search(area, play_date, min_fee, max_fee, start_times)
        # セッション状態に保存
        st.session_state.golfcourse_df = golfcourse_df

# メイン表示
if 'golfcourse_df' in st.session_state:
    st.markdown("**ゴルフコース一覧:**")

    for i, row in st.session_state.golfcourse_df.iterrows():
        # Markdownを使ってゴルフコース名をハイパーリンクとして表示
        link = f"[{row['golf_course_name']}]({row['url']})"
        cols = st.columns([2, 0.5, 0.5, 0.5, 2, 1, 0.5])
        cols[0].markdown(link, unsafe_allow_html=True)
        cols[1].write(row['min_price'])
        cols[2].write(row['max_price'])
        cols[3].write(row['rating'])
        cols[4].write(row['address'])
        cols[5].write(row['distance_from_highway'])
        
        # ボタンの配置
        if cols[6].button("選択", key=f"select_{i}"):
            st.session_state.selected_address = row['address']

    if 'selected_address' in st.session_state:
        st.write(f"Selected Address: {st.session_state.selected_address}")