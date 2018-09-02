<img src="https://storage.googleapis.com/ultralytics/UltralyticsLogoName1000×676.png" width="200">  

# Introduction

This directory contains software developed by Ultralytics LLC, and **is freely available for redistribution under the MIT license**. For more information on Ultralytics projects please visit:
http://www.ultralytics.com  

# Description

The https://github.com/ultralytics/xview-docker repo contains code to create an xView docker container for submission to the xView challenge: https://challenge.xviewdataset.org/. This repo is intended for use in conjunction with models trained using https://github.com/ultralytics/xview-yolov3.

# Requirements

Python 3.6 or later with the following `pip3 install -U -r requirements.txt` packages:

- `numpy`
- `scipy`
- `torch`
- `opencv-python`

# Running

`run.sh` contains directions for dockerizing this repository for submission in the xView challenge. The steps are:

### 1. Copy Checkpoint
Copy best checkpoint from `xview-yolov3` (https://github.com/ultralytics/xview-yolov3)
``` bash
$ mkdir xview-docker/checkpoints
$ cp xview-yolov3/checkpoints/best.pt xview-docker/checkpoints
```

### 2. Build and Tag Container
Prune older containers, move into `/xview` directory, assign permissions to `run.sh`, and build and tag container (tagged as `ultralytics/xview:v30` in this example)
``` bash
$ sudo docker image prune -a
$ cd xview-docker && chmod +x run.sh
$ sudo docker build -t friendlyhello . 
$ sudo docker tag friendlyhello ultralytics/xview:v30
```

### 3. Test Example Image
Run `detect.py` to test example image `1047.tif` for speed and errors.
``` bash
$ time sudo docker run -it --memory=8g --cpus=1 ultralytics/xview:v30 bash -c './run.sh /1047.tif /tmp && cat /tmp/1047.tif.txt'
```
![Alt](https://github.com/ultralytics/xview/blob/master/output_img/1047.jpg "example")


### 4. Push to DockerHub
Push container to DockerHub (https://hub.docker.com/)
``` bash
$ sudo docker push ultralytics/xview:v30
```

Container now resides at https://hub.docker.com/r/ultralytics/xview/

# Contact

For questions or comments please contact Glenn Jocher at glenn.jocher@ultralytics.com or visit us at http://www.ultralytics.com/contact
