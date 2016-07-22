# coding:utf-8
# try:
#     from gevent import monkey
#     monkey.patch_all()
#     from gevent.pool import Pool
# except:
#     from multiprocessing.dummy import Pool

import re
import requests
import glob
from SpiderModel import httpHelper
import json
'''
淘宝并行开太多会需要验证码，只要浏览器打完验证码，把cookies里的那句sec的放入header就可以跳过去了,目前测试Pool大小设定在5比较持久……但还是会要验证码，10以上都会要打验证码
'''

def get_taobao_ids(catid,pagenum):
    if pagenum==1:
        pagenum=1
    else:
        pagenum=(pagenum-1)*96
    while 1:
        try:
            # print pagenum
            url = 'http://list.taobao.com/itemlist/default.htm?_input_charset=utf-8&json=on&cat={0}&sort=biz30day&msp=1&as=1&viewIndex=1&atype=b&style=list&same_info=1&tid=0&isnew=2&pSize=96&data-key=s&data-value={1}&data-action&module=page&s=0'.format(
                catid, pagenum)
            html=httpHelper.GetHtml(url,'utf-8')
            obj=json.loads(html)
        except Exception as e:

            continue

get_taobao_ids(1,1)


    #     r = requests.get(url, headers=headers, proxies=proxies, timeout=5)
    #     ss = r.text
    #     ids = '\n'.join(re.findall('itemId":"(.*?)"', ss))
    #     print pagenum / 96, 'get'
    #     return ids
    # except Exception as e:
    #     print('retry fen')
    #     continue
