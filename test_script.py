import os
from image_extend import  Appium_Extend
from time import sleep, time
from appium import webdriver

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['deviceName'] = '71MBBLN23KT8'
desired_caps['platformVersion'] = '4.4.4'
desired_caps['deviceName'] = 'xiaobai'
desired_caps['appPackage'] = 'com.baplay.gd.wp'
desired_caps['appActivity'] = 'com.baplay.gd.wp.UnityPlayerActivity'
driver = webdriver.Remote('http://172.16.40.20:4723/wd/hub', desired_caps)
sleep(15)
driver.tap([(540, 1560), ])
starttime = time()
while True:
    el = driver.find_elements_by_android_uiautomator(
        'new UiSelector().text("登 入")')
    sleep(1)
    if el:
        break
speet = time() - starttime
print('进入时间为：' + str(speet))
driver.tap([(540, 1620), ])
sleep(3)
print('成功进入登录页面')
print('开始测试免注册登录')
driver.tap([(458, 693), ])
sleep(3)
print('选择稍后再说')
driver.tap([(170, 1500), ])
sleep(10)
print('点击进入游戏')
extend = Appium_Extend(driver)
element = driver.find_element_by_class_name("android.view.View")
load = extend.load_image("D:/py/xlbbtest/xlbbtest/loginimage/1.png")
result = extend.get_screenshot_by_element(element).same_as(load, 0.8)
if result:
    print("相似度验证通过"+str(result))
    print("点击进入游戏"+str(result))
    driver.tap([(513, 1768), ])
    sleep(3)
    driver.tap([(513, 1768), ])
