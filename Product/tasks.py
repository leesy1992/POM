import json
import time
from celery.task import task
from Autotest_platform.PageObject.logger import Logger

log=Logger("测试").logger

# 自定义要执行的task任务


@task
def SplitTask(result_id):
    from Product.models import Result, SplitResult
    result = Result.objects.get(id=result_id)
    result.status = 20
    result.save()
    parameter = json.loads(result.parameter) if result.parameter else []
    browsers = json.loads(result.browsers) if result.environments else [1]
    environments = json.loads(result.environments) if result.environments else []
    beforlogins= json.loads(result.beforeLogin) if result.beforeLogin else []
    for browser in browsers:
        if environments:
            for environmentId in environments:
                if beforlogins:
                    for beforlogin in beforlogins:
                        if parameter:
                            for params in parameter:
                                for k, v in params.items():
                                    if v and isinstance(v, str):
                                        if '#time#' in v:
                                            v = v.replace('#time#',
                                                        time.strftime('%Y%m%d', time.localtime(time.time())))
                                        if '#random#' in v:
                                            import random
                                            v = v.replace('#random#', str(random.randint(1000, 9999)))
                                        if '#null#' == v:
                                            v = None
                                        if '#logo#' == v:
                                            v = "/home/Atp/logo.png"
                                        params[k] = v
                                sr = SplitResult.objects.create(environmentId=environmentId, browserId=browser,beforeLogin=beforlogin,
                                                                resultId=result.id,
                                                                parameter=json.dumps(params, ensure_ascii=False),
                                                                expect=params.get('expect', True))
                                SplitTaskRunning.delay(sr.id)
                        else:
                            sr = SplitResult.objects.create(environmentId=environmentId, browserId=browser ,resultId=result.id,
                                                            parameter={}, expect=True,beforeLogin=beforlogin)
                            SplitTaskRunning.delay(sr.id)
        else:
            if parameter:
                for params in parameter:
                    for k, v in params.items():
                        if v and isinstance(v, str):
                            if '#time#' in v:
                                v = v.replace('#time#', time.strftime('%Y%m%d', time.localtime(time.time())))
                            if '#random#' in v:
                                import random
                                v = v.replace('#random#', str(random.randint(1000, 9999)))
                            if '#null#' == v:
                                v = None
                            if '#logo#' == v:
                                v = "/home/Atp/logo.png"
                            params[k] = v
                    sr = SplitResult.objects.create(environmentId=0, browserId=browser, resultId=result.id,
                                                    parameter=json.dumps(params, ensure_ascii=False),
                                                    expect=params.get('expect', True))
                    SplitTaskRunning.delay(sr.id)
            else:
                sr = SplitResult.objects.create(environmentId=0, browserId=browser, resultId=result.id,
                                                parameter={}, expect=True)
                SplitTaskRunning.delay(sr.id)
    SplitTaskRan.delay(result_id)


@task
def SplitTaskRan(result_id):
    from Product.models import Result, SplitResult
    result = Result.objects.get(id=result_id)
    while len(SplitResult.objects.filter(resultId=result.id, status__in=[10, 20])) > 0:
        time.sleep(1)
    split_list = SplitResult.objects.filter(resultId=result.id)
    for split in split_list:
        expect = split.expect;
        result_ = True if split.status == 30 else False
        if expect != result_:
            result.status = 40
            result.save()
            return
    result.status = 30
    result.save()
    return


