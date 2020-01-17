#!/usr/bin/env python3

import glob 
import random
import cv2

images = sorted(glob.glob("data/**/*.jpg", recursive=True))
i = random.randint(0, len(images))
while True:
    img = cv2.imread(images[i])
    for line in open(images[i].replace(".jpg", ".txt")):
        classId, x, y, w, h = [float(n) for n in line.split(" ")]
        x = int(x * img.shape[1])
        y = int(y * img.shape[0])
        w = int(w * img.shape[1])
        h = int(h * img.shape[0])
        img = cv2.rectangle(img, (x-w//2, y-h//2), (x+w//2, y+h//2), (0, 0, 255))
    cv2.imshow("Data", img)
    cv2.waitKey()
    i += 1