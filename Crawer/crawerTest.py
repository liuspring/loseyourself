#Python3.5
#liujian 2016.04.12
#coding=utf-8

from bs4 import BeautifulSoup
import httpHelper
import downHelper
import dbHelper
import logging

logging.basicConfig(level=logging.DEBUG)
dbHelper.create_engine("root", "1234qwer", "bhsb", "127.0.0.1", "3306")

url="http://bohaishibei.com/post/{0}/"
targetDir="E:\python\PycharmProjects\CrawerBHSB\img\{0}/"
# todo
def GetData(soup,category):
    article=soup.h1.get_text()
    targetPath=targetDir.format(article)
    sql="INSERT INTO bhsb_article (article,category,url,`comment`)VALUES ('{0}','{1}','{2}','{0}')"
    sql=sql.format(article,category,realUrl)
    with dbHelper.transaction():
        article_id=dbHelper._insert(sql)
        if category=="博海拾贝" or category=="图片":
            article=soup.find_all("article",attrs={"class":"article-content"})
            list=article[0].find_all("p")
            for i in range(1,len(list)-3):
                if(i%2==1):
                    title=list[i].string
                    if i+1>=len(list)-3:
                        break
                    if(i==13):
                        a=2
                    img=list[i+1].find_all("img")
                    if(len(img)!=1):
                        continue
                    src=img[0].attrs["src"]
                    #downHelper.DownLoadImg(targetPath,src)
                    sql="INSERT INTO bhsb_picture(article_id,title,source_url,current_url) VALUES ('{0}','{1}','{2}','{3}')"
                    sql=sql.format(article_id,title,src,src)
                    dbHelper._insert(sql)
                    i+=2

#for i in range(0,10000):
realUrl=url.format(18682)
currentHtml = httpHelper.GetHtml(realUrl, "utf-8")
soup = BeautifulSoup(''.join(currentHtml),"html.parser")
objCategory=soup.find_all("a",rel="category")
# if(len(objCategory)!=1):
#  continue;
category=objCategory[0].string
GetData(soup,category)











    
