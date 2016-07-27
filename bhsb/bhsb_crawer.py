#Python3.5
#liujian 2016.07.27
#coding=utf-8
import logging
import os
import sys
import time
from bs4 import BeautifulSoup
from common import http_helper
from common import down_helper
from common import mysql_helper

logging.basicConfig(level=logging.DEBUG)

# 连接数据库，创建engine全局对象
mysql_helper.create_engine("root","1234qwer","loseyou","127.0.0.1","3306")
_url="http://bohaishibei.com/post/{0}/"
_target_dir=os.path.join(os.path.dirname(sys.argv[0]),"img","{0}")
_category_id=0

def crawer_site():
    _real_url=_url.format(20510)
    _html=http_helper.get_html(_real_url,"utf=8")
    _soup=BeautifulSoup(''.join(_html),"html.parser")
    _get_data(_real_url,_soup)

def value_to_key(argument):
    switcher={
        "pics":1,
        "tuyue":1,
        "main":1,
        "videos":2,
        "digests":3
    }
    return switcher.get(argument,0)

def _get_data(real_url,soup):
    _href=soup.find("a",rel="category tag")["href"]
    _list_href= _href.split("/")
    _category=_list_href[5]
    if _category=="pics":
        _get_pics(real_url,soup)
    elif _category=="tuyue":
        _get_tuyue(real_url,soup)
    elif _category=="main":
        _get_main(real_url,soup)
    elif _category=="videos":
        _get_videos(real_url,soup)
    elif _category=="digests":
        _get_digest(real_url,soup)


# http://bohaishibei.com/post/category/pics/
# 分析图片分类，插入数据库
def _get_pics(real_url,soup):
    _category_id=1
    _main_name=soup.h1.get_text()
    _article = soup.find("article", "article-content")
    _list_p=_article.find_all("p");
    _content=_list_p[0].text
    _insert_mian_info = ("INSERT INTO ly_main_info(main_name,content,category_id,source_url,is_deleted,creation_time,creator_user_id)"
                         "VALUES ('{0}','{1}','{2}','{3}','{4}',now(),'{5}')")
    _insert_mian_info = _insert_mian_info.format(_main_name, _content, _category_id, real_url,0 , 1)
    _list_img=_list_p[1].find_all("img")
    with mysql_helper.transaction():
        _main_id=mysql_helper._insert(_insert_mian_info)
        for i in range(0,len(_list_img)):
            _href=_list_img[i].attrs["src"]
            _insert_pics=("INSERT INTO ly_pics(main_id,title,current_path,original_url,is_deleted,creation_time,creator_user_id)"
                          "VALUES ('{0}','{1}','{2}','{3}','{4}',now(),'{5}')")
            _insert_pics=_insert_pics.format(_main_id,"","",_href,0,1)
            mysql_helper._insert(_insert_pics)


# http://bohaishibei.com/post/category/tuyue/
def _get_tuyue(real_url,soup):
    _category_id=1
    _main_name = soup.h1.get_text()
    _article = soup.find("article", "article-content")
    _list_p=_article.find_all("p");
    _article_p_a=_list_p[0].find("a")
    _content=""
    if _article_p_a is None:
        _content=_list_p[0].text
        del _list_p[0]
    _insert_mian_info = ("INSERT INTO ly_main_info(main_name,content,category_id,source_url,is_deleted,creation_time,creator_user_id)"
        "VALUES ('{0}','{1}','{2}','{3}','{4}',now(),'{5}')")
    _insert_mian_info = _insert_mian_info.format(_main_name, _content, _category_id, real_url, 0, 1)
    with mysql_helper.transaction():
        _main_id=mysql_helper._insert(_insert_mian_info)
        for i in range(0,len(_list_p)-1):
            _img=_list_p[i].find("img")
            if _img is not None:
                _href=_img.attrs["src"]
                _insert_pics = ("INSERT INTO ly_pics(main_id,title,current_path,original_url,is_deleted,creation_time,creator_user_id)"
                    "VALUES ('{0}','{1}','{2}','{3}','{4}',now(),'{5}')")
                _insert_pics=_insert_pics.format(_main_id,"","",_href,0,1)
                mysql_helper._insert(_insert_pics)



# http://bohaishibei.com/post/category/main/
def _get_main(real_url,soup):
    _category_id=1
    _main_name = soup.h1.get_text()
    _article = soup.find("article", "article-content")
    _list_p=_article.find_all("p")
    _content = ""
    _insert_mian_info = ("INSERT INTO ly_main_info(main_name,content,category_id,source_url,is_deleted,creation_time,creator_user_id)"
        "VALUES ('{0}','{1}','{2}','{3}','{4}',now(),'{5}')")
    _insert_mian_info = _insert_mian_info.format(_main_name, "", _category_id, real_url, 0, 1)
    num=1
    while num<len(_list_p)-4:
        print(_list_p[num].string)
        num+=1
    # for i in range (1,len(_list_p)-4,2):
    #     print(i)
    #     print(_list_p[i].string)
    #     print(_list_p[i+1].find("img").attrs["src"])
    # return ""

# http://bohaishibei.com/post/category/videos/
def _get_videos(real_url,soup):
    _category_id=2
    return ""

# http://bohaishibei.com/post/category/digest/
def _get_digest(real_url,soup):
    _category_id=3
    return ""



if  __name__=="__main__":
    '''
    1. 如果模块是被导入，__name__的值为模块名字
    2. 如果模块是被直接执行，__name__的值为’__main__’
    # print(os.path.abspath(os.path.dirname(sys.argv[0])))
    # print(sys.argv[0])
    # print(os.path.dirname(sys.argv[0]))
    '''
    # print("2. 如果模块是被直接执行，__name__的值为’__main__’")
    crawer_site()

else:
    print("1. 如果模块是被导入，__name__的值为模块名字")
