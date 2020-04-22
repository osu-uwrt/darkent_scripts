# darknet_scripts
Scripts to prepare data and run darknet

## Setup
Clone [AlexeyAB's darknet](https://github.com/AlexeyAB/darknet) into your home directory on Ubuntu and build it. Then clone this repository into the ~/darknet/ directory. After cloning, this repository should be located in ~/darknet/darknet_scripts/. Next, install the requirements from requirements.txt. Finally, install rclone to interface with box by running the training/install_rclone.sh script and then following the instructions [here](https://rclone.org/box/) to link rclone to your box account. Name the remote box.

## Layout
The data folder is for holding all hand-labeled and simulated positive and negative samples. 

The simulation folder is for simulating samples from models of objects

The training folder is for setting up training configurations and training