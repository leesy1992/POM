run_server(){
    # 判断是否存在python进程，如果存在，杀死进程
    python_pid_list=$(ps -ef |grep python3 |grep -v grep |head -10 |awk '{print $2}')
    for python_pid in $python_pid_list
    do 
        kill -s 9 $python_pid
        echo "kill $python_pid  杀死进程"
    done  

}
run_server