@task
def SplitTaskRunning(splitResult_id):
    from Product.models import SplitResult, Browser, Environment, Element, Check, Result, EnvironmentLogin, LoginConfig,Keyword,TestCase,Count
    import django.utils.timezone as timezone
    from Autotest_platform.PageObject.Base import PageObject
    from Autotest_platform.helper.util import get_model,get_timing,send_dingding,send_email
    split = SplitResult.objects.get(id=splitResult_id)
    result_ = Result.objects.get(id=split.resultId)
    steps = json.loads(result_.steps) if result_.steps else []
    parameter = json.loads(split.parameter) if split.parameter else {}
    checkType = result_.checkType
    checkValue = result_.checkValue
    checkText = result_.checkText
    selectText = result_.selectText
    case_title = result_.title #获取用例标题
    beforeLogin = split.beforeLogin if split.beforeLogin else []
    beforeLogin = [""+beforeLogin+""]
    split.status = 20
    split.save()
    split.startTime = timezone.now()
    environment = get_model(Environment, id=split.environmentId)
    host = environment.host if environment and environment.host else ''
    driver = None
    try:
        driver = Browser.objects.get(id=split.browserId).buid()
    except Exception as e:
        split.status = 40
        split.remark = '浏览器初始化失败'
        split.finishTime = timezone.now()
        split.save()
        log.error(split.remark)
        send_dingding(case_title +"\n"+ split.remark)
        send_email("【失败】",case_title,split.resultId)
        # send_email_reports(split.resultId,name=case_title,status="【失败】")
        if driver:
            driver.quit()
        return
    if beforeLogin and len(beforeLogin) > 0:
        for bl in beforeLogin:
            login = get_model(LoginConfig, id=bl)
            loginCheckType = login.checkType
            loginCheckValue = login.checkValue
            loginCheckText = login.checkText
            loginSelectText = login.selectText
            if not login:
                split.loginStatus = 3
                split.status = 50
                split.remark = "找不到登陆配置,id=" + str(bl)
                split.finishTime = timezone.now()
                split.save()
                log.error(split.remark)
                send_dingding(case_title +"\n"+split.remark)
                send_email("【失败】",case_title,split.resultId)
                if driver:
                    driver.quit()
                return
            loginSteps = json.loads(login.steps) if login.steps else []
            loginParameter = {}
            if environment:
                environmentLogin = get_model(EnvironmentLogin, loginId=bl, environmentId=environment.id)
                if environmentLogin:
                    loginParameter = json.loads(environmentLogin.parameter) if environmentLogin.parameter else {}
            for loginStep in loginSteps:
                try:
                    #登录步骤（核心）
                    Step(loginStep.get("keywordId"), loginStep.get("values")).perform(driver, loginParameter, host)
                except Exception as e:
                    split.loginStatus = 2
                    split.status = 50
                    split.remark = "初始化登陆失败</br>登陆名称=" + login.name + " , </br>错误信息=" + str(e.args)
                    split.finishTime = timezone.now()
                    split.save()
                    log.error(split.remark)
                    send_dingding(case_title +"\n"+split.remark)
                    send_email("【失败】",case_title,split.resultId)
                    if driver:
                        driver.quit()
                    return
            if loginCheckType:
                time.sleep(2)
                if loginCheckType == Check.TYPE_URL:
                    if not driver.current_url.endswith(str(loginCheckValue)):
                        split.loginStatus = 2
                        split.status = 50
                        split.remark = "初始化登陆失败</br>登陆名称=" + login.name + " , </br>错误信息=登录断言不通过"
                        split.finishTime = timezone.now()
                        split.save()
                        log.error(split.remark)
                        send_dingding(case_title +"\n"+split.remark)
                        send_email("【失败】",case_title,split.resultId)
                        if driver:
                            driver.quit()
                        return
                elif loginCheckType == Check.TYPE_ELEMENT:
                    element = loginCheckValue
                    if str(loginCheckValue).isdigit():
                        element = get_model(Element, id=loginCheckValue)
                    try:
                        PageObject.find_element(driver, element)
                    except:
                        split.loginStatus = 2
                        split.status = 50
                        split.remark = "初始化登陆失败[ 登陆名称:" + login.name + " , 错误信息：断言不通过"
                        split.finishTime = timezone.now()
                        split.save()
                        log.error(split.remark)
                        send_dingding(case_title +"\n"+split.remark)
                        send_email("【失败】",case_title,split.resultId)
                        if driver:
                            driver.quit()
                        return
        else:
            split.loginStatus = 1
    index = 1
    for step in steps:
        try:
            #执行测试步骤（核心）
            time.sleep(0.5)
            start_time=int(round(time.time() * 1000))
            Step(step.get("keywordId"), step.get("values")).perform(driver, parameter, host)
            durtion=  str(int(round(time.time() * 1000))-start_time)+"ms"         
            durtions={"页面加载完成":durtion}
            #准备log，获取到关键字（keyname）和元素名称(elemetname)，将其组合成步骤log，但有的value值需连表查询，有的是直接在value
            keyname = Keyword.objects.get(id=step.get("keywordId")).name
            try:
                if step.get("values"):
                    elemetname = Element.objects.get(id=step.get("values")[0]["value"]).name
                else:
                    elemetname=""     
            except:
                elemetname=step.get("values")[0]["value"]         
            split.remark="第" + str(index) + "步:"+keyname + elemetname

            try:
                getTime=get_timing()
                getTime.update(durtions)
                if split.loadtime:
                    split.loadtime=str(split.loadtime) +"/" + str(getTime) #计算步骤的加载时间并存入数据库
                else:
                    split.loadtime=getTime 
                log.info(getTime) 
            except Exception as e:
                log.error("计时错误！！！{}".format(e))
            log.info(split.remark)
            index = index + 1
        except RuntimeError as re:
            split.status = 40
            split.remark = "测试用例执行第" + str(index) + "步失败，错误信息:" + str(re.args)
            split.finishTime = timezone.now()
            split.save()
            log.error(split.remark)
            send_dingding(case_title +"\n"+split.remark)
            send_email("【失败】",case_title,split.resultId)
            if driver:
                driver.quit()
            return
        except Exception as info:
            split.status = 40
            split.remark = "执行测试用例第" + str(index) + "步发生错误，请检查测试用例:" + str(info.args)
            split.finishTime = timezone.now()
            split.save()
            log.error(split.remark)
            send_dingding(case_title +"\n"+split.remark)
            send_email("【失败】",case_title,split.resultId)
            if driver:
                driver.quit()
            return
    remark = '测试用例未设置断言,建议设置'
    time.sleep(2)
    if checkType:
        if checkType == Check.TYPE_URL:
            TestResult = driver.current_url.endswith(checkValue)
            if not TestResult:
                if not split.expect:
                    remark = '测试通过'
                else:
                    remark = '测试不通过,预期结果为["' + checkValue + '"], 但实际结果为["' + driver.current_url + '"]'
            else:
                if split.expect:
                    remark = '测试通过'
                else:
                    remark = '测试不通过,预期结果为["' + checkValue + '"], 但实际结果为["' + driver.current_url + '"]'
        elif checkType == Check.TYPE_ELEMENT:
            element = checkValue
            expect_text = checkText
            select_text = selectText
            if str(checkValue).isdigit():
                element = get_model(Element, id=int(element))
            try:
                actual_text=PageObject().get_text(element)
                if select_text == 'all':
                    if expect_text == actual_text:
                        TestResult = True
                    else:
                        TestResult = False
                    if TestResult:
                        if split.expect:
                            remark = '测试通过，预期断言值完全匹配实际断言值。'
                        else:
                            remark = '测试不通过，预期结果失败，但实际结果是成功。'
                    else:
                        if not split.expect:
                            remark = '测试通过，预期结果失败，实际结果也是失败。'
                        else:
                            remark = '测试不通过，预期结果为["' + expect_text + '"]，但实际结果为["' + actual_text + '"]'
                else:
                    if expect_text in actual_text:
                        TestResult = True
                    else:
                        TestResult = False
                    if TestResult:
                        if split.expect:
                            remark = '测试通过，预期断言值包含匹配实际断言值。'
                        else:
                            remark = '测试不通过，预期结果失败，但实际结果是成功。'
                    else:
                        if not split.expect:
                            remark = '测试通过，预期结果失败，实际结果也是失败。'
                        else:
                            remark = '测试不通过，预期结果为["' + expect_text + '"]，但实际结果为["' + actual_text + '"]'
            except BaseException as e:
                log.error("断言出现异常:{}".format(e))
                TestResult = False
                remark = "断言出现异常:{}".format(e)
                

                    
    if driver:
        driver.quit()
    split.status = 30 if TestResult else 40
    split.remark = remark
    split.finishTime = timezone.now()
    split.save()
    log.info(split.remark)
    send_dingding(case_title +"\n"+split.remark)
    status= "【成功】" if "测试通过" in remark  else "【失败】"
    send_email(status,case_title,split.resultId)
    return

