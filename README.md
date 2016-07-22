注意：
1，配置数据库链接注意：
settings.py修改如下
DATABASES = {
       'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'LoseYourself',
        'USER': 'root',
        'PASSWORD': '1234qwer',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
__init__.py添加如下代码
import pymysql
pymysql.install_as_MySQLdb()

2，初始化数据库时需要先创建空数据库
执行如下语句：python manage.py migrate

3，创建超级管理员
python manage.py createsuperuser
admin
admin@qq.com
1234qwer

4，https://github.com/Qutan/Spider





