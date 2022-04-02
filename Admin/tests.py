import time as t


class MyTimer():

    # 初始化构造函数
    def __init__(self):
        self.prompt = "未开始计时..."
        self.lasted = []
        self.begin = 0
        self.end = 0

    # 重写__str__方法 (演示使用，代码可省略)
    def __str__(self):
        return self.prompt

    # 重写__repr__方法
    def __repr__(self):
        return self.prompt

    # __repr__ = __str__   #偷懒的repr方法

    # 开始计时
    def start(self):
        self.begin = int(round(t.time() * 1000))
        print ("计时开始....")

    # 结束计时
    def stop(self):
        self.end = int(round(t.time() * 1000))
        print ("计时结束...")
        return self.calc()

    # 计算运行时间
    def calc(self):
        self.lasted = []
        self.lasted.append(self.end-self.begin)
        self.prompt = "总共运行了"
        self.prompt +=str(self.lasted)
        return self.prompt

        # for i in range(6):
        #     self.lasted.append(self.end[i] - self.begin[i])
        #     self.prompt += str(self.lasted[i])
        # print

if __name__=="__main__":
    timeing=MyTimer()
    timeing.start()
    t.sleep(1)

    #函数。无参装饰器，单形参，返回值也是函数，目前功能增强，功能装饰
    #等价式