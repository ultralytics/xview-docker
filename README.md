html
<img src="https://storage.googleapis.com/ultralytics/UltralyticsLogoName1000×676.png" width="200">
```

# 🎉 Introduction

Welcome to the Ultralytics repository! This space is dedicated to open source software crafted by the Ultralytics team, proudly licensed under AGPL-3.0. For a deeper dive into our array of exciting projects, you're warmly invited to  visit [our website](http://www.ultralytics.com).

# 🔍 Description

The [Ultralytics xView Docker](https://github.com/ultralytics/xview-docker) repository contains the essential code to create a Docker container tailored for submissions to the [xView Challenge](https://challenge.xviewdataset.org/). This repository is particularly designed to synergize with models trained using the [xView YOLOv3 repository](https://github.com/ultralytics/xview-yolov3).

# 📋 Requirements

Before you can dominate the xView challenge, ensure you've got Docker and Python >= 3.6. Install the required Python packages by running:

```bash
pip3 install -U -r requirements.txt
```

The packages include:
- `numpy`
- `scipy`
- `torch`
- `opencv-python`

# 🚀 Running Your Dockerized Model

`run.sh` holds the secret recipe to wrap this repository into a container for the xView challenge inclusion. Let the walkthrough begin:

### 🔑 1. Copy Best Checkpoint

Seize your top-notch model checkpoint from `xview-yolov3`. Let's get started:

```bash
mkdir xview-docker/checkpoints
cp path_to_your_xview-yolov3/checkpoints/best.pt xview-docker/checkpoints
```

### 🏗️ 2. Build and Tag Container

Cleanse any outdated containers and set the stage for your brand-new creation:

```bash
sudo docker image prune -a
cd xview-docker && chmod +x run.sh
sudo docker build -t your_docker_image_name . 
sudo docker tag your_docker_image_name ultralytics/xview:your_version_tag
```

### 📸 3. Test Example Image
Now, put your container to the test with an example image, all while adhering to specific resource constraints:

```bash
time sudo docker run -it --memory=8g --cpus=1 ultralytics/xview:your_version_tag bash -c './run.sh /path_to_your_example_image/1047.tif /tmp && cat /tmp/1047.tif.txt'
```

Example output:
![Example Detection Output](https://github.com/ultralytics/xview/blob/master/output_img/1047.jpg "Example Detection Output")

### 📤 4. Push to DockerHub

Once all checks are green, dispatch your container to [DockerHub](https://hub.docker.com/):

```bash
sudo docker push ultralytics/xview:your_version_tag
```

And voilà! Your container now proudly resides at [Ultralytics xView DockerHub](https://hub.docker.com/r/ultralytics/xview/) and is set for the challenge!

# 😃 Need Help?

For support or queries, rather than direct contact, please avail the [contact form](http://www.ultralytics.com/contact) on our website. We’d love to hear from you!
