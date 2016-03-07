import os
import tempfile
import shutil
import glob
import sys
from functools import reduce

from PIL import Image

PATH = lambda p: os.path.abspath(p)
TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")


class Appium_Extend(object):

    def __init__(self, driver):
        self.driver = driver

    # 获取整个屏幕
    def get_screenshot_by_element(self, element):
        self.driver.get_screenshot_as_file(TEMP_FILE)

        # 获取元素
        location = element.location
        size = element.size
        box = (
            location['x'],
            location['y'],
            location['x'] +
            size['width'],
            location['y'] +
            size['height'])

        # 获取图片
        image = Image.open(TEMP_FILE)
        newimage = image.crop(box)
        newimage.save(TEMP_FILE)

        return self

    # 自定义截图
    def get_screenshot_by_custom_size(self, start_x, start_y, end_x, end_y):
        self.driver.get_screenshot_as_file(TEMP_FILE)
        box = (start_x, start_y, end_x, end_y)

        image = Image.open(TEMP_FILE)
        newimage = image.crop(box)
        newimage.save(TEMP_FILE)

        return self

    # 将截屏文件复制到指定目录
    def write_to_file(self, dirpath, imagename, form='png'):
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
        shutil.copyfile(
            TEMP_FILE,
            PATH(
                dirpath +
                "/" +
                imagename +
                "." +
                form))

    # 加载目标文件
    def load_image(self, image_path):
        if os.path.isfile(image_path):
            load = Image.open(image_path)
            return load
        else:
            raise Exception("%s is not exist" % image_path)

    # 图片分割
    def split_image(self, img, part_size=(64, 64)):
        w, h = img.size

        pw, ph = part_size

        assert w % pw == h % ph == 0

        return [img.crop((i, j, i + pw, j + ph)).copy()

                for i in range(0, w, pw)

                for j in range(0, h, ph)]

    # 图片直方图对比
    def hist_similar(self, lh, rh):
        return sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r))
                   for l, r in zip(lh, rh)) / len(lh)

    def avhash(self, im):
        im = im.resize((8, 8), Image.ANTIALIAS).convert('L')
        avg = reduce(lambda x, y: x + y, im.getdata()) / 64
        return reduce(lambda x, y_z: x | (y_z[1] << y_z[0]),
               enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())),
               0)

    def hamming(self, h1, h2):
        h, d = 0, h1 ^ h2
        while d:
            h += 1
            d &= d-1
        return h


    # 对比图片
    def same_as(self, load_image, percent):
        image1 = Image.open(TEMP_FILE)
        image2 = load_image
        #os.startfile(TEMP_FILE)
        #os.startfile("D:/py/xlbbtest/xlbbtest/loginimage/2.png")
        im1_hash=self.avhash(image1)
        im2_hash=self.avhash(image2)
        h=self.hamming(im1_hash, im2_hash)
        # li = image1.resize((256, 256)).convert('RGB')
        # ri = image2.resize((256, 256)).convert('RGB')
        # differ1 = self.hist_similar(image1.histogram(), image2.histogram())
        # print(str(differ1))
        # differ = sum(
        #     self.hist_similar(
        #         l.histogram(), r.histogram()) for l, r in zip(
        #         self.split_image(li), self.split_image(ri))) / 16.0
        # print(str(differ))
        #differ = sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)
        # differ = math.sqrt(reduce(operator.add,  list(map(lambda a,b: (a-b)**2,  histogram1, histogram2)))/len(histogram1) )
        if h <= percent:
            print('info:汉明距离：'+str(h))
            return True
        else:
            return False
