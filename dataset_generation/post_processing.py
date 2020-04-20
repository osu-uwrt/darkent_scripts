import cv2
import glob
import os
import random
import numpy as np

def applyAlphaImage(back, fore):
    alpha = fore[:, :, 3] / 255.0
    final = np.zeros((outH, outW, 3), np.uint8)
    final[:, :, 0] = fore[:, :, 0] * alpha + back[:, :, 0] * (1-alpha)
    final[:, :, 1] = fore[:, :, 1] * alpha + back[:, :, 1] * (1-alpha)
    final[:, :, 2] = fore[:, :, 2] * alpha + back[:, :, 2] * (1-alpha)
    return final

outW = 644
outH = 482
path = "dataset_generation/rendered_images/"
negatives = glob.glob("negatives/*.jpg")
random.shuffle(negatives)

for roiPath in glob.glob(path + "*_roi.png"):
    name = os.path.split(roiPath)[-1].split("_")[0]
    imagePath = path+name+".png"
    obstructionPath = path+name+"_obstruction.png"
    image = cv2.imread(imagePath, cv2.IMREAD_UNCHANGED)
    rect = cv2.boundingRect(cv2.split(image)[3])
    roi = cv2.imread(roiPath, cv2.IMREAD_UNCHANGED)
    obstruction = cv2.imread(obstructionPath, cv2.IMREAD_UNCHANGED)
    image = image[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
    roi = roi[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
    obstruction = obstruction[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]

    _,roi_thresh = cv2.threshold(cv2.cvtColor(roi, cv2.COLOR_BGRA2GRAY), 128, 255, cv2.THRESH_BINARY)
    _,obstruction_thresh = cv2.threshold(cv2.cvtColor(obstruction, cv2.COLOR_BGRA2GRAY), 128, 255, cv2.THRESH_BINARY)
    obstructed = cv2.countNonZero(obstruction_thresh) < cv2.countNonZero(roi_thresh) / 2
    alpha = image[:, :, 3] / 255.0

    for _ in range(90):
        # Load image and crop out black or white sections
        backgroundPath = negatives.pop(0)
        background = cv2.imread(backgroundPath)
        _, backgroundGray = cv2.threshold(cv2.cvtColor(background, cv2.COLOR_BGR2GRAY), 10, 255, cv2.THRESH_BINARY)
        backRect = list(cv2.boundingRect(backgroundGray))
        if np.average(backgroundGray[:3, 400:500]) > 240:
            backRect[1] += backRect[2] // 5
            backRect[3] -= backRect[2] // 5
        if backRect[2] != 0 or backRect[3] != 0:
            background = cv2.resize(background[backRect[1]:backRect[1]+backRect[3], backRect[0]:backRect[0]+backRect[2]], (outW, outH))
        else:
            background = cv2.resize(background, (outW, outH))
        
        # Generate randomization rotation and translation
        roll = random.uniform(-180, 180)
        baseScale = outH * outW / (image.shape[0] * image.shape[1])
        tf = cv2.getRotationMatrix2D((rect[2]//2, rect[3]//2), roll, baseScale * random.uniform(0.1, 0.9))
        tf[0,2] += random.randint(-outW // 2, outW // 2)
        tf[1,2] += random.randint(-outH // 2, outH // 2)
        imageTransformed = cv2.warpAffine(image, tf, (outW, outH))

        # Generate fog
        fogColorHSV = np.array([[[random.randint(70, 90), random.randint(0, 255), 255]]], np.uint8)
        fogColor = cv2.cvtColor(fogColorHSV, cv2.COLOR_HSV2BGR)[0,0]
        fog = np.ones((outH, outW, 4)) * 256
        fog[:, :, 0] = fogColor[0]
        fog[:, :, 1] = fogColor[1]
        fog[:, :, 2] = fogColor[2]
        fog[:, :, 3] = random.randint(0, 170)
        noise = np.random.random((outH, outW, 4)) * 256
        noise[:, :, 3] = random.randint(0, 64)

        final = applyAlphaImage(background, imageTransformed)
        final = applyAlphaImage(final, fog)
        final = applyAlphaImage(final, noise)
        

        obstructionTransformed = cv2.warpAffine(obstruction_thresh, tf, (outW, outH))
        bbox = (0,0,0,0)
        if not obstructed:
            bbox = cv2.boundingRect(obstructionTransformed)
        final = cv2.rectangle(final, (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3]), (0, 0, 255))

        cv2.imshow("Background", background)
        cv2.imshow("Final", final)
        cv2.waitKey()
        pass
    pass