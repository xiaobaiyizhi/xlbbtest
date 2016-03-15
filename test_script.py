import os
from image_extend import Appium_Extend
from time import sleep, time
from appium import webdriver
import image_template_match
from decorator import time_decorator


#CURRENT_SCREEN_SHOT = driver.get_screenshot_as_file('current_screen.png')
def pre_image_verify_decorator(*args):  # 脚本调用图片验证decorator
    image_path = os.path.join(PATH, 'image', args[0])
    secs = args[1]

    def decorator(function):
        def wrapper():
            result = False
            sec = 0
            while result == False:
                sleep(1)
                extend = Appium_Extend(driver)
                driver.get_screenshot_as_file(os.path.join(PATH, 'image', 'temp_shot.png'))
                load = extend.load_image(image_path)
                temp = extend.load_image(os.path.join(PATH, 'image', 'temp_shot.png'))
                load = extend.load_image(image_path)
                result = extend.same_as(temp, load, 10)
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


def after_image_verify_decorator(*args):  # 脚本调用后置图片验证decorator
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
                driver.get_screenshot_as_file(os.path.join(PATH, 'image', 'temp_shot.png'))
                load = extend.load_image(image_path)
                temp = extend.load_image(os.path.join(PATH, 'image', 'temp_shot.png'))
                load = extend.load_image(image_path)
                result = extend.same_as(temp, load, 10)
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



def wait_by_image(image_name, seconds):
    image_path = os.path.join(PATH, 'image', image_name)
    result = False
    sec = 0
    while result == False:
        sleep(1)
        extend = Appium_Extend(driver)
        #element = driver.find_element_by_class_name("android.widget.FrameLayout")
        driver.get_screenshot_as_file(os.path.join(PATH, 'image', 'temp_shot.png'))
        load = extend.load_image(image_path)
        temp = extend.load_image(os.path.join(PATH, 'image', 'temp_shot.png'))
        result = extend.same_as(temp, load, 10)
        if result:
            return "pass"
        else:
            if sec <= seconds:
                print('.')
                sec += 1
                print(str(sec))
            else:
                return "timeout"



PATH = os.path.dirname(__file__)

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['deviceName'] = 'device'
desired_caps['platformVersion'] = '4.3'
desired_caps['deviceName'] = 'xiaobai'
desired_caps['appPackage'] = 'com.baplay.gd.wp'
desired_caps['appActivity'] = 'com.baplay.gd.wp.UnityPlayerActivity'
global driver
driver = webdriver.Remote('http://172.16.40.20:4723/wd/hub', desired_caps)


@time_decorator
@pre_image_verify_decorator('pre_1.png', 10)
@after_image_verify_decorator('aft_1.png', 5)
# 打开app到第一屏
def step1():
    driver.tap([(540, 1460), ])
    wait_by_image('wait1.png', 8)
    print()
    driver.tap([(540, 1528), ])
    wait_by_image('wait2.png', 5)
    driver.tap([(458, 700), ])
    sleep(2)
    wait_by_image('wait5.png', 4)
    driver.tap([(458, 593), ])
    wait_by_image('wait3.png', 5)

    sleep(2)
    driver.tap([(630, 1500), ])
    sleep(1)
    while 1:
        driver.get_screenshot_as_file(os.path.join(PATH, 'image', 'temp_shot.png'))
        x, y = image_template_match.template_match('temp_shot.png', 's4.png')
        if x == 0 and y == 0:
            driver.swipe(630, 1500, 630, 1100, 2000)
            sleep(2)
        else:
            break

    sleep(2)
    starttime = time()

    print('校验时间'+str(starttime-time()))
    driver.tap([(x, y), ])
    sleep(2)
    print('点击进入游戏')
    driver.tap([(540, 1662), ])
    wait_by_image('wait4.png', 8)

    driver.tap([(100, 250), ])
    sleep(1)
    driver.tap([(100, 250), ])
    sleep(1)

step1()
