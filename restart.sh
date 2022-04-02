sudo ps -ef|grep python3|grep -v grep|cut -c 9-15|xargs kill -9
echo "删除进程"
nohup python3 manage.py runserver 0.0.0.0:8000 &
echo "启动 Django 项目"
nohup python3 manage.py celeryd -l  info -c 1 &
echo "启动 celery 异步执行"
nohup sudo python3 manage.py celerybeat -l info &
echo "启动 celery 定时执行"
