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
#############

def route_search(starting_point,first_person_address,second_person_address,third_person_address,destination,play_date,estimated_arrival_time):

    #経由情報（詳細） ※経由地はwaypointを1にする。有料区間は'tollsection'を1にする
    routes_details = [
        {'latitude': 35.6895, 'longitude': 139.6917, 'waypoint':1,'tollsection':0},
        {'latitude': 34.0522, 'longitude': -118.2437, 'waypoint':0,'tollsection':1},
        {'latitude': 34.0522, 'longitude': -118.2437, 'waypoint':0,'tollsection':1},
        {'latitude': 34.0522, 'longitude': -118.2437, 'waypoint':0,'tollsection':1},
        {'latitude': 51.5074, 'longitude': -0.1278, 'waypoint':1,'tollsection':0},
        {'latitude': 34.0522, 'longitude': -118.2437, 'waypoint':0,'tollsection':1},
        {'latitude': 34.0522, 'longitude': -118.2437, 'waypoint':0,'tollsection':1},
        {'latitude': 34.0522, 'longitude': -118.2437, 'waypoint':1,'tollsection':0},
     ]
    
    #経由情報（概要）
    routes_overview =[
        #Start⇒1人目の情報　※1人目が存在しない場合は、全てNULLにする
        {
            'time':'1:00', 
            'distance':5.5,
            'highway':[
                [['35.516139','139.591444'],['35.516139','139.591444']],
                [['35.627389','139.625778'],['35.647651','139.679167']],
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
                [['35.647651','139.679167'],["柏",'35.908708','139.934653']]
            ]
        },
        #3人目⇒到着地の情報　※到着値が入力されていないときは、全てNULLにする
        {
            'time':'0:20', 
            'distance':10,
            'highway':[]
        },
    ]

    return routes_overview,routes_details