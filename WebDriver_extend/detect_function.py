import os
from time import sleep
from config import PATH
from appium.webdriver.webdriver import WebDriver
from image_extend import Appium_Extend



class WebDriver_extend(WebDriver):

    def wait_by_image(self, image_name, max_wait):
        image_path = os.path.join(PATH, 'image', image_name)
        result = False
        sec = 0
        while result == False:
            sleep(1)
            extend = Appium_Extend(self)
            #element = driver.find_element_by_class_name("android.widget.FrameLayout")
            self.get_screenshot_as_file(os.path.join(PATH, 'image', 'temp_shot.png'))
            load = extend.load_image(image_path)
            temp = extend.load_image(os.path.join(PATH, 'image', 'temp_shot.png'))
            result = extend.same_as(temp, load, 10)
            if result:
                return "pass"
            else:
                if sec <= max_wait:
                    print('.')
                    sec += 1
                    print(str(sec))
                else:
                    return "timeout"

    def wait_by_element_image(self, element_image, max_wait=5):
        image_path = os.path.join(PATH, 'image', element_image)
        result = False
        sec = 0
        while result == False:
            sleep(1)
            extend = Appium_Extend(self)
            #element = driver.find_element_by_class_name("android.widget.FrameLayout")
            self.get_screenshot_as_file(os.path.join(PATH, 'image', 'temp_shot.png'))
            load = image_path
            temp = os.path.join(PATH, 'image', 'temp_shot.png')
            x, y = extend.template_match(temp, load)
            if x != 0 or y != 0:
                return "pass"
            else:
                if sec <= max_wait:
                    print('.')
                    sec += 1
                    print(str(sec))
                else:
                    return "timeout"


    def result_image_verify(self, image_name, result_filename, max_wait=5):  # 结果校验
        image_path = os.path.join(PATH, 'image', image_name)
        result = False
        sec = 0
        while not result:
            sleep(1)
            extend = Appium_Extend(self)
            self.get_screenshot_as_file(os.path.join(PATH, 'image', 'temp_shot.png'))
            temp = extend.load_image(os.path.join(PATH, 'image', 'temp_shot.png'))
            load = extend.load_image(image_path)
            result = extend.same_as(temp, load, 10)
            if result:
                print('info:结果验证通过')
                temp.save(os.path.join(PATH, 'result', result_filename))
            else:
                if sec <= max_wait:
                    print('.')
                    sec += 1
                else:
                    print('info:结果验证超时')
                    break
        print('--------------------------')
