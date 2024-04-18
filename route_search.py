#############
#【関数名】
#ルート検索（route_search）
#【処理内容】
#GoogleAPIを利用してルート情報を作成する。

#【パラメータ】
# ・出発点：文字列
# ・１人目住所：文字列
# ・２人目住所：文字列
# ・３人目住所：文字列
# ・目的地：文字列
# ・プレイ日：文字列
# ・到着予定時刻：文字列
#【返り値】
# ・経由情報（概要）：辞書のリスト  
# ・経由情報（詳細）：辞書のリスト
# ・総時間：文字列
# ・総距離：数字
#############
import requests
import json
from datetime import datetime

def route_search(starting_point,first_person_address,second_person_address,third_person_address,destination,play_date,estimated_arrival_time):
    print(play_date)
    play_date = datetime.strptime(play_date, "%Y-%m-%d")
    # 日付と時刻を結合して一つの文字列にする
    combined_datetime_str = play_date.strftime("%Y-%m-%d") + ' ' + estimated_arrival_time.strftime("%H:%M:%S") 
    # 文字列を datetime オブジェクトに変換する
    combined_datetime = datetime.strptime(combined_datetime_str, '%Y-%m-%d %H:%M:%S')
    # Unix時間に変換
    unixtime = int(combined_datetime.timestamp())

    # APIキー
    API_KEY = 'AIzaSyD_0D80nd7tu68Ah7nIBjfK7vbyHPfpl9E'
    # リクエストURL
    URL = 'https://maps.googleapis.com/maps/api/directions/json'

    params = {
        'origin': starting_point, #出発地
        'destination': destination, #目的地
        'waypoints': 'optimize:true|{}|{}|{}'.format(first_person_address, second_person_address, third_person_address), #経由地を"|"で区切る, optimize:trueとすることでルート最適化が有効となる。waypoint_orderで順番を返してくれる。
        'key': API_KEY,
        'arrival_time': unixtime #到着時間
    }

    # APIリクエストの送信
    response = requests.get(URL, params=params)

    # レスポンスの取得
    data = response.json()

    #データ処理
    distance = []
    durations = []
    routes_details_factors=[]
    html_toll = []
    ic = []
    toll_flag = []

    for leg in range(len(data["routes"][0]["legs"])):
        distance.append(data["routes"][0]["legs"][leg]["distance"]["text"])
        durations.append(data["routes"][0]["legs"][leg]["duration"]["text"])
        if leg > 0:
            routes_details_factors.pop()
        for i in range(len(data["routes"][0]["legs"][leg]["steps"])):
            html = data["routes"][0]["legs"][leg]["steps"][i]["html_instructions"]
            if "Toll" in html:
                html_toll.append(1)
            else:
                html_toll.append(0)

        #各区間のhtml_tollリストをtoll_listに追加 
        toll_flag.append(html_toll)

        #スタート地点の緯度経度情報の取得（始まり）
        start_start_location = data["routes"][0]["legs"][0]["steps"][0]["start_location"].copy()
        #スター地点だから経由地
        waypoint = 1
        #tollか否かを判断した結果をhtml_tollに格納している。スタート地点だから0番目の要素を取得
        tollsection = html_toll[0]

        # 新しいデータを辞書に追加
        start_start_location['waypoint'] = waypoint
        start_start_location['tollsection'] = tollsection
    
        routes_details_factors.append(start_start_location)

        #スタート地点の緯度経度情報の取得（終わり）
        start_end_location = data["routes"][0]["legs"][0]["steps"][0]["end_location"].copy()
        #スター地点だから経由地
        waypoint = 0
        #tollか否かを判断した結果をhtml_tollに格納している。スタート地点だから0番目の要素を取得
        tollsection = html_toll[0]
        # 新しいデータを辞書に追加
        start_end_location['waypoint'] = waypoint
        start_end_location['tollsection'] = tollsection

        routes_details_factors.append(start_end_location)

        #"steps"の数だけ繰り返し
        for step in range(1, len(data["routes"][0]["legs"][leg]["steps"])):
            location_data = data["routes"][0]["legs"][leg]["steps"][step]["end_location"].copy()
            waypoint = 0
            tollsection = html_toll[step]

            location_data['waypoint'] = waypoint
            location_data['tollsection'] = tollsection

            routes_details_factors.append(location_data)
        html_toll = []

    routes_details_factors[-1]['waypoint'] = 1

    #経由情報（詳細） ※経由地はwaypointを1にする。有料区間は'tollsection'を1にする
    routes_details = routes_details_factors

    #区間ごとのIC取得
    j = 1
    pre_ic_list = []

    for i in range(len(toll_flag)):
        #最初の要素が1の場合の処理
        if toll_flag[i][0]==1:
            ic.append(data["routes"][0]["legs"][leg]["steps"][0]["end_location"])

        while j < len(toll_flag[i]):
            #有料区間1つのみ
            if toll_flag[i][j] == 1 and (toll_flag[i][j-1] == 0) and (toll_flag[i][j+1] == 0):
                ic.append(data["routes"][0]["legs"][i]["steps"][j]["start_location"])
                ic.append(data["routes"][0]["legs"][i]["steps"][j]["end_location"])
                j += 2  
            #入口IC付近
            elif toll_flag[i][j] - toll_flag[i][j-1] == 1:
                ic.append(data["routes"][0]["legs"][i]["steps"][j]["end_location"])
                j += 1 
            #出口IC付近
            elif toll_flag[i][j] - toll_flag[i][j-1] == -1:
                ic.append(data["routes"][0]["legs"][i]["steps"][j]["start_location"])
                j += 1 
            #有料区間または一般道の継続
            elif toll_flag[i][j] - toll_flag[i][j-1] == 0:
                j += 1
        pre_ic_list.append(ic)
        ic = []
        j = 1

    ic_list = [[list(pair.values()) for pair in pair_list] if pair_list else [] for pair_list in pre_ic_list]
    summary_ic_list = []
    for sublist in ic_list:
        paired_sublist = []
        for i in range(0, len(sublist), 2):
            paired_sublist.append([sublist[i], sublist[i+1]])
        summary_ic_list.append(paired_sublist)

    distances_list = [float(distances.split(' ')[0]) for distances in distance]

    # 時間表記を変換する関数
    def convert_time(duration):
        hours = 0
        mins = 0

        # ' hours' および ' hour' を ':' に置き換えて時間と分を取得
        if ' hour' in duration:
            hours = int(duration.split(' hour')[0])
            duration = duration.replace(' hour', '')
        
        # ' mins' および ' min' を取り除いて分を取得
        if ' min' in duration:
            mins = int(duration.split(' min')[0].split()[-1])

        # 時間と分を文字列に変換して ':' で結合し、ゼロ埋めを行う
        return f'{hours:0>2}:{mins:0>02}'  # 分の部分には2桁のゼロ埋めを行う

    # 時間表記のリストを変換
    times_list = [convert_time(duration) for duration in durations]
    
    #経由情報（概要）
    if len(data["routes"][0]["legs"]) == 1:
        routes_overview = [
        {
            'time':None, 
            'distance':None,
            'highway':None
        },

        {
            'time':None, 
            'distance':None,
            'highway':None
        },

        {
            'time':None, 
            'distance':None,
            'highway':None
        },

        {
            'time':times_list[0], 
            'distance':distances_list[0],
            'highway':summary_ic_list[0]
        }
        ]

    elif len(data["routes"][0]["legs"]) == 2:
        routes_overview = [
        {
            'time':times_list[0], 
            'distance':distances_list[0],
            'highway':summary_ic_list[0]
        },

        {
            'time':None, 
            'distance':None,
            'highway':None
        },

        {
            'time':None, 
            'distance':None,
            'highway':None
        },

        {
            'time':times_list[1], 
            'distance':distances_list[1],
            'highway':summary_ic_list[1]
        }
        ]

    elif len(data["routes"][0]["legs"]) == 3:
        routes_overview = [
        {
            'time':times_list[0], 
            'distance':distances_list[0],
            'highway':summary_ic_list[0]
        },

        {
            'time':times_list[1], 
            'distance':distances_list[1],
            'highway':summary_ic_list[1]
        },

        {
            'time':None, 
            'distance':None,
            'highway':None
        },

        {
            'time':times_list[2], 
            'distance':distances_list[2],
            'highway':summary_ic_list[2]
        }
        ]

    elif len(data["routes"][0]["legs"]) == 4:
        routes_overview = [
        {
            'time':times_list[0], 
            'distance':distances_list[0],
            'highway':summary_ic_list[0]
        },

        {
            'time':times_list[1], 
            'distance':distances_list[1],
            'highway':summary_ic_list[1]
        },

        {
            'time':times_list[2], 
            'distance':distances_list[2],
            'highway':summary_ic_list[2]
        },

        {
            'time':times_list[3], 
            'distance':distances_list[3],
            'highway':summary_ic_list[3]
        }
        ]

    total_time = '3:00'
    total_distance = '120'

    return routes_overview,routes_details,total_time,total_distance
