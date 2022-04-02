from __future__ import absolute_import, unicode_literals

import os

from celery import Celery,platforms

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Autotest_platform.settings')

# 注册Celery的APP
app = Celery('Autotest_platform')
# 绑定配置文件
app.config_from_object('django.conf:settings')

# 自动发现各个app下的tasks.py文件
app.autodiscover_tasks(['Product'], force=True)

platforms.C_FORCE_ROOT = True  #celery不能用root用户启动 加上这一行
