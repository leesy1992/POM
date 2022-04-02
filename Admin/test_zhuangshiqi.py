from bs4 import BeautifulSoup
import os

def statistics_report_timeOut(html_doc, time_ms=300.00):
    """统计报告中是否存在接口超时请求
    html_doc:html报告路径
    time_ms：超时判定的毫米
    :return：totalCaseNameList 组装后的超时用例集合列表： [ 用例：冒烟18-排班分组-全部人员更新排班表成功 下 [单接口-【排班管理】-B端更新全部员工排班分组接口, 响应时间:463.45 ms, 用例状态:pass], 用例：xxx]
            signleTotal  超时用例列表：[单接口-【排班管理】-B端更新全部员工排班分组接口,x2,x3]
    """
    with open(html_doc, 'rb') as f:
        soup = BeautifulSoup(f.read(), "lxml")
        totalCaseNameList = list()
        signleTotal = list()
        signleUrl = []
        # # 创建CSS选择器
        result = soup.select("ul#test-collection>li>div.test-content")  # 获取测试集合节点
        for site in result:  # 获取单个用例的位置
            totalCaseName = site.select("div.test-attributes>div>span:nth-child(1)")
            caseTotal = "用例：{} 下 ".format(totalCaseName[0].get_text())            
            signleSuiteCase = site.select("ul.node-list>li")
            for s in signleSuiteCase:
                signleCase = ""
                signleurl = ""
                caseName = s.select("div>div.node-name")
                responseTime = s.select("div>span.node-duration")
                responseResult = s.select("div>span.test-status")
                responseurl = s.select(" tbody > tr:nth-child(1)>td.step-details")
                # print(responseurl[0].get_text())
                if "登录" in caseName[0].get_text(): continue # 去除登录接口的校验
                if float(responseTime[0].get_text()[15:].replace("ms", "")) >= time_ms:
                    caseTotal += "[{}接口, 响应时间:{}, 用例状态:{}]".format(caseName[0].get_text(),responseTime[0].get_text()[15:],responseResult[0].get_text())
                    signleCase +="{}接口".format(caseName[0].get_text())
                    signleurl  +="{}".format(responseurl[0].get_text())
                    signleTotal.append(signleCase)
                    signleUrl.append(signleurl)
            if caseTotal.endswith("]"):
                totalCaseNameList.append(caseTotal)                
    # print("组装超时用例集列表", totalCaseNameList)
    # print("单个超时用例列表", signleTotal)
    return totalCaseNameList,list(set(signleTotal))



def get_list(caselist=[]):
    print(type(caselist))
    if caselist:
        for case in caselist:
            print("fffffffffffff \n ggggggggggg")

# html="C:/Users/dell/AppData/Roaming/Foxmail7/Temp-4332-20200720091416/Attach/TestReports(4).html "  
# ss=statistics_report_timeOut(html,time_ms=150)
# # print(ss[0])
# print(ss[1])
# sbulist=list(ss[1].keys())
# # valuelist= list(ss[1].values())
# for sbu in sbulist:
#     print(ss[1][sbu])
# get_list(ss[1])
a=13.00902938383
print(str(int(a))+"ms")
