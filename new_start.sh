run_server(){
    # 判断是否存在python进程，如果存在，杀死进程
    python_pid_list=$(ps -ef |grep python3 |grep -v grep |head -10 |awk '{print $2}')
    for python_pid in $python_pid_list
    do 
        kill -s 9 $python_pid
        echo "kill $python_pid"
    done  

   #启动服务  
    nohup python3 manage.py runserver 0.0.0.0:8000  --insecure &
    echo "启动 Django 项目"
    nohup python3 manage.py celeryd -l  info -c 1 &
    echo "启动 celery 异步执行"
    nohup sudo python3 manage.py celerybeat -l info &
    echo "启动 celery 定时执行"

}
run_server
