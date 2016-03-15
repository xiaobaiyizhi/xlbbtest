import os
from time import sleep
from config import PATH
from image_extend import Appium_Extend


def wait_by_image(driver, image_name, seconds):
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

def after_image_verify_decorator(*args):  # 脚本调用后置图片验证decorator
    image_path = os.path.join(PATH, 'image', args[0])
    secs = args[1]

    def decorator(function):
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
            result = False
            sec = 0
            while not result:
                sleep(1)
                extend = Appium_Extend(driver)
                driver.get_screenshot_as_file(os.path.join(PATH, 'image', 'temp_shot.png'))
                temp = extend.load_image(os.path.join(PATH, 'image', 'temp_shot.png'))
                load = extend.load_image(image_path)
                result = extend.same_as(temp, load, 10)
                if result:
                    print('info:结果验证通过')
                    temp.save(os.path.join(PATH, 'result', 'success_image.png'))
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