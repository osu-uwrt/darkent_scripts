import cv2
import glob
import os
import random
import numpy as np
from tqdm import tqdm

def applyAlphaImage(back, fore):
    alpha = fore[:, :, 3] / 255.0
    final = np.zeros((outH, outW, 3), np.uint8)
    final[:, :, 0] = fore[:, :, 0] * alpha + back[:, :, 0] * (1-alpha)
    final[:, :, 1] = fore[:, :, 1] * alpha + back[:, :, 1] * (1-alpha)
    final[:, :, 2] = fore[:, :, 2] * alpha + back[:, :, 2] * (1-alpha)
    return final

outW = 644
outH = 482
inPath = "simulation/rendered_images/"
outPath = "data/simulated/"
negatives = glob.glob("data/negatives/*.jpg")
random.shuffle(negatives)

for imagePath in tqdm(glob.glob(inPath + "*.png")):
    if "_roi" in imagePath or "_obstruction" in imagePath:
        continue
    name = os.path.split(imagePath)[-1].split(".")[0]
    
    image = cv2.imread(imagePath, cv2.IMREAD_UNCHANGED)
    rect = cv2.boundingRect(cv2.split(image)[3])
    image = image[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]

    roiPath = inPath+name+"_roi.png"
    obstructed = False
    roiExists = False
    if os.path.exists(roiPath):
        roiExists = True
        obstructionPath = inPath+name+"_obstruction.png"
        roi = cv2.imread(roiPath, cv2.IMREAD_UNCHANGED)
        obstruction = cv2.imread(obstructionPath, cv2.IMREAD_UNCHANGED)
        roi = roi[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
        obstruction = obstruction[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]

        _,roi_thresh = cv2.threshold(cv2.cvtColor(roi, cv2.COLOR_BGRA2GRAY), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        _,obstruction_thresh = cv2.threshold(cv2.cvtColor(obstruction, cv2.COLOR_BGRA2GRAY), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        obstructed = cv2.countNonZero(obstruction_thresh) < cv2.countNonZero(roi_thresh) / 2
    
    alpha = image[:, :, 3] / 255.0

    for i in range(10):
        # Load image
        backgroundPath = negatives.pop(0)
        background = cv2.imread(backgroundPath)
        background = cv2.resize(background, (outW, outH))
        
        # Generate randomization rotation and translation
        roll = random.uniform(-180, 180)
        baseScale = outH * outW / (image.shape[0] * image.shape[1])
        scaleModifier = random.uniform(-0.1, -.9)
        tf = cv2.getRotationMatrix2D((rect[2]//2, rect[3]//2), roll, baseScale * 10 ** scaleModifier)
        tf[0,2] += random.randint(-outW // 3, outW // 3)
        tf[1,2] += random.randint(-outH // 3, outH // 3)
        imageTransformed = cv2.warpAffine(image, tf, (outW, outH))

        # Generate random blur
        blurAmount = random.randint(1, 3)
        blurKernelSize = (blurAmount, blurAmount)

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
        final = cv2.blur(final, blurKernelSize)
        final = applyAlphaImage(final, fog)
        final = applyAlphaImage(final, noise)
        
        bbox = (0,0,0,0)
        if not obstructed:
            if roiExists:
                obstructionTransformed = cv2.warpAffine(obstruction_thresh, tf, (outW, outH))
                bbox = cv2.boundingRect(obstructionTransformed)
            else:
                bbox = cv2.boundingRect(cv2.split(imageTransformed)[3])
        
        cv2.imwrite(outPath + name + "_%d.jpg" % i, final)
        with open(outPath + name + "_%d.txt" % i, 'w+') as labelFile:
            if not bbox[2] == 0 and not bbox[3] == 0:
                x = (bbox[0] + bbox[2] / 2) / outW
                y = (bbox[1] + bbox[3] / 2) / outH
                w = bbox[2] / outW
                h = bbox[3] / outH
                labelFile.write("0 %f %f %f %f\n" % (x, y, w, h))

        pass
    pass