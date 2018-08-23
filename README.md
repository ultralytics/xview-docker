<img src="https://storage.googleapis.com/ultralytics/UltralyticsLogoName1000×676.png" width="200">  

# Introduction

This directory contains software developed by Ultralytics LLC. For more information on Ultralytics projects please visit:
http://www.ultralytics.com  

# Description

The https://github.com/ultralytics/xview-docker repo contains code to create xview challenge docker containers for submission. Credit to P.J. Reddie for YOLO (https://pjreddie.com/darknet/yolo/) and to Erik Lindernoren for the pytorch implementation (https://github.com/eriklindernoren/PyTorch-YOLOv3).

# Requirements

Python 3.6 or later with the following `pip3 install -U -r requirements.txt` packages:

- `numpy`
- `scipy`
- `torch`
- `torchvision`
- `opencv-python`

# Running
- Run `detect.py` to process example image `1047.tif`. `detect.py` looks for weightfile `best.pt` in `checkpoints/`. `run.sh` contains directions for dockerizing the repository for submission in the xview challenge https://challenge.xviewdataset.org/ 

![Alt](https://github.com/ultralytics/xview/blob/master/output_img/1047.jpg "example")

# Contact

For questions or comments please contact Glenn Jocher at glenn.jocher@ultralytics.com or visit us at http://www.ultralytics.com/contact
