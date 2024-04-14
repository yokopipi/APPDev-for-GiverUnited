import requests
import json
from datetime import datetime

dt = datetime(2024, 4, 15, 12, 30, 0)  #入力情報より持ってくる（到着時間）
unixtime = dt.timestamp() #UNIX時間に変換
print(unixtime)

# APIキー
API_KEY = 'your API key'
# リクエストURL
URL = 'https://maps.googleapis.com/maps/api/directions/json'

start = "町田駅" #入力情報より持ってくる
goal = "笠間カントリークラブ" #選択したゴルフ場情報より持ってくる
waypoint1 = "東京駅" #入力情報より持ってくる(1人目)
waypoint2 = "横浜駅" #入力情報より持ってくる(2人目)
waypoint3 = "水戸駅" #入力情報より持ってくる(3人目)

params = {
    'origin': start, #出発地
    'destination': goal, #目的地
    'waypoints': 'optimize:true|{}|{}|{}'.format(waypoint1, waypoint2, waypoint3), #経由地を"|"で区切る, optimize:trueとすることでルート最適化が有効となる。waypoint_orderで順番を返してくれる。
    'key': API_KEY,
    'arrival_time': unixtime #到着時間
}

# APIリクエストの送信
response = requests.get(URL, params=params)

# レスポンスの取得
data = response.json()

#print(json.dumps(data, ensure_ascii=False))

html_toll=[]
ic = []
ic_pairs = []
distance = []
duration = []
j = 1
route = []

route = data["routes"][0]["waypoint_order"]
route_kai = [f"{x + 1}人目" for x in route] 
print("ピックアップの順番：" + route_kai[0] + "→" + route_kai[1] + "→" + route_kai[2])

#各区間毎にループ処理
for legs in range(len(data["routes"][0]["legs"])):
    distance.append(data["routes"][0]["legs"][legs]["distance"]["text"])
    duration.append(data["routes"][0]["legs"][legs]["duration"]["text"])
#    print(legs)
    for i in range(len(data["routes"][0]["legs"][legs]["steps"])):
        html = data["routes"][0]["legs"][legs]["steps"][i]["html_instructions"]
        if "Toll" in html:
            html_toll.append(1)
        else:
            html_toll.append(0)
#    print(html_toll)

    #最初の要素が1の場合の処理
    if html_toll[0]==1:
        ic.append(data["routes"][0]["legs"][legs]["steps"][0]["end_location"])

    while j < len(html_toll):
        #有料区間1つのみ
        if html_toll[j] == 1 and (html_toll[j-1] == 0) and (html_toll[j+1] == 0):
            ic.append(data["routes"][0]["legs"][legs]["steps"][j]["start_location"])
            ic.append(data["routes"][0]["legs"][legs]["steps"][j]["end_location"])
            j += 2  
        #入口IC付近
        elif html_toll[j] - html_toll[j-1] == 1:
            ic.append(data["routes"][0]["legs"][legs]["steps"][j]["end_location"])
            j += 1 
        #出口IC付近
        elif html_toll[j] - html_toll[j-1] == -1:
            ic.append(data["routes"][0]["legs"][legs]["steps"][j]["start_location"])
            j += 1 
        #有料区間または一般道の継続
        elif html_toll[j] - html_toll[j-1] == 0:
            j += 1
    j = 1
#    print(ic)
    html_toll=[]

for i in range(0, len(ic), 2):
    pair = (ic[i], ic[i+1])
    ic_pairs.append(pair)

#入口IC、出口ICのペア
print(ic_pairs)
#各区間の距離
print(distance)
#各区間でかかる時間
print(duration)