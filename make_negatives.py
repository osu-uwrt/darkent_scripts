import glob 
import os
import cv2

print("Making negative samples...")
# Find all negative videos
videos = glob.glob("negatives/videos/*")

# Break each video down into frames
for video in videos:
    videoName = os.path.basename(video)
    if len(glob.glob("negatives/%s_*.jpg" % videoName)) > 0:
        print("%s was skipped, there are already frames from this video" % videoName)
        continue
    vidcap = cv2.VideoCapture(video)
    success,image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite("negatives/%s_%05d.jpg" % (videoName, count), image)     # save frame as JPEG file    
        with open("negatives/%s_%05d.txt" % (videoName, count), "w"):
            pass  
        success,image = vidcap.read()
        count += 1
    print("%s done!" % videoName)

print("All done!")