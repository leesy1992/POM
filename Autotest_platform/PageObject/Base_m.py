from lib2to3.pgen2 import driver
import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class APPObject:
    driver = None

    def sleep(self, second):
        if str(second).isdigit():
            time.sleep(int(second))
        else:
            time.sleep(0.5)

    def wait(self, seconds):
        self.driver.implicitly_wait(seconds)

    # def open_baidu(self):       
    #     self.driver.find_element_by_id("com.android.browser:id/search_hint").click()
    #     self.sleep(2)
    #     self.driver.find_element_by_id("com.android.browser:id/url").send_keys("m.baidu.com")
    #     self.sleep(3)
    #     self.driver.find_element_by_id("com.android.browser:id/rightText").click()
    #     self.sleep(6)
    #     self.wait(4)

    @staticmethod
    def find_element(driver, locator, more=False, timeout=20):
        message = locator
        if isinstance(locator, dict):
            locator = (locator.get("by", None), locator.get("locator", None))
            message = locator
        elif isinstance(locator, list) and len(locator) > 2:
            locator = (locator[0], locator[1])
            message = locator
        elif isinstance(locator, Element):
            message = locator.name
            locator = (locator.by, locator.locator)
        elif isinstance(locator, str):
            locator = tuple(locator.split(".", 1))
            message = locator
        else:
            raise TypeError("element参数类型错误: type:" + str(type(locator)))
        try:
            try:
                if more:
                    return WebDriverWait(driver, timeout).until(ec.visibility_of_all_elements_located(locator))
                else:
                    return WebDriverWait(driver, timeout).until(ec.visibility_of_element_located(locator))
            except:
                if more:
                    return WebDriverWait(driver, timeout).until(ec.presence_of_all_elements_located(locator))
                else:
                    return WebDriverWait(driver, timeout).until(ec.presence_of_element_located(locator))
        except Exception:
            raise RuntimeError("找不到元素:" + str(message))


    def swipe(self,start_x, start_y, end_x, end_y, duration=None):
        """swipe滑动事件"""
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)

    def scroll(self,origin_el, destination_el):
        """scroll滑动事件"""
        origin=self.find_element(self.driver,origin_el)
        estination=self.find_element(self.driver,destination_el)
        self.driver.scroll(origin,estination)

    def drag_and_drop(self,origin_el, destination_el):
        """drag_and_drop拖拽事件"""
        origin=self.find_element(self.driver,origin_el)
        estination=self.find_element(self.driver,destination_el)
        self.driver.drag_and_drop(origin,estination)

    def get_screenshot(self,filename):
        """截图操作"""
        date=time.strftime('%Y-%m-%d',time.localtime(time.time()))

        self.driver.get_screenshot_as_file('APP{}{}.png'.format(date,filename))
        return "截图成功"

    def click(self, locator):
        if locator is None:
            return
        else:
            try:
                self.find_element(self.driver, locator).click()
            except:
                raise "无效点击"

    
    def send_keys(self, locator, value):
        if locator is None:
            return
        if self.get_text(locator):
            self.clear(locator)
            self.find_element(self.driver, locator).send_keys(value)
        else:
            self.find_element(self.driver, locator).send_keys(value)

    def clear(self, locator):
        if locator is None:
            return
        else:
            self.find_element(self.driver,locator).clear()