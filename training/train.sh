#!/bin/bash
./training/download_data.sh
python3 training/setup.py $1
cd ~/darknet
./darknet detector train $1/$1.data $1/$1.cfg startingWeights.weights -map