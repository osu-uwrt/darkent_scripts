#!/bin/bash

# On the mega-computer, box data is automatically backed up but is slow.
# Copy data from there so rclone has less work
rsync -r "/mnt/Data/Box Sync/The Underwater Robotics Team/Software/YOLO/TrainingData/" data
rclone sync "box:The Underwater Robotics Team/Software/YOLO/TrainingData" data -P