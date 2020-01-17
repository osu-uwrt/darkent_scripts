#!/usr/bin/env python3

import glob 
import os
import random


trainingData = []
testData = []

print("Soring positives...")

# Find all positive frames in order
positiveImages = sorted(glob.glob("data/**/*.jpg", recursive=True))

# Sort frames into videos they came from
videos = {}
for imagePath in positiveImages:
    if os.path.exists(imagePath.replace(".jpg", ".txt")):
        imageName = os.path.basename(imagePath)
        videoName = "_".join(imageName.split("_")[:-1])
        if not videoName in videos:
            videos[videoName] = []
        videos[videoName].append(imagePath) 

# For each video, take one consecutive tenth of the video and make it test data
for imageList in videos.values():
    trainingImages = imageList
    testImages = []
    i = random.randint(0, len(trainingImages)-1)
    for _ in range(len(trainingImages) // 10):
        if i == len(trainingImages) - 1:
            i = 0
        image = trainingImages.pop(i)
        testImages.append(image)
    trainingData += trainingImages
    testData += testImages

print("Done!")



print("Sorting negatives...")

# Find all negative frames in order
negativeImages = sorted(glob.glob("negatives/**/*.jpg", recursive=True))

# We shouldnt have more negatives than positives
# Remove random frames until positive >= negative
while (len(positiveImages) <= len(negativeImages)):
    negativeImages.pop(random.randint(0, len(negativeImages)-1))

# Sort frames into videos they came from
videos = {}
for imagePath in negativeImages:
    if os.path.exists(imagePath.replace(".jpg", ".txt")):
        imageName = os.path.basename(imagePath)
        videoName = "_".join(imageName.split("_")[:-1])
        if not videoName in videos:
            videos[videoName] = []
        videos[videoName].append(imagePath) 

# For each video, take one consecutive tenth of the video and make it test data
for imageList in videos.values():
    trainingImages = imageList
    testImages = []
    i = random.randint(0, len(trainingImages)-1)
    for _ in range(len(trainingImages) // 10):
        if i == len(trainingImages) - 1:
            i = 0
        image = trainingImages.pop(i)
        testImages.append(image)
    trainingData += trainingImages
    testData += testImages


# Write list of frames to test and train files
with open(os.path.expanduser("~/darknet/data/train.txt"), "w") as trainFile:
    trainFile.writelines(os.path.abspath(image) + "\n" for image in trainingData)

with open(os.path.expanduser("~/darknet/data/test.txt"), "w") as testFile:
    testFile.writelines(os.path.abspath(image) + "\n" for image in testData)

print("Done!")