<img src="https://storage.googleapis.com/ultralytics/UltralyticsLogoName1000×676.png" width="200">  

# Introduction :wave:

Welcome to the Ultralytics software directory! Our codebase is open-source and 🔓 **distributed under the AGPL-3.0 license**. Explore more about Ultralytics and our cutting-edge projects at [our website](http://www.ultralytics.com).

# Project Overview :page_facing_up:

This repository, located at https://github.com/ultralytics/xview-docker, is designed to help you dockerize and deploy machine learning models for the xView detection challenge 🔍. It should be used in combination with the trained models from our [xView YOLOv3 repository](https://github.com/ultralytics/xview-yolov3).

# Prerequisites :bookmark_tabs:

To get started, you need Docker and Python 3.6 (or newer). Ensure that you have all the required packages by installing them via pip:

```bash
pip3 install -U -r requirements.txt
```

You should have the following packages:

- `numpy` for numerical operations,
- `scipy` for scientific computations,
- `torch` as the deep learning framework, and
- `opencv-python` for computer vision tasks.

# Dockerization Steps :whale:

Below are the steps to containerize this repository for the xView challenge using `run.sh`.

## Step 1: Copy Best Model Checkpoint

Get the best performing checkpoint from our [xView YOLOv3 model](https://github.com/ultralytics/xview-yolov3):

```bash
mkdir xview-docker/checkpoints
cp xview-yolov3/checkpoints/best.pt xview-docker/checkpoints
```

## Step 2: Build and Tag The Docker Container

Here's how to remove older images, set the right permissions for the script, build the image, and tag it appropriately (e.g., `ultralytics/xview:v30`):

```bash
sudo docker image prune -a
cd xview-docker && chmod +x run.sh
sudo docker build -t friendlyhello .
sudo docker tag friendlyhello ultralytics/xview:v30
```

## Step 3: Run Container on Example Image

Test the container with the example image while specifying CPU and memory usage:

```bash
time sudo docker run -it --memory=8g --cpus=1 ultralytics/xview:v30 bash -c './run.sh /1047.tif /tmp && cat /tmp/1047.tif.txt'
```

Here's a sample output:

![Example Detection](https://github.com/ultralytics/xview/blob/master/output_img/1047.jpg "Example Detection")

## Step 4: Push to Docker Hub

Finally, upload the container to Docker Hub ready for challenge submission:

```bash
sudo docker push ultralytics/xview:v30
```

You can find the container now hosted at [Docker Hub](https://hub.docker.com/r/ultralytics/xview/), prepared for the challenge 🚀.

# Let's Connect :handshake:

Curious about what we're up to? Head over to [Ultralytics Contact Page](http://www.ultralytics.com/contact) to connect!
