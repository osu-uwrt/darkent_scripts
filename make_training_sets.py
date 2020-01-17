#!/usr/bin/env python3

import glob 
import os
import random

images = sorted(glob.glob("data/**/*.jpg", recursive=True))
videos = {}
for imagePath in images:
    if os.path.exists(imagePath.replace(".jpg", ".txt")):
        imageName = os.path.basename(imagePath)
        videoName = "_".join(imageName.split("_")[:-1])
        if not videoName in videos:
            videos[videoName] = []
        videos[videoName].append(imagePath) 

trainingData = []
testData = []
for imageList in videos.values():
    trainingImages = imageList
    testImages = []
    i = random.randint(0, len(trainingImages))
    for _ in range(len(trainingImages) // 10):
        if i == len(trainingImages) - 1:
            i = 0
        image = trainingImages.pop(i)
        testImages.append(image)
    trainingData += trainingImages
    testData += testImages

with open(os.path.expanduser("~/darknet/data/train.txt"), "w") as trainFile:
    trainFile.writelines(os.path.abspath(image) + "\n" for image in trainingData)

with open(os.path.expanduser("~/darknet/data/test.txt"), "w") as testFile:
    testFile.writelines(os.path.abspath(image) + "\n" for image in testData)
