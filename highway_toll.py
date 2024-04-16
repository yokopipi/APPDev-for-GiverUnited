#############
#【関数名】
#高速料金計算（highway_toll）
#【処理内容】
#パラメータには高速IN/OUTの座標情報があるので、ICリストから最も近い座標のIC名称を取得する
#高速IN/OUT名が取得できたら、ドラぷらサイトのスクレイピングから高速料金を求め、リストに追加する。


#【パラメータ】
# ・ルートサマリ情報：リストのリスト ※リストの内容については、route_search.py参照
# ・ICリスト：データフレーム
#【返り値】
# ・高速乗降リスト（金額付）：リストのリスト
#############

def highway_toll(routes_details,ic_list_df):

    highway_toll_List =  [['都筑','港北',1000],['用賀','渋谷',500],['渋谷','柏',2000]]

    return  highway_toll_List