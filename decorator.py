import os
from image_extend import Appium_Extend
from time import sleep, time


def time_decorator(function):  # 时间花费修饰器
    def wrapper():
        start_time = time()
        function()
        print('time=' + str((time() - start_time)) + 's')
        print('--------------------------')
    return wrapper

#def log_decorator()

"""
暂时保留修饰器
"""
# def pre_image_verify_decorator(*args):  # 脚本调用图片验证decorator
#     image_path = os.path.join(PATH, 'image', args[0])
#     secs = args[1]
#
#     def decorator(function):
#         def wrapper():
#             result = False
#             sec = 0
#             while result == False:
#                 sleep(1)
#                 extend = Appium_Extend(driver)
#                 element = driver.find_element_by_class_name(
#                     "android.widget.FrameLayout")
#                 load = extend.load_image(image_path)
#                 result = extend.get_screenshot_by_element(
#                     element).same_as(load, 10)
#                 if result:
#                     print('info:前置验证通过')
#                 else:
#                     if sec <= secs:
#                         print('.')
#                         sec += 1
#                     else:
#                         print('info:前置验证超时')
#                         break
#             function()
#             print('--------------------------')
#         return wrapper
#     return decorator
#
#
# def after_image_verify_decorator(*args):  # 脚本调用后置图片验证decorator
#     image_path = os.path.join(PATH, 'image', args[0])
#     secs = args[1]
#
#     def decorator(function):
#         def wrapper():
#             function()
#             result = False
#             sec = 0
#             while not result:
#                 sleep(1)
#                 extend = Appium_Extend(driver)
#                 element = driver.find_element_by_class_name(
#                     "android.widget.FrameLayout")
#                 load = extend.load_image(image_path)
#                 result = extend.get_screenshot_by_element(
#                     element).same_as(load, 10)
#                 if result:
#                     print('info:结果验证通过')
#                 else:
#                     if sec <= secs:
#                         print('.')
#                         sec += 1
#                     else:
#                         print('info:结果验证超时')
#                         break
#             print('--------------------------')
#         return wrapper
#     return decorator
