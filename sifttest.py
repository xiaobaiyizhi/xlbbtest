import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

starttime = time.time()
MIN_MATCH_COUNT = 10

img1 = cv2.imread('s3.png')
img2 = cv2.imread('search1.png')
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

sift = cv2.xfeatures2d.SIFT_create()
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

FLANN_INDEX_KDTREE = 0

index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.BFMatcher()
matches = flann.knnMatch(des1, des2, k=2)

# store all the good matches as per Lowe's ratio test.
good = []
for m, n in matches:
    if m.distance < 0.7*n.distance:
        good.append(m)


if len(good)>MIN_MATCH_COUNT:
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()

    h,w = img1.shape
    print(type(w))
    print(str(h))

    pts = np.float32([ [0, 0], [0, h-1], [w-1, h-1], [w-1, 0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts, M)
    w = np.int32(dst)[0][0][0] + int(w)/2
    h = np.int32(dst)[0][0][1] + int(h)/2
    print(str(time.time()-starttime))
    img2 = cv2.polylines(img2, [np.int32(dst)],True,255,3, cv2.LINE_AA)
    #plt.imshow(img2),plt.show()
else:

    matchesMask = None

draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 2)

img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)



plt.imshow(img3),plt.show()

print('asd')