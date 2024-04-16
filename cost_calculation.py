#############
#【関数名】
#費用計算（cost_calculation）総距離と交通量情報、高速料金から交通費、1人あたりの交通費を算出する
#【処理内容】
#交通費の算出と割り勘計算の実施。

#【パラメータ】
# ・高速料金一覧：リストのリスト
# ・ガソリン代（1Lあたり）：数字
# ・燃費（L/KM）：数字
# ・人数：数字
# ・経由情報（概要）：辞書のリスト  
#【返り値】
# ・総コスト：数字
# ・一人あたりのコスト：数字 
# ・高速金額：数字 
# ・ガソリン代：数字 
# ・総時間：文字列
# ・総距離：数字
#############

def cost_calculation(highway_toll_List,price_per_liter, fuel_efficiency,cnt_people,routes_overview):
    total_cost = 4000
    per_cost = 1333
    total_highway_cost = 2000
    fuel_cost = 2000
    total_time = '2:00'
    total_distance = 120

    return total_cost,per_cost,total_highway_cost,fuel_cost,total_time,total_distance