#Python3.5
#liujian 2016.04.12
#coding=utf-8

import urllib.request
import gzip

#获取指定url内容，并返回指定编码内容
def get_html(url,coding):
    #返回页面内容
    header_dict = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
    req =urllib.request.Request(url=url, headers=header_dict)
    doc=urllib.request.urlopen(req,timeout=1200).read()
    #解码
    try:
        html=gzip.decompress(doc).decode(coding,"ignore")
    except:
        html=doc.decode(coding,"ignore")
    #返回html
    return html