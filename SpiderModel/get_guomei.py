# coding:utf-8

from bs4 import BeautifulSoup
from SpiderModel import httpHelper

url='http://www.gome.com.cn/allcategory/'
html=httpHelper.GetHtml(url,'utf-8')
soup=BeautifulSoup(''.join(html),'html.parser')
items=soup.find_all('div','item')
with open('allcategory.txt', 'w') as f:
    for item in items:
        cat=item.h3.next
        f.write(cat+'：')
        childs=item.find_all('a')
        str=""
        for child in childs:
            str+=child.string+"、"
        f.write(str+'\n')









# cat = fromstring(r.text).xpath('//div[@class="in"]/a/@href')
# cat = ''.join(cat)
# cat = re.findall('(cat\d+)\.', cat)
# with open('allcategory.txt', 'w') as f:
#     f.write('\n'.join(cat))