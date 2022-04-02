"""获取数据库对应表的对象"""
def get_model(model, get=True, *args, **kwargs ):
    from django.db.models.base import ModelBase
    if isinstance(model, ModelBase):
        if get:
            try:
                return model.objects.get(*args, **kwargs)
            except:
                return None
        else:
            return model.objects.filter(*args, **kwargs)
    else:
        raise TypeError("model 没有继承 django.db.models.base.ModelBase")


def isLegal(string, length=5, match_='([^a-z0-9A-Z_])+'):
    import re
    pattern = re.compile(match_)
    match = pattern.findall(string)
    if string and len(string) > length:
        if match:
            return False
        else:
            return True
    else:
        return False

def md5(string):
    import hashlib
    return hashlib.md5(string.encode()).hexdigest()

def validateEmail(email):
    import re
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email):
            return True
    return False

def get_timing():
    """
       计算页面加载时间、白屏时间、DOM加载时间、资源加载最大耗时
    """
    from Autotest_platform.PageObject.Base import PageObject
    

    domready = """          // DOMready时间 
                    let mytiming = window.performance.timing;
                    return mytiming.domContentLoadedEventEnd   - mytiming.navigationStart ;
              """
    loadEventTime = """     //onload页面加载时间
                   let mytiming = window.performance.timing;
                   return mytiming.loadEventEnd - mytiming.navigationStart ;
                   """
    whiteTime="""         //白屏时间
                    let mytiming  = window.performance.timing;
                    return mytiming.responseStart - mytiming.navigationStart ;
                """  
    resource="""          //资源加载时间
                let resources = window.performance.getEntriesByType('resource');
                var durations=[];
                for (let i in resources){
                    durations +=resources[i].duration +",";
                    }
                return durations;
                        
            """ 

    get_resource=PageObject().js_execute(resource)

    resource_max =str(int(get_maxNunber(get_resource)))+"ms"
 
    DOM_time=str(int(PageObject().js_execute(domready)))+"ms"

    white_time=str(int(PageObject().js_execute(whiteTime)))+"ms"

    load_EventTime=str(int(PageObject().js_execute(loadEventTime)))+"ms"

    return {"页面加载时间": load_EventTime,"白屏时间":white_time,"DOM加载时间": DOM_time,"资源加载最大耗时":resource_max} 


def send_dingding(massage):
    import json,requests
    '''
        关联钉钉机器人，执行错误会推送消息到钉钉
		access_token: 钉钉的Webhook
		content: 发送的内容
		msgtype : 类型
	'''     
    value={
            "msgtype": "text", 
            "text": {
                "content": massage }
                } 
    access_token = 'https://oapi.dingtalk.com/robot/send?access_token=ed7e3e0483fb6ec66dee3281d58c4983d6e6da5b90c5f8a07fa8aa2efb99ca00'
        
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    values = json.dumps(value)
    respose=requests.post(access_token,values,headers=headers)  
    print("钉钉消息推送成功：{}".format(respose.text)) if "ok" in respose.text else print ("钉钉消息推送失败：{}".format(respose.text)) 
    


def get_maxNunber(string):
    if isinstance(string,str):
        string=string.split(',')
        my_list=[]
        for i in string:
            if i:
                my_list.append(float(i))
        return max(my_list)    
    else:
        return max(string)


#新建一个计时装饰器
import time
from Autotest_platform.PageObject.logger import Logger
log=Logger("计时").logger

def get_time(fn):
    """计时装饰器"""
    def swapper(*args,**kwargs):
        start_time=int(round(time.time() * 1000))
        res=fn(*args,**kwargs)
        stop_time=int(round(time.time() * 1000))
        delta=stop_time-start_time
        log.info(str(delta) +"ms")

        return res
    return swapper



            
"""失败发邮件判断"""

from Product.models import Count
from Autotest_platform.PageObject.emails import send_email_reports
def send_email(massage,case_title,resultId):
        if massage=="【失败】":
            count=get_model(Count,title=case_title)  
            if count:
                count.counts=count.counts +1
                if count.counts%5==0:
                    count.status +=1

            else:
                Count.objects.create(title=case_title,counts=1,status=0)
                return "Done"        
        else:
            return "Done"    
        if count.counts>=5:
            send_email_reports(resultId,name=case_title,status=massage)
            count.counts=0
        count.save()




def task_login(**kwargs):
    if kwargs.get("name") is "":
        return '任务名称不可为空'

    if kwargs.get("timing")==2:
        return "该任务为常规任务"
    try:
        crontab_time = kwargs.pop('crontab').split('/')
        if len(crontab_time) > 5:
            return '定时配置参数格式不正确'
        crontab = {
            'day_of_week': crontab_time[-1],
            'month_of_year': crontab_time[3],  # 月份
            'day_of_month': crontab_time[2],  # 日期
            'hour': crontab_time[1],  # 小时
            'minute': crontab_time[0],  # 分钟
        }
    except Exception:
        crontab = {
            'day_of_week': '1-5',
            'month_of_year': '*',  # 月份
            'day_of_month': '*',  # 日期
            'hour': 0,  # 小时
            'minute': 0,  # 分钟
        }
    name=kwargs.get('name')
    kwarg={"name":name}
    return create_task(name, 'Product.tasks.timingRunning', kwarg,  crontab)



import json

from djcelery import models as celery_models


def create_task(name, task, task_args, crontab_time,):
    '''
    新增定时任务
    :param name: 定时任务名称
    :param task: 对应tasks里已有的task
    :param task_args: list 参数
    :param crontab_time: 时间配置
    :param desc: 定时任务描述
    :return: ok
    '''
    # task任务， created是否定时创建
    task, created = celery_models.PeriodicTask.objects.get_or_create(name=name, task=task)
    # 获取 crontab
    crontab = celery_models.CrontabSchedule.objects.filter(**crontab_time).first()
    if crontab is None:
        # 如果没有就创建，有的话就继续复用之前的crontab
        crontab = celery_models.CrontabSchedule.objects.create(**crontab_time)
    task.crontab = crontab  # 设置crontab
    task.enabled = True  # 开启task
    task.kwargs = json.dumps(task_args, ensure_ascii=False)  # 传入task参数
    # task.description = desc
    task.save()
    return 'ok'