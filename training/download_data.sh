#!/bin/bash

# On the mega-computer, box data is automatically backed up but is sometimes not up to date.
# Copy data from there so rclone has less work
echo "Copying data from Box Sync (If it exists)..."
rsync -r "/mnt/Data/Box Sync/The Underwater Robotics Team/Software/YOLO/TrainingData/" data
mkdir -p negatives
rsync -r "/mnt/Data/Box Sync/The Underwater Robotics Team/Software/YOLO/Negatives/" negatives/videos

# This command will only transfer files that are wrong or missing
echo "Syncing directly with Box..."
rclone sync "box:The Underwater Robotics Team/Software/YOLO/TrainingData" data -P --fast-list --checkers 32 --transfers 32 
rclone sync "box:The Underwater Robotics Team/Software/YOLO/Negatives" negatives/videos -P --fast-list --checkers 32 --transfers 32 
echo "Done!"