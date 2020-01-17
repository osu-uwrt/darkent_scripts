#!/bin/bash
./download_data.sh
python3 change_class_num.py
python3 make_negatives.py 
python3 make_training_sets.py 
cd ~/darknet
./darknet detector train data/path.data cfg/yolov3-tiny-path.cfg yolov3-tiny.conv.15 -map