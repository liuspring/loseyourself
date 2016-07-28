# Python3.5
# liujian 2016.07.27
# coding=utf-8
import html
import logging
import os
import sys
import time
from bs4 import BeautifulSoup
from common import http_helper
from common import down_helper
from common import mysql_helper

logging.basicConfig(level=logging.DEBUG)

_url = "http://bohaishibei.com/post/{0}/"
_target_dir = os.path.join(os.path.dirname(sys.argv[0]), "img", "{0}")
_category_id = 0


def crawer_site():
    _less_num=0 #遍历50次都没有详情页分析则认为遍历结束
    _start_num=14
    while _less_num<50:
        # 连接数据库，创建engine全局对象
        mysql_helper.create_engine("root", "1234qwer", "loseyou", "127.0.0.1", "3306")
        _less_num+=1
        _real_url = _url.format(_start_num)
        _html = http_helper.get_html(_real_url, "utf=8")
        _soup = BeautifulSoup(''.join(_html), "html.parser")
        _a_category=_soup.find("a", rel="category tag")
        print(_real_url)
        if _a_category is not None:
            _href =_a_category["href"]
            _list_href = _href.split("/")
            _category = _list_href[5]
            print(_category)
            _get_data(_real_url, _soup,_category)
            _less_num=0
        _start_num += 1

def crawer_site1():
    _start_num=20537
    _start_num=36
    _start_num=1
    _real_url = _url.format(_start_num)
    _html = http_helper.get_html(_real_url, "utf=8")
    _soup = BeautifulSoup(''.join(_html), "html.parser")
    _a_category=_soup.find("a", rel="category tag")
    print(_real_url)
    if _a_category is not None:
        _href =_a_category["href"]
        _list_href = _href.split("/")
        _category = _list_href[5]
        print(_category)
        _get_data(_real_url, _soup,_category)


def value_to_key(argument):
    switcher = {
        "pics": 1,
        "tuyue": 1,
        "main": 1,
        "videos": 2,
        "digest": 3
    }
    return switcher.get(argument, 0)


def _get_data(real_url, soup,category):
    if category == "pics":
        _get_pics(real_url, soup)
    elif category == "tuyue":
        _get_tuyue(real_url, soup)
    elif category == "main":
        _get_main(real_url, soup)
    elif category == "videos":
        _get_videos(real_url, soup)
    # elif category == "digest":
    #     _get_digest(real_url, soup)


# http://bohaishibei.com/post/category/pics/
# 分析图片分类，插入数据库
def _get_pics(real_url, soup):
    _category_id = 2
    _main_name = soup.h1.get_text()
    _article = soup.find("article", "article-content")
    _list_p = _article.find_all("p");
    _content = _list_p[0].text
    _insert_mian_info = (
        "INSERT INTO ly_main_info(main_name,content,category_id,source_url,is_deleted,creation_time,creator_user_id)"
        "VALUES ('%s','%s','%d','%s','%d',now(),'%d')")
    _insert_mian_info = _insert_mian_info % (_main_name, _content, _category_id, real_url, 0, 1)
    _list_img = _list_p[1].find_all("img")
    with mysql_helper.transaction():
        _main_id = mysql_helper._insert(_insert_mian_info)
        for i in range(0, len(_list_img)):
            _href = _list_img[i].attrs["src"]
            _insert_pics = (
                "INSERT INTO ly_pics(main_id,title,current_path,original_url,is_deleted,creation_time,creator_user_id)"
                "VALUES ('%d','%s','%s','%s','%d',now(),'%d')")
            _insert_pics = _insert_pics % (_main_id, "", "", _href, 0, 1)
            mysql_helper._insert(_insert_pics)


# http://bohaishibei.com/post/category/tuyue/
def _get_tuyue(real_url, soup):
    _category_id = 1
    _main_name = soup.h1.get_text()
    _article = soup.find("article", "article-content")
    _list_p = _article.find_all("p");
    _article_p_a = _list_p[0].find("a")
    _content = ""
    if _article_p_a is None:
        _content = _list_p[0].text
        del _list_p[0]
    _insert_mian_info = (
        "INSERT INTO ly_main_info(main_name,content,category_id,source_url,is_deleted,creation_time,creator_user_id)"
        "VALUES ('%s','%s','%s','%s','%d',now(),'%d')")
    _insert_mian_info = _insert_mian_info % (_main_name, _content, _category_id, real_url, 0, 1)
    with mysql_helper.transaction():
        _main_id = mysql_helper._insert(_insert_mian_info)
        for i in range(0, len(_list_p) - 1):
            _img = _list_p[i].find("img")
            if _img is not None:
                _href = _img.attrs["src"]
                _insert_pics = (
                    "INSERT INTO ly_pics(main_id,title,current_path,original_url,is_deleted,creation_time,creator_user_id)"
                    "VALUES ('%d','%s','%s','%s','%d',now(),'%d')")
                _insert_pics = _insert_pics.format(_main_id, "", "", _href, 0, 1)
                mysql_helper._insert(_insert_pics)


