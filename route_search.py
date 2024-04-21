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
    print(estimated_arrival_time)
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
    waypoint_order = data["routes"][0]["waypoint_order"]
    waypoint_order_address = [first_person_address, second_person_address, third_person_address]
    waypoint_list = [waypoint_order_address[i] for i in waypoint_order]

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
        start_start_location = data["routes"][0]["legs"][leg]["steps"][0]["start_location"].copy()
        #スタート地点だから経由地
        waypoint = 1
        #tollか否かを判断した結果をhtml_tollに格納している。スタート地点だから0番目の要素を取得
        tollsection = html_toll[0]

        # 新しいデータを辞書に追加
        start_start_location['waypoint'] = waypoint
        start_start_location['tollsection'] = tollsection
    
        routes_details_factors.append(start_start_location)

        #スタート地点の緯度経度情報の取得（終わり）
        start_end_location = data["routes"][0]["legs"][leg]["steps"][0]["end_location"].copy()
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
    #リストの要素を逆にする
    times_list_reversed = list(reversed(times_list))
    # 到着時間から秒を削除する
    arrival_time = datetime.strptime(str(estimated_arrival_time), '%H:%M:%S').strftime('%H:%M')
    # 到着時間を時間と分に分解する
    arrival_hours, arrival_minutes = map(int, arrival_time.split(':'))

    dep_time=[]
    carry_over = 0  # 時間の繰り上がりを追跡するための変数

    for time_str in range(len(times_list_reversed)):
        # 目標時間を時間と分に分解する
        time_hours, time_minutes = map(int, times_list_reversed[time_str].split(':'))
        # １回目のループ処理では到着時間から１つ前の地点からの所要時間を引く
        if time_str == 0:
            result_hours = arrival_hours - time_hours
            result_minutes = arrival_minutes - time_minutes    

            # 分が負の場合、時間を減らして正の分に変換する
            if result_minutes < 0:
                result_hours -= 1
                result_minutes += 60

            # 時間が負の場合、24時間を加えて正の時間に変換する
            if result_hours < 0:
                result_hours += 24
                carry_over -= 1  # 繰り下がりを記録

        else:
            result_hours = result_hours - time_hours + carry_over
            result_minutes = result_minutes - time_minutes    

            # 分が負の場合、時間を減らして正の分に変換する
            if result_minutes < 0:
                result_hours -= 1
                result_minutes += 60

            # 時間が負の場合、24時間を加えて正の時間に変換する
            if result_hours < 0:
                result_hours += 24
                carry_over -= 1  # 繰り下がりを記録

        # 結果を文字列に整形する
        result_str = "{:02d}:{:02d}".format(result_hours, result_minutes)
        dep_time.append(result_str)
        print(dep_time)

    #総時間の算出
    dep_hours, dep_minutes = map(int, dep_time[-1].split(':'))
    total_hours = arrival_hours - dep_hours
    total_minutes = arrival_minutes - dep_minutes
    if total_minutes < 0:
        total_hours -= 1
        total_minutes += 60
    if total_hours < 0:
         total_hours += 24
         
    total_time = "{:02d}時間{:02d}分".format(total_hours, total_minutes)

    #総距離の算出
    total_distance = sum(distances_list)

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
#            'time':times_list[0], 
            'time':dep_time[0],
            'distance':distances_list[0],
            'highway':summary_ic_list[0]
        }
        ]

    elif len(data["routes"][0]["legs"]) == 2:
        routes_overview = [
        {
#            'time':times_list[0], 
            'time':dep_time[1],
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
#            'time':times_list[1], 
            'time':dep_time[0],
            'distance':distances_list[1],
            'highway':summary_ic_list[1]
        }
        ]

    elif len(data["routes"][0]["legs"]) == 3:
        routes_overview = [
        {
#            'time':times_list[0], 
            'time':dep_time[2],
            'distance':distances_list[0],
            'highway':summary_ic_list[0]
        },

        {
#            'time':times_list[1], 
            'time':dep_time[1],
            'distance':distances_list[1],
            'highway':summary_ic_list[1]
        },

        {
            'time':None, 
            'distance':None,
            'highway':None
        },

        {
#            'time':times_list[2], 
            'time':dep_time[0],
            'distance':distances_list[2],
            'highway':summary_ic_list[2]
        }
        ]

    elif len(data["routes"][0]["legs"]) == 4:
        routes_overview = [
        {
#            'time':times_list[0], 
            'time':dep_time[3],
            'distance':distances_list[0],
            'highway':summary_ic_list[0]
        },

        {
#            'time':times_list[1], 
            'time':dep_time[2],
            'distance':distances_list[1],
            'highway':summary_ic_list[1]
        },

        {
#            'time':times_list[2], 
            'time':dep_time[1],
            'distance':distances_list[2],
            'highway':summary_ic_list[2]
        },

        {
#            'time':times_list[3], 
            'time':dep_time[0],
            'distance':distances_list[3],
            'highway':summary_ic_list[3]
        }
        ]


    return routes_overview,routes_details,total_time,total_distance,arrival_time,waypoint_list