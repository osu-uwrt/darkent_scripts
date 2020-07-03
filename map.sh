#!/bin/bash
cd ~/darknet
./darknet detector map $1/$1.data $1/$1.cfg $1/$1_best.weights 