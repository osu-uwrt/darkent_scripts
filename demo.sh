#!/bin/bash
cd ~/darknet
./darknet detector demo $1/$1.data $1/$1.cfg $1/$1_best.weights $2 -out_filename darknet_scripts/demo.mp4