#定时任务
@task
def timingRunning(**kwargs):    
    from Product.models import Task, TestCase, Result
    from Autotest_platform.helper.util import get_model
    tasks = Task.objects.filter(timing=1,name=kwargs.get('name'))  if kwargs.get('name') else Task.objects.filter(timing=1) 
    for t in tasks:
        browsers = json.loads(t.browsers) if t.browsers else []
        testcases = json.loads(t.testcases) if t.testcases else []
        for tc in testcases:
            environments = tc.get("environments", [])
            tc = get_model(TestCase, id=tc.get("id", 0))
            r = Result.objects.create(projectId=tc.projectId, testcaseId=tc.id, checkValue=tc.checkValue,
                                      checkType=tc.checkType, checkText=tc.checkText, selectText=tc.selectText,
                                      title=tc.title, beforeLogin=tc.beforeLogin,
                                      steps=tc.steps, parameter=tc.parameter,
                                      browsers=json.dumps(browsers, ensure_ascii=False),
                                      environments=json.dumps(environments, ensure_ascii=False), taskId=t.id)
            SplitTask.delay(r.id) 


class Step:
    def __init__(self, keyword_id, values):
        from .models import Keyword, Params
        from Autotest_platform.helper.util import get_model
        self.keyword = get_model(Keyword, id=keyword_id)
        self.params = [Params(value) for value in values]

    def perform(self, driver, parameter, host):
        from .models import Params, Element
        #1-关键字类型为系统里面的
        if self.keyword.type == 1:
            values = list()
            for p in self.params:
                if p.isParameter:
                    if p.Type == Params.TYPE_ELEMENT:
                         v = Element.objects.get(id=parameter.get(p.value, None))
                    else:
                        v = parameter.get(p.value, None)
                elif p.Type == Params.TYPE_ELEMENT:
                    v = Element.objects.get(id=p.value)
                else:
                    v = p.value
                if self.keyword.method == 'open_url' and not ('http://' in v or 'https://' in v):
                    v = host + v
                values.append(v)

            try:
                self.sys_method__run(driver, tuple(values))
            except:
                raise
        #2-关键字类型为自定义，多个步骤组成    
        elif self.keyword.type == 2:
            steps = json.loads(self.keyword.steps)
            for pa in self.params:
                if not pa.isParameter:
                    if pa.Type == Params.TYPE_ELEMENT:
                        parameter[pa.key] = Element.objects.get(id=pa.value)
                    else:
                        parameter[pa.key] = pa.value
            for step in steps:
                try:
                    Step(step.get("keywordId"), step.get("values")).perform(driver, parameter, host)
                except:
                    raise

    def sys_method__run(self, driver, value):
        #导入包，等同import packge
        package = __import__(self.keyword.package, fromlist=True)
        #获取包的类的字段
        clazz = getattr(package, self.keyword.clazz)
        #用于设置属性值，把driver给到类
        setattr(clazz, "driver", driver)
        #通过方法名称获取那个方法,getattr() 函数用于返回一个对象属性值。
        method = getattr(clazz, self.keyword.method)

        def running(*args):
            try:
                #实例化类
                c = clazz()
                #参数收集的逆过程
                para = (c,)
                args = para + args[0]
                method(*args)
            except:
                raise

        try:
            running(value)
        except:
            raise
