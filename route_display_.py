import pandas as pd
import streamlit as st
from streamlit_folium import folium_map
import googlemaps as gmaps
from PIL import Image

def route_display(routes_overview,ic_list_df,highway_toll_List,total_cost,per_cost,total_highway_cost,fuel_cost):
  """
  ルートと費用情報をStreamlit上で表示

  Args:
    routes_overview: ルート概要情報（リスト）
    ic_list_df: IC情報を含むデータフレーム
    highway_toll_List: 高速料金情報（リストのリスト）
    total_cost: 総コスト
    per_cost: 一人あたりのコスト
    total_highway_cost: 高速金額
    fuel_cost: ガソリン代
  """

  # 出発地・目的地情報の取得
  start_location = routes_overview[0]['highway'][0][0]
  end_location = routes_overview[-1]['highway'][-1][1]

  # Google Maps APIキーの取得
  gmaps_key = st.secrets["google_maps_api_key"]

  # Google Mapsクライアントの作成
  gmaps_client = gmaps.Client(key=gmaps_key)

  # 出発地・目的地の緯度経度を取得
  start_latlng = gmaps_client.geocode(start_location).location
  end_latlng = gmaps_client.geocode(end_location).location

  # 地図を作成
  m = folium_map(location=start_latlng, zoom_start=10)

  # 出発地・目的地のマーカーを配置
  folium.Marker(start_latlng, popup=f"出発地: {start_location}").add_to(m)
  folium.Marker(end_latlng, popup=f"目的地: {end_location}").add_to(m)

  # ルートを表示
  for i in range(len(routes_overview)):
    highway = routes_overview[i]['highway']
    for j in range(len(highway) - 1):
      start_lat = highway[j][0][0]
      start_lng = highway[j][0][1]
      end_lat = highway[j][1][0]
      end_lng = highway[j][1][1]
      folium.PolyLine([(start_lat, start_lng), (end_lat, end_lng)], color='blue', weight=2, opacity=0.7).add_to(m)

  # 地図をStreamlitに表示
  st.write(m)

  # ルート詳細

  st.header("ルート詳細")
  for i, route in enumerate(routes_overview):
    st.write(f"{i + 1}区間目")
    st.write(f"  距離：{route['distance']} km")
    st.write(f"  時間：{route['time']}")
    st.write(f"  高速料金：{route['highway'][0][0]} - {route['highway'][-1][0]} = {route['highway'][-1][2]} 円")

  # 費用詳細

  st.header("費用詳細")
  st.write(f"  総コスト：{total_cost} 円")
  st.write(f"  一人あたり：{per_cost} 円")
  st.write(f"  高速料金：{total_highway_cost} 円")
  st.write(f"  ガソリン代：{fuel_cost} 円")