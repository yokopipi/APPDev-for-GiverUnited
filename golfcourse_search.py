#############
#【関数名】
#ゴルフ場検索（golfcourse_search）
#【処理内容】
#楽天GORAのAPIを利用して検索結果となるゴルフ場一覧を作成する。

#【パラメータ】
# ・エリア：文字列[リスト]
# ・プレー日：日付
# ・プレー料金（最低値）：数字
# ・プレー料金（最高値）：数字
# ・スタート時間：文字列[リスト]
#【返り値】
# ・ゴルフ場一覧：データフレーム
#############
import requests
import pandas as pd

def fetch_golf_course_details(golf_course_id, api_key):
    detail_url = "https://app.rakuten.co.jp/services/api/Gora/GoraGolfCourseDetail/20131113"
    detail_params = {
        "applicationId": api_key,
        "golfCourseId": golf_course_id,
        "format": "json"
    }
    response = requests.get(detail_url, params=detail_params)
    return response.json()


def golfcourse_search(area,play_date,min_fee,max_fee,start_times):

    api_key = '1011509919335500197' 
    url = "https://app.rakuten.co.jp/services/api/Gora/GoraPlanSearch/20170623"
    params = {
        "applicationId": api_key,
        "areaCode": area,
        "format": "json",
        "playDate": play_date,
        "minPrice": int(min_fee),
        "maxPrice": int(max_fee),
        "startTimeZone":start_times
    }

    # APIを呼び出して結果を表示
    response = requests.get(url, params=params)
    results = response.json()
 

    gora_data = []
    for item in results['Items']:
        golf_course_id = item['Item']['golfCourseId']
        details = fetch_golf_course_details(golf_course_id, api_key)
    
        selected_data = {
            'golf_course_name':item['Item']['golfCourseName'],
            'min_price_Weekday':item['Item']['displayWeekdayMinPrice'],
            'min_price_Holiday':item['Item']['displayHolidayMinPrice'],
            'rating':item['Item']['evaluation'],
            'address':details['Item']['address'],
            'distance_from_highway':item['Item']['icDistance'],
            'url':item['Item']['reserveCalUrlPC']
            
        }
        gora_data.append(selected_data)

    df = pd.DataFrame(gora_data)
   
    return df