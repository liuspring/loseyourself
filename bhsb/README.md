解析博海拾贝网站内容存入数据
1，图片 pics  http://bohaishibei.com/post/category/pics/   
注;第一个P元素是content，第二个P包含的img是多张图片
5，图悦 tuyue  http://bohaishibei.com/post/category/tuyue/
注:第一个p元素不包含a标签是content，下面是多张a标签的内容，最后一个p不是
6，博海拾贝 main   http://bohaishibei.com/post/category/main/
获取<font color="green">下的所有p元素

1，5，6可以放在一个表内。

2，优惠 tao   http://bohaishibei.com/post/category/tao/

3，视频，videos   http://bohaishibei.com/post/category/videos/

第一个p是content，第二个视频，第三个图片

4，文摘 digest  http://bohaishibei.com/post/category/digest/
<article class="article-content">内的所有内容


存放库：LoseYou

        
    # __category_id=value_to_key(_category)
    # __target_dir=_target_dir.format(__category_id)
    # _main_name = soup.h1.get_text()
    # _content=""
    # _article=soup.find("article","article-content")
    # with mysql_helper.transaction():
    #     if (_category == "pics" or _category == "videos" or _category == "tuyue"):
    #         _article_p = _article.find("p")
    #         _article_p_a = _article_p.find("a")
    #         if _article_p_a is None:
    #             _content = _article_p.text
    #     _insert_mian_info = ("INSERT INTO ly_main_info(main_name,content,category_id,source_url,creation_time,creator_user_id)"
    #                         "VALUES ('{0}','{1}','{2}','{3}','{4}','{5}')"
    #     )
    #     _insert_mian_info = _insert_mian_info.format(_main_name, _content, __category_id, real_url, time.time(), 1)
    #     _list_p=_article.find_all("p")