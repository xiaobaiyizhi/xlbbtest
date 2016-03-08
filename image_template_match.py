from matplotlib import pyplot as plt
import os
import cv2

PATH = os.path.dirname(__file__)
image_path = os.path.join(PATH, 'image')


def template_match(whole_image='search1.png', part_image='s11.png'):  # 模板匹配函数
    whole_image_path = os.path.join(image_path, whole_image)
    image1 = cv2.imread(whole_image_path, 0)

    path_image_path = os.path.join(image_path, part_image)
    template_image = cv2.imread(path_image_path, 0)
    w, h = template_image.shape[::-1]

    res = cv2.matchTemplate(image1, template_image, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(max_val)
    print(max_loc)
    if max_val >= 6500000:  # 阈值设置
        top_left = max_loc
    else:
        return

    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(image1, top_left, bottom_right, 255, 2)

    plt.subplot(121), plt.imshow(res, cmap='gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(image1, cmap='gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    # plt.suptitle(meth)

    plt.show()

template_match()

# 初始话结果矩阵
