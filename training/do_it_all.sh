#!/bin/bash
#./download_data.sh
python3 change_class_num.py
python3 make_negatives.py 
python3 make_training_set.py 
cd ~/darknet
./darknet detector train data/gate.data cfg/yolov3-tiny-gate.cfg yolov3-tiny.conv.15 -map