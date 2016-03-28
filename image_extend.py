import os
import tempfile
import shutil
from functools import reduce
from matplotlib import pyplot as plt
import cv2
from PIL import Image
import numpy as np



PATH = lambda p: os.path.abspath(p)
TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")


class Appium_Extend(object):

    def __init__(self, driver):
        self.driver = driver

    # 根据element名称获取截图
    def get_screenshot_by_element(self, element):
        self.driver.get_screenshot_as_file(TEMP_FILE)
        location = element.location
        size = element.size
        box = (
            location['x'],
            location['y'],
            location['x'] +
            size['width'],
            location['y'] +
            size['height'])

        image = Image.open(TEMP_FILE)
        newimage = image.crop(box)
        newimage.save(TEMP_FILE)

        return newimage

    # 自定义截图
    def get_screenshot_by_custom_size(self, start_x, start_y, end_x, end_y):
        self.driver.get_screenshot_as_file(TEMP_FILE)
        box = (start_x, start_y, end_x, end_y)

        image = Image.open(TEMP_FILE)
        newimage = image.crop(box)
        newimage.save(TEMP_FILE)

        return newimage

    # 全屏幕截图
    def get_screenshot_by_full_size(self):
        self.driver.get_screenshot_as_file(TEMP_FILE)
        newimage = Image.open(TEMP_FILE)
        return newimage

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
    def same_as(self, temp_image, load_image, percent):
        image1 = temp_image
        image2 = load_image
        #os.startfile(TEMP_FILE)
        #os.startfile("D:/py/xlbbtest/xlbbtest/loginimage/2.png")
        im1_hash = self.avhash(image1)
        im2_hash = self.avhash(image2)
        h = self.hamming(im1_hash, im2_hash)
        if h <= percent:
            print('info:汉明距离：'+str(h))
            return True
        else:
            return False

    # 模板匹配函数
    def template_match(self, whole_image, part_image):

        image1 = cv2.imread(whole_image, 0)

        template_image = cv2.imread(part_image, 0)
        w, h = template_image.shape[::-1]

        res = cv2.matchTemplate(image1, template_image, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        print(max_val)
        print(max_loc)
        if len(os.path.split(part_image)[1].split('.')[0]) ==  2:
            threshold = 6000000
        else:
            threshold = 9000000
        if max_val >= threshold:  # 阈值设置 临时解决办法
            top_left = max_loc
        else:
            return 0, 0

        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(image1, top_left, bottom_right, 255, 2)
        #debug专用
        # plt.subplot(121), plt.imshow(res, cmap='gray')
        # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        # plt.subplot(122), plt.imshow(image1, cmap='gray')
        # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        # #plt.suptitle(meth)

        plt.show()
        return top_left[0]+w/2, top_left[1]+h/2  # 返回模板中心点坐标


    def sift_match(self,whole_image, part_image):
        MIN_MATCH_COUNT = 10  #匹配点阈值

        img1 = cv2.imread(part_image)
        img2 = cv2.imread(whole_image)
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        sift = cv2.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)

        # FLANN_INDEX_KDTREE = 0

        # index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        # search_params = dict(checks=50)

        flann = cv2.BFMatcher()
        matches = flann.knnMatch(des1, des2, k=2)

        # store all the good matches as per Lowe's ratio test.
        good = []
        for m, n in matches:
            if m.distance < 0.7*n.distance:
                good.append(m)


        if len(good)>MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            # matchesMask = mask.ravel().tolist()
            w, h = img1.shape

            pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)
            x = np.int32(dst)[0][0][0] + int(w)/2
            y = np.int32(dst)[0][0][1] + int(h)/2
            return x, y
            #plt.imshow(img2),plt.show()
        else:

            # matchesMask = None
            return 0, 0

        # draw_params = dict(matchColor = (0,255,0), # draw matches in green color
        #                    singlePointColor = None,
        #                    matchesMask = matchesMask, # draw only inliers
        #                    flags = 2)
        #
        # img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
        #
        #
        #
        # plt.imshow(img3),plt.show()

    # 初始话结果矩阵

        #直方图比较算法
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
        # 图片分割
    # def split_image(self, img, part_size=(64, 64)):
    #     w, h = img.size
    #     pw, ph = part_size
    #     assert w % pw == h % ph == 0
    #     return [img.crop((i, j, i + pw, j + ph)).copy()
    #             for i in range(0, w, pw)
    #             for j in range(0, h, ph)]

    # 图片直方图对比
    # def hist_similar(self, lh, rh):
    #     return sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r))
    #                for l, r in zip(lh, rh)) / len(lh)

