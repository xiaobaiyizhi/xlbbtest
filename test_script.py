import os
from image_extend import Appium_Extend
from time import sleep, time
from appium import webdriver


def time_decorator(function):  # 时间花费修饰器
    def wrapper():
        start_time = time()
        function()
        print('time=' + str((time() - start_time)) + 's')
        print('--------------------------')
    return wrapper


def wait_by_image(image_name, seconds):
    image_path = os.path.join(PATH, 'image', image_name)
    result = False
    sec = 0
    while result == False:
        sleep(1)
        extend = Appium_Extend(driver)
        element = driver.find_element_by_class_name(
            "android.widget.FrameLayout")
        load = extend.load_image(image_path)
        result = extend.get_screenshot_by_element(
            element).same_as(load, 10)
        if result:
            return "pass"
        else:
            if sec <= seconds:
                print('.')
                sec += 1
            else:
                return "timeout"


def pre_image_verify_decorator(*args):  # 脚本调用图片验证验证
    image_path = os.path.join(PATH, 'image', args[0])
    secs = args[1]

    def decorator(function):
        def wrapper():
            result = False
            sec = 0
            while result == False:
                sleep(1)
                extend = Appium_Extend(driver)
                element = driver.find_element_by_class_name(
                    "android.widget.FrameLayout")
                load = extend.load_image(image_path)
                result = extend.get_screenshot_by_element(
                    element).same_as(load, 10)
                if result:
                    print('info:前置验证通过')
                else:
                    if sec <= secs:
                        print('.')
                        sec += 1
                    else:
                        print('info:前置验证超时')
                        break
            function()
            print('--------------------------')
        return wrapper
    return decorator


def after_image_verify_decorator(*args):  # 脚本调用后置图片验证
    image_path = os.path.join(PATH, 'image', args[0])
    secs = args[1]

    def decorator(function):
        def wrapper():
            function()
            result = False
            sec = 0
            while not result:
                sleep(1)
                extend = Appium_Extend(driver)
                element = driver.find_element_by_class_name(
                    "android.widget.FrameLayout")
                load = extend.load_image(image_path)
                result = extend.get_screenshot_by_element(
                    element).same_as(load, 10)
                if result:
                    print('info:结果验证通过')
                else:
                    if sec <= secs:
                        print('.')
                        sec += 1
                    else:
                        print('info:结果验证超时')
                        break
            print('--------------------------')
        return wrapper
    return decorator

PATH = os.path.dirname(__file__)

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['deviceName'] = '71MBBLN23KT8'
desired_caps['platformVersion'] = '4.4.4'
desired_caps['deviceName'] = 'xiaobai'
desired_caps['appPackage'] = 'com.baplay.gd.wp'
desired_caps['appActivity'] = 'com.baplay.gd.wp.UnityPlayerActivity'
global driver
driver = webdriver.Remote('http://172.16.40.20:4723/wd/hub', desired_caps)


@time_decorator
@pre_image_verify_decorator('1.png', 10)
# 打开app到第一屏
def step1():
    driver.tap([(540, 1560), ])
    wait_by_image('wait1.png', 8)
    driver.tap([(540, 1628), ])


@time_decorator
@pre_image_verify_decorator('2.png', 12)
def step2():
    driver.tap([(458, 693), ])


@time_decorator
@after_image_verify_decorator('aft1.png', 5)
@pre_image_verify_decorator('pre1.png', 3)
# 打开app到第一屏
def step3():
    print('选择稍后再说')
    driver.tap([(170, 1500), ])
    wait_by_image('wait2.png',6)
    print('点击进入游戏')
    driver.tap([(540, 1762), ])


step1()
step2()
step3()
