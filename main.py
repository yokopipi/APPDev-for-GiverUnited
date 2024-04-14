# サブモジュールをインポートする
# import

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
