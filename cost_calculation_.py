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
#【返り値】
# ・総コスト：数字
# ・一人あたりのコスト：数字 
# ・高速金額：数字 
# ・ガソリン代：数字 
#############

def cost_calculation(highway_toll_List, price_per_liter, fuel_efficiency, cnt_people):
  """
  費用計算（cost_calculation）

  総距離と交通量情報、高速料金から交通費、1人あたりの交通費を算出する

  Args:
    highway_toll_List: 高速料金一覧（リストのリスト）
    price_per_liter: ガソリン代（1Lあたり）
    fuel_efficiency: 燃費（L/KM）
    cnt_people: 人数

  Returns:
    total_cost: 総コスト
    per_cost: 一人あたりのコスト
    total_highway_cost: 高速金額
    fuel_cost: ガソリン代
  """

  # # 高速料金の合計
  total_highway_cost = sum([toll[2] for toll in highway_toll_List])

  # # 総走行距離の計算
  total_distance = 0
  for i in range(len(highway_toll_List) - 1):
     total_distance += highway_toll_List[i][2]

  # # ガソリン代計算
  fuel_cost = int(total_distance) /int(fuel_efficiency) * int(price_per_liter) 

  # # 総コスト計算
  total_cost = total_highway_cost + fuel_cost

  # # 一人あたりのコスト計算
  per_cost = total_cost / cnt_people


  return total_cost, per_cost, total_highway_cost, fuel_cost