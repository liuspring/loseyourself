#Python3.5
#liujian 2016.04.12
#coding=utf-8
import os
import urllib.request

#返回保存路径
def dest_file(targetDir,path):
    if not os.path.isdir(targetDir):
        os.mkdir(targetDir)
    pos = path.rindex('/')
    t = os.path.join(targetDir, path[pos+1:])
    return t

#下载图片到指定路径
def down_img(targetDir,link):
    filePath=dest_file(targetDir,link)
    urllib.request.urlretrieve(link,filePath)