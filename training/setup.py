import glob 
import os
import cv2
from tqdm import tqdm
import argparse
import yaml
import random

def generateNegativeFrames():
    print("Generating negative frames from videos")
    # Find all negative videos
    videos = glob.glob("data/negatives/videos/*")

    # Break each video down into frames
    for video in tqdm(videos):
        videoName = os.path.basename(video)
        if len(glob.glob("data/negatives/%s_*.jpg" % videoName)) > 0:
            continue

        vidcap = cv2.VideoCapture(video)
        success,image = vidcap.read()
        count = 0
        while success:
            cv2.imwrite("data/negatives/%s_%05d.jpg" % (videoName, count), image)     # save frame as JPEG file    
            with open("data/negatives/%s_%05d.txt" % (videoName, count), "w"):
                pass  
            success,image = vidcap.read()
            count += 1

def copyTemplate(srcPath, dstPath):
    with open(srcPath, "r") as srcFile:
        fileContents = srcFile.read()
    
    while "{{" in fileContents:
        start = fileContents.index("{{")
        end = fileContents.index("}}")+2
        expressionStr = fileContents[start:end].replace("{{", "").replace("}}", "")
        value = eval(expressionStr)
        fileContents = fileContents[:start] + str(value) + fileContents[end:]
        pass

    with open(dstPath, "w+") as dstFile:
        dstFile.write(fileContents)

def remapClassNumbers(labeledClassList, annotationPath):
    annotationLines = []
    with open(annotationPath, "r") as annotationFile:
        for annotationLine in annotationFile:
            if annotationLine != "\n":
                labeledClassNumber = int(annotationLine.split(" ")[0])
                labeledClass = labeledClassList[labeledClassNumber]
                if labeledClass in classes:
                    newClassNumber = classes.index(labeledClass)
                    annotationContents = annotationLine.split(" ")
                    annotationContents[0] = str(newClassNumber)
                    annotationLines.append(" ".join(annotationContents))
    
    with open(annotationPath, "w+") as annotationFile:
        annotationFile.writelines([line+"\n" for line in annotationLines])




# Get configuration name parameter
parser = argparse.ArgumentParser(description='Setup files for darknet training.')
parser.add_argument('cfgName', nargs='?', default="simulated_test",
                    help='name of the training configuration.')
cfgName = parser.parse_args().cfgName

# Read yaml and extract parameters
with open(os.path.expanduser("~/darknet/darknet_scripts/training/cfg/%s.yaml" % cfgName)) as cfgFile:
    cfgData = yaml.load(cfgFile)
classes = cfgData["classes"]
classes = [c.lower() for c in classes]
numClasses = len(classes)
subdivisions = cfgData["subdivisions"]
width = cfgData["width"]
height = cfgData["height"]
testRatio = cfgData["test_ratio"]
negativeRatio = cfgData["negative_ratio"]
iterationsPerClass = cfgData["iterations_per_class"]

generateNegativeFrames()

testSamples = []
trainSamples = []

if cfgData["use_simulated"]:
    print("Processing simulated samples")
    simulatedPath = os.path.expanduser("~/darknet/darknet_scripts/data/simulated/")
    for imagePath in tqdm(glob.glob(simulatedPath + "**/*.jpg", recursive=True)):
        fileName = os.path.split(imagePath)[-1]
        imageClass = fileName.split("_")[0].lower()
        if imageClass in classes:
            classNum = classes.index(imageClass)
            remapClassNumbers([imageClass] * 999, simulatedPath + fileName.replace(".jpg", ".txt"))
            if random.random() > testRatio:
                trainSamples.append(imagePath)
            else:
                testSamples.append(imagePath)
else:
    print("Skipping simulated samples")


if cfgData["use_hand_labeled"]:
    print("Processing hand labeled samples")
    handLabeledPath = os.path.expanduser("~/darknet/darknet_scripts/data/hand_labeled/")
    with open(handLabeledPath+"ClassNumbers.txt") as classFile:
        labeledClassList = [line.split(":")[0].lower() for line in list(classFile)]

    for imagePath in tqdm(glob.glob(handLabeledPath + "**/*.jpg", recursive=True)):
        fileName = os.path.split(imagePath)[-1]
        remapClassNumbers(labeledClassList, imagePath.replace(".jpg", ".txt"))
        if random.random() > testRatio:
            trainSamples.append(imagePath)
        else:
            testSamples.append(imagePath)
else:
    print("Skipping hand labeled samples")


if cfgData["use_negatives"]:
    print("Processing negative samples")
    handLabeledPath = os.path.expanduser("~/darknet/darknet_scripts/data/negatives/")

    negativeImages = glob.glob(handLabeledPath + "**/*.jpg", recursive=True)
    if (len(testSamples) + len(trainSamples)) * negativeRatio > len(negativeImages):
        print("\n\n\n\nWARNING: Not enough negatives!\n\n\n\n")
    while (len(testSamples) + len(trainSamples)) * negativeRatio < len(negativeImages):
        negativeImages.pop(random.randint(0, len(negativeImages)-1))

    for imagePath in tqdm(negativeImages):
        if random.random() > testRatio:
            trainSamples.append(imagePath)
        else:
            testSamples.append(imagePath)
else:
    print("Skipping negative samples")


cfgPath = os.path.expanduser("~/darknet/%s/" % cfgName)
templatePath = os.path.expanduser("~/darknet/darknet_scripts/training/templates/")
if not os.path.exists(cfgPath):
    os.mkdir(cfgPath)
copyTemplate(templatePath + "template.data", cfgPath + "%s.data" % cfgName)
copyTemplate(templatePath + cfgData['cfg_template'], cfgPath + "%s.cfg" % cfgName)
with open(cfgPath + "%s.names" % cfgName, "w+") as namesFile:
    namesFile.writelines([c + "\n" for c in classes])
with open(cfgPath + "test.txt", "w+") as testFile:
    testFile.writelines([line + "\n" for line in testSamples])
with open(cfgPath + "train.txt", "w+") as trainFile:
    trainFile.writelines([line + "\n" for line in trainSamples])