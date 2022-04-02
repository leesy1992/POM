from pickle import TRUE
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from Product.models import Element
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import time
import requests
import json
import random
import pyautogui
from Autotest_platform.PageObject.logger import Logger
from Admin.tests import MyTimer
from Autotest_platform.helper.util import get_time


log=Logger("111").logger
timing=MyTimer()
class PageObject:
    driver = None

    def sleep(self, second):
        if str(second).isdigit():
            time.sleep(int(second))
        else:
            time.sleep(0.5)

    def wait(self, seconds):
        """隐式等待"""
        self.driver.implicitly_wait(seconds)
        
    def open_url(self, url):
        self.driver.get(url)

    def max_size(self):
        self.driver.maximize_window()

    def click(self, locator):
        if locator is None:
            return
        else:
            try:
                self.find_element(self.driver, locator).click()
            except :
                raise AssertionError("没有找到可点击元素" )

    def click_point(self, x, y, left_click=True):
        if left_click:
            ActionChains(self.driver).move_by_offset(x, y - 103).click().perform()
        else:
            ActionChains(self.driver).move_by_offset(x, y - 103).context_click().perform()

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

    def alert_accept(self):
        self.driver.switch_to.alert().accept()

    def alert_dismiss(self):
        self.driver.switch_to.alert().dismiss()

    def switch_to_window(self, title=None):
        handle = self.driver.current_window_handle
        if title:
            for handle_ in self.driver.window_handles:
                if handle != handle_:
                    self.driver.switch_to.window(handle)
                    if self.driver.title == title:
                        break
            else:
                raise ValueError("未找到标题为：" + title + " 的页面")
        else:
            for handle_ in self.driver.window_handles:
                if handle != handle_:
                    self.driver.switch_to.window(handle)

    def switch_to_frame(self, locator=None):
        if locator:
            self.driver.switch_to.frame(self.find_element(self.driver, locator))
        else:
            self.driver.switch_to.default_content()

    def forward(self):
        self.driver.forward()

    def back(self):
        self.driver.back()
        self.sleep(1)

    def refresh(self):
        self.driver.refresh()

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()

    def select_by_text(self, locator, value, visible=False):
        if locator is None:
            return
        locator = self.find_element(self.driver, locator)
        if not visible:
            Select(locator).select_by_text(value)
        else:
            Select(locator).select_by_visible_text(value)

    
    @staticmethod   #@staticmethod 静态方法只是名义上归属类管理，但是不能使用类变量和实例变量，是类的工具包
    @get_time      #计算查找元素的时间（使用隐性等待等待页面加载完成后定位）
    def find_element(driver, locator, more=False, timeout=1):
        driver.implicitly_wait(10)
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

    def move_to_element(self, locator):
        ActionChains(self.driver).move_to_element(self.find_element(self.driver, locator)).perform()

    # def autologin(self, locator1, locator2):
    #     telephone = '181'+''.join(str(random.choice(range(10))) for _ in range(8))
    #     payload = {"telephone": telephone}
    #     r = requests.post('https://your_website/your_api/code', data = payload)
    #     dic = r.json()
    #     code = dic['data']['code']
    #     self.sleep(3)
    #     self.send_keys(locator1, telephone)
    #     self.send_keys(locator2, code)

    def move_jindutiao(self, locator):
        self.driver.execute_script("arguments[0].scrollIntoView();", PageObject.find_element(self.driver, locator))

    # 鼠标悬停
    def xuanting(self, locator):
        el = self.find_element(self.driver, locator)
        ActionChains(self.driver).move_to_element(el).perform()

    def get_text(self,locator):
        '''获取文本'''
        element =self.find_element(self.driver, locator)
        log.info(element.text)
        return element.text

    def keyboard(self, locator, operation):

        ''' 键盘事件，operation=模拟的键盘值 Keys. '''
        operation=operation.upper()
        keywords={
          "BACK_SPACE":Keys.BACK_SPACE,
          "ENTER":Keys.ENTER,
          "CONTROL":Keys.CONTROL,
          "TAB":Keys.TAB,
          "ESCAPE":Keys.ESCAPE,
          "PAGE_UP":Keys.PAGE_UP,
          "PAGE_DOWN":Keys.PAGE_DOWN,
        }
        operation=keywords.get(operation)              
        try:
            self.send_keys(locator, operation)
        except BaseException as e:
            raise AssertionError("键盘事件异常！ Reason:{}".format(e))

    def js_execute(self,js):
        '''执行js'''
        js_value=self.driver.execute_script(js)

        return js_value

    def get_screenshot(self,title):
        """截图操作"""
        date=time.strftime('%Y-%m-%d',time.localtime(time.time()))

        self.driver.save_screenshot('{}{}.png'.format(date,title))
        return "截图成功"

    def drag_and_drop(self,locator,locator1):
        '''拖拽页面元素到另一个元素位置'''
        try:
            source=self.find_element(self.driver, locator)
            target=self.find_element(self.driver, locator1)
            action=ActionChains(self.driver)
            action.click_and_hold(source)
            action.pause(2)
            # ActionChains(self.driver).drag_and_drop(source,target).perform()
            action.move_to_element(target)
            action.release(target)
            action.perform()

        except :
            raise AssertionError("拖拽元素没有找到" )

    def drag_and_drop_by_offset(self,locator, xoffset, yoffset):
        '''拖拽页面元素到另一个指定位置'''
        try:
            source=self.find_element(self.driver, locator)
            ActionChains(self.driver).drag_and_drop_by_offset(source,xoffset,yoffset).perform()
        except :
            raise AssertionError("拖拽元素没有找到" )


    def drag_by_pyautogui(self,locator,locator1):
        source=self.find_element(self.driver, locator)
        target=self.find_element(self.driver, locator1)
        pyautogui.FAILSAFE = False
        pyautogui.moveTo(source.location['x']+20,source.location['y']+125)
        pyautogui.dragTo(target.location['x']+20,target.location['y']+155,duration=1)


    def assert_elemet(self,locator,expect_text):
        '''检查指定元素文本——包含'''
        actual_text=self.get_text(locator)
        if expect_text in actual_text:
            return True
        else:
            raise AssertionError('断言不通过，预期结果为["' + expect_text + '"]，但实际结果为["' + actual_text + '"]')


    def assert_title(self,title):
        '''断言页面标题'''
        actual_title=self.driver.title
        print(actual_title)
        if title in actual_title:
            return True
        else:
            raise AssertionError('断言不通过，预期结果为["' + title + '"]，但实际结果为["' + actual_title + '"]')

    def assert_url(self,except_url):
        '''断言页面url'''
        if self.driver.current_url.endswith(str(except_url)):
            return True
        else:
            raise AssertionError('断言不通过，预期结果为["' + except_url + '"]，但实际结果为["' + self.driver.current_url + '"]')

    def drag_and_drop1(self,locator,locator1):
        '''拖拽页面元素到另一个元素位置方案2'''
        source=self.find_element(self.driver, locator)
        target=self.find_element(self.driver, locator1)
        action=ActionChains(self.driver)
        action.click_and_hold(source)
        action.pause(2)
        action.move_to_element(target)
        action.release(target)
        action.perform()

if __name__=='__main__':
    PageObject().drag_and_drop()