# http://bohaishibei.com/post/category/main/
def _get_main(real_url, soup):
    _category_id = 1
    _main_name = soup.h1.get_text()
    _article = soup.find("article", "article-content")
    _list_p = _article.find_all("p")
    _content = ""
    _insert_mian_info = (
        "INSERT INTO ly_main_info(main_name,content,category_id,source_url,is_deleted,creation_time,creator_user_id)"
        "VALUES (%s,%s,%s,%s,%s,now(),%s)")
    #_insert_mian_info = _insert_mian_info % (_main_name, _content, _category_id, real_url, 0, 1)
    mysql_helper.connection()
    with mysql_helper.transaction():
        _main_id = mysql_helper._insert(_insert_mian_info,_main_name, _content, _category_id, real_url, 0, 1)
        num = 1
        while num < len(_list_p) - 6:
            _str_p = _list_p[num].string
            if _str_p is None:
                _str_p = ""
                _embed =_list_p[num].find("embed")
                if _embed is not None:
                    _href=_embed.attrs["src"]
                _iframe=_list_p[num].find("iframe")
                if _iframe is not None:
                    _href=_iframe.attrs["src"]
            else:
                num += 1
                _embed =_list_p[num].find("embed")
                if _embed is not None:
                    _href=_embed.attrs["src"]
                _iframe=_list_p[num].find("iframe")
                if _iframe is not None:
                    _href=_iframe.attrs["src"]
            _insert_pics = (
                "INSERT INTO ly_pics(main_id,title,current_path,original_url,is_deleted,creation_time,creator_user_id)"
                "VALUES (%s,%s,%s,%s,%s,now(),%s)")
            # _insert_pics = _insert_pics % (_main_id, _str_p, "", _href, 0, 1)
            mysql_helper._insert(_insert_pics,_main_id, _str_p, "", _href, 0, 1)
            num += 1


# http://bohaishibei.com/post/category/videos/
def _get_videos(real_url, soup):
    _category_id = 2
    _main_name = soup.h1.get_text()
    _article = soup.find("article", "article-content")
    _list_p = _article.find_all("p")
    _content = _list_p[0]
    _insert_mian_info = (
        "INSERT INTO ly_main_info(main_name,content,category_id,source_url,is_deleted,creation_time,creator_user_id)"
        "VALUES ('%s','%s','%d','%s','%d',now(),'%d')")
    _insert_mian_info = _insert_mian_info % (_main_name, _content, _category_id, real_url, 0, 1)
    _video_src = _list_p[1].contents[0].attrs["src"]
    _pic_src = _list_p[2].find("img").attrs["src"]
    with mysql_helper.transaction():
        _main_id = mysql_helper._insert(_insert_mian_info)
        _insert_videos = (
            "INSERT INTO ly_videos(main_id,video_current_path,video_original_url,pic_current_path,pic_original_url,is_deleted,creation_time,creator_user_id)"
            "VALUES ('%d','%s','%s','%s','%s','%d',now(),'%d')")
        _insert_videos = _insert_videos % (_main_id, "", _video_src, "", _pic_src, 0, 1)
        mysql_helper._insert(_insert_videos)


# http://bohaishibei.com/post/category/digest/
def _get_digest(real_url, soup):
    _category_id = 3
    _main_name = soup.h1.get_text()
    _article = soup.find("article", "article-content")
    _len_p = len(_article.contents)
    del _article.contents[_len_p - 1]
    del _article.contents[_len_p - 2]
    _insert_mian_info = (
        "INSERT INTO ly_main_info(main_name,content,category_id,source_url,is_deleted,creation_time,creator_user_id)"
        "VALUES ('%s','%s','%d','%s','%d',now(),'%d')")
    _insert_mian_info = _insert_mian_info % (_main_name, "", _category_id, real_url, 0, 1)
    print(_insert_mian_info)
    with mysql_helper.transaction():
        _main_id = mysql_helper._insert(_insert_mian_info)
        _insert_digest = (
            "INSERT INTO ly_digests(main_id,content,is_deleted,creation_time,creator_user_id)"
            "VALUES ('%d','%s','%d',now(),'%d')")
        _insert_digest = _insert_digest % (_main_id, _article, 0, 1)
        mysql_helper._insert(_insert_digest)

if __name__ == "__main__":
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

