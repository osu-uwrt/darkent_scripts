#!/usr/bin/env python3

import glob 
import random
import cv2

print("Displaying a random frame. Press any key to view next frame")

# Get list of frames and sort thm so thr frames are in order
images = sorted(glob.glob("data/simulated/**/*.jpg", recursive=True))

# Choose a starting frame
i = random.randint(0, len(images)-1)
while True:
    print(images[i])
    img = cv2.imread(images[i])

    # Draw bboxes on image
    for line in open(images[i].replace(".jpg", ".txt")):
        if line != "\n":
            classId, x, y, w, h = [float(n) for n in line.split(" ")]
            x = int(x * img.shape[1])
            y = int(y * img.shape[0])
            w = int(w * img.shape[1])
            h = int(h * img.shape[0])
            img = cv2.rectangle(img, (x-w//2, y-h//2), (x+w//2, y+h//2), (0, 0, 255))

    # Display image and wait for user to click button
    cv2.imshow("Data", img)
    cv2.waitKey()
    i += 1