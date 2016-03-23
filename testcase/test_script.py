import os
from image_extend import Appium_Extend
from time import sleep, time
from decorator import time_decorator
import WebDriver_extend
import linecache
from base_config import PATH
from basemethod.base_xlwt import write_xls


#
# import unittest
# class Search(unittest.TestCase):
#     def setUp(self):
#         pass
#     def test_s(self):
#         pass
#     def tearDown(self):
#         pass
#
#
# if __name__ == '__main__':
#     unittest.main()


#CURRENT_SCREEN_SHOT = driver.get_screenshot_as_file('current_screen.png')
def pre_image_verify_decorator(*args):  # 脚本调用图片验证decorator
    image_path = os.path.join(PATH, 'image', args[0])
    secs = args[1]

    def decorator(function):
        def wrapper(*args, **kwargs):
            result = False
            sec = 0
            while result == False:
                sleep(1)
                extend = Appium_Extend(driver)
                driver.get_screenshot_as_file(os.path.join(PATH, 'image', 'temp_shot.png'))
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
            function(*args, **kwargs)
            print('--------------------------')
        return wrapper
    return decorator


@time_decorator
@pre_image_verify_decorator('pre_1.png', 10)
# 打开app到第一屏
def step1(server):
    driver.tap([(540, 1460), ])
    driver.wait_by_image('wait1.png', 8)
    print()
    driver.tap([(540, 1528), ])
    driver.wait_by_image('wait2.png', 5)
    driver.tap([(458, 700), ])
    sleep(2)
    driver.wait_by_image('wait5.png', 4)
    driver.tap([(458, 593), ])
    driver.wait_by_image('wait6.png', 3)
    driver.tap([(44, 40), ])
    driver.wait_by_element_image('center.png', 10)

    sleep(2)
    driver.tap([(630, 1500), ])
    sleep(1)
    while 1:
        driver.get_screenshot_as_file(os.path.join(PATH, 'image', 'temp_shot.png'))
        server_iamge_path = server+'.png'
        extend = Appium_Extend(driver)
        x, y = extend.template_match(os.path.join(PATH, 'image', 'temp_shot.png'), os.path.join(PATH, 'image', server_iamge_path))
        if x == 0 and y == 0:
            driver.swipe(630, 1380, 630, 1050, 2000)
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
    driver.wait_by_image('wait4.png', 8)

    driver.tap([(100, 250), ])
    sleep(1)
    driver.tap([(100, 250), ])
    sleep(1)
    driver.result_image_verify('aft_1.png', servercode+'.png')




def read_script_config(config_path):
    config_data=[]
    config_data.append(linecache.getline(config_path, 1).strip().split('=')[1].split(','))# 获取server
    config_data.append(linecache.getline(config_path, 2).strip().split('=')[1].strip(','))# 获得登录方式
    return config_data


config_data = read_script_config('script_config.txt')

for servercode in config_data[0]:
    print(servercode)
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['deviceName'] = 'device'
    desired_caps['platformVersion'] = '4.3'
    desired_caps['deviceName'] = '192.168.56.101:5555'
    desired_caps['appPackage'] = 'com.baplay.gd.wp'
    desired_caps['appActivity'] = 'com.baplay.gd.wp.UnityPlayerActivity'
    global driver
    #driver = webdriver.Remote('http://172.16.40.20:4723/wd/hub', desired_caps)
    driver = WebDriver_extend.Remote('http://172.16.40.20:4723/wd/hub', desired_caps)
    step1(servercode)
    driver.close_app()
    driver.quit()

result_table = []
result_table = [['server', 'time']]
with open(os.path.join(PATH, 'result', 'result_temp.txt'), 'r') as f:
    for servercode in config_data[0]:
        server_time = f.readline().strip('\n')
        result_table.append([servercode, server_time])

write_xls(os.path.join(PATH, 'result', 'login.xls'), result_table)

