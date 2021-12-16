import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from clickhouse_driver import Client

def read_sql_():

    client2 = Client(host='10.228.81.162', port='39014', user='default', database='zhiyi', password='xtxv%qD%')
    click_house = client2.execute("select * from zhiyi.l_taobao_item_test_test",types_check=True)
    col = client2.execute('DESCRIBE TABLE zhiyi.l_taobao_item_test_test')
    col2 = pd.DataFrame(col)
    aa = pd.Series(col2[0]).tolist()
    data1 = pd.DataFrame(click_house, columns=aa)
    data1 = data1[["item_id","title"]]
    return data1


print(read_sql_())
