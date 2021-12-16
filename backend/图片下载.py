#encoding:utf-8
"""
@project=企查查
@file=图片下载
@author=hjfan
@create_time:2021/8/25 14:19
"""

import re
import warnings
import pandas as pd
import requests
import multiprocessing
from clickhouse_driver import Client

warnings.filterwarnings("ignore")



def write_queue(queue):
    # client2 = Client(host='10.228.81.162', port='39013', user='default', database='dm', password='xtxv%qD%')
    #
    # click_house = client2.execute("select distinct (item_id),image_4 from l_taobao_item where create_time>'2021-01-01'", types_check=True)
    # col = client2.execute('DESCRIBE TABLE dws.dws_brain_goods_by_live')
    # col2 = pd.DataFrame(col)
    # aa = pd.Series(col2[0]).tolist()
    # data = pd.DataFrame(click_house, columns=aa)
    data = pd.read_parquet('download_picture_image3.parquet')
    # data = pd.read_excel('sky_cat_update.xlsx')
    # data = data.dropna()

    ## 循环写入数据，读取分词结果数据
    # data = pd.read_parquet("f_topic.parquet")
    # data = pd.read_sql("select * from f_topic_title_top_zengliang_xueli_0801",read_fandan_mysql_zhengshi())
    # sql = 'select * from test.weibo_red_words'
    # data = pd.read_sql(sql,engine1)
    #data = pd.read_excel(r'wan_red_content2.xlsx')
    ##将DataFrame数据转化为列表，方便下边循环和赋新列
    data_list = [data.ix[i].to_dict() for i in data.index.values]
    for i in data_list:
        if queue.full():
            print("队列已满!")
        queue.put(i)


import redis
def read_queue(queue, pid):
    ##读取类别词库
    # 循环读取队列消息
    # count = 1
    redis_pool = redis.ConnectionPool(host='10.228.83.123', port=6379, decode_responses=True)
    redis_conn = redis.Redis(connection_pool=redis_pool)
    data_set_name = "download_pid_redis_image3"
    data_list1 = []
    while True:


        i = queue.get()
        data_frame_name = str(i)
        # 判断是否重复
        if redis_conn.sismember(data_set_name, data_frame_name):
            pass
        else:
            data_list1.append(data_frame_name)
            redis_conn.sadd(data_set_name, data_frame_name)

        b = str(i['item_id'])
        # c = str(i["month_id"])

        re_images = re.sub('https:|http:','',i['image_3'])
        r = requests.get('http:' + re_images)
        aa_code = r.status_code
        print(aa_code)
        path = "/home/bi/fandan_predict/download_pic/pic_down_image3/"+b+'_3'+'.jpg'
        with open(path, 'wb') as f:
            f.write(r.content)
            f.close()



if __name__ == '__main__':
    queue = multiprocessing.Queue(200)
    p1 = multiprocessing.Process(target=write_queue, args=(queue,))
    # 等待p1写数据进程执行结束后，再往下执行
    p2 = multiprocessing.Process(target=read_queue, args=(queue, 1))
    p3 = multiprocessing.Process(target=read_queue, args=(queue, 2))
    p4 = multiprocessing.Process(target=read_queue, args=(queue, 3))
    p5 = multiprocessing.Process(target=read_queue, args=(queue, 4))
    p6 = multiprocessing.Process(target=read_queue, args=(queue, 5))
    p7 = multiprocessing.Process(target=read_queue, args=(queue, 6))
    p8 = multiprocessing.Process(target=read_queue, args=(queue, 7))
    p9 = multiprocessing.Process(target=read_queue, args=(queue, 8))
    p10 = multiprocessing.Process(target=read_queue, args=(queue, 9))
    p11 = multiprocessing.Process(target=read_queue, args=(queue, 10))
    p12 = multiprocessing.Process(target=read_queue, args=(queue, 11))
    p13 = multiprocessing.Process(target=read_queue, args=(queue, 12))
    p14 = multiprocessing.Process(target=read_queue, args=(queue, 13))
    p15 = multiprocessing.Process(target=read_queue, args=(queue, 14))
    p16 = multiprocessing.Process(target=read_queue, args=(queue, 15))
    p17 = multiprocessing.Process(target=read_queue, args=(queue, 16))
    p18 = multiprocessing.Process(target=read_queue, args=(queue, 17))
    p19 = multiprocessing.Process(target=read_queue, args=(queue, 18))
    p20 = multiprocessing.Process(target=read_queue, args=(queue, 19))
    p21 = multiprocessing.Process(target=read_queue, args=(queue, 20))
    p22 = multiprocessing.Process(target=read_queue, args=(queue, 21))
    p23 = multiprocessing.Process(target=read_queue, args=(queue, 22))
    p24 = multiprocessing.Process(target=read_queue, args=(queue, 23))
    p25 = multiprocessing.Process(target=read_queue, args=(queue, 24))
    #
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()
    p8.start()
    p9.start()
    p10.start()
    p11.start()
    p12.start()
    p13.start()
    p14.start()
    p15.start()
    p16.start()
    p17.start()
    p18.start()
    p19.start()
    p20.start()
    p21.start()
    p22.start()
    p23.start()
    p24.start()
    p25.start()


    p1.join()
    p2.join()
    p3.join()
    print("=============")
    p4.join()
    p5.join()
    p6.join()
    p7.join()
    p8.join()
    p9.join()
    p10.join()
    p11.join()
    p12.join()
    p13.join()
    p14.join()
    p15.join()
    p16.join()
    p17.join()
    p18.join()
    p19.join()
    p20.join()
    p21.join()
    p22.join()
    p23.join()
    p24.join()
    p25.join()



# import pandas as pd
# from clickhouse_driver import Client
#
# client2 = Client(host='10.228.81.162', port='39014', user='default', database='zhiyi', password='xtxv%qD%')
#
# click_house = client2.execute("select distinct (item_id),image_4 from l_taobao_item where create_time>'2021-01-01'", types_check=True)
# col = client2.execute('DESCRIBE TABLE zhiyi.l_taobao_item')
# col2 = pd.DataFrame(col)

# col2 = pd.DataFrame(col)

# aa = pd.Series(col2[0]).tolist()pd.Series(col2[0]).tolist()
# data = pd.DataFrame(click_house, columns=aa)
# print(data)