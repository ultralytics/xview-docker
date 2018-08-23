<img src="https://storage.googleapis.com/ultralytics/UltralyticsLogoName1000×676.png" width="200">  

# Introduction

This directory contains software developed by Ultralytics LLC. For more information on Ultralytics projects please visit:
http://www.ultralytics.com  

# Description

The https://github.com/ultralytics/xview-docker repo contains code to create an xView docker container for submission to the xView challenge: https://challenge.xviewdataset.org/.

# Requirements

Python 3.6 or later with the following `pip3 install -U -r requirements.txt` packages:

- `numpy`
- `scipy`
- `torch`
- `opencv-python`

# Running

- Run `detect.py` to process example image `1047.tif`. `detect.py` looks for weightfile `best.pt` in `checkpoints/`. `run.sh` contains directions for dockerizing the repository for submission in the xview challenge https://challenge.xviewdataset.org/ 

![Alt](https://github.com/ultralytics/xview/blob/master/output_img/1047.jpg "example")

# Contact

For questions or comments please contact Glenn Jocher at glenn.jocher@ultralytics.com or visit us at http://www.ultralytics.com/contact
