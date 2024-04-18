#############
#【関数名】
#IC一覧作成（create_iclist）
#【処理内容】
#予めGoogleスプレッドシートに作っておいたICのリストをデータフレームにする。

#【パラメータ】
# ・なし
#【返り値】
# ・ICリスト：データフレーム
#############

def create_iclist():
    import pandas as pd

    file_path = 'IC_list.csv'
    # 空のデータフレームを定義するための列名
    columns = ['ic_name', 'latitude', 'longitude']

    # 空のデータフレームを作成
    df = pd.read_csv(file_path)


    # 追加するサンプルデータ
    # ic_data = [
    #     ["港北", '35.516139','139.591444'],
    #     ["都筑", '35.544167','139.603889'],
    #     ["柏",'35.908708','139.934653'],
    #     ["用賀",'35.627389','139.625778'],
    #     ["渋谷",'35.647651','139.679167']
    # ]
    # サンプルデータをデータフレームに追加
    # df = pd.DataFrame(ic_data, columns=columns)

    return df