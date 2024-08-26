<br>
<a href="https://ultralytics.com" target="_blank"><img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg" width="320" alt="Ultralytics logo"></a>

# Introduction :wave:

Welcome to the Ultralytics software directory! Our codebase is open-source and 🔓 **distributed under the AGPL-3.0 license**. Explore more about Ultralytics and our cutting-edge projects at [our website](http://www.ultralytics.com).

[![Ultralytics Actions](https://github.com/ultralytics/xview-docker/actions/workflows/format.yml/badge.svg)](https://github.com/ultralytics/xview-docker/actions/workflows/format.yml) <a href="https://ultralytics.com/discord"><img alt="Discord" src="https://img.shields.io/discord/1089800235347353640?logo=discord&logoColor=white&label=Discord&color=blue"></a> <a href="https://community.ultralytics.com"><img alt="Ultralytics Forums" src="https://img.shields.io/discourse/users?server=https%3A%2F%2Fcommunity.ultralytics.com&logo=discourse&label=Forums&color=blue"></a> <a href="https://reddit.com/r/ultralytics"><img alt="Ultralytics Reddit" src="https://img.shields.io/reddit/subreddit-subscribers/ultralytics?style=flat&logo=reddit&logoColor=white&label=Reddit&color=blue"></a>

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

![Example Detection](https://github.com/ultralytics/xview/blob/main/output_img/1047.jpg "Example Detection")

## Step 4: Push to Docker Hub

Finally, upload the container to Docker Hub ready for challenge submission:

```bash
sudo docker push ultralytics/xview:v30
```

You can find the container now hosted at [Docker Hub](https://hub.docker.com/r/ultralytics/xview/), prepared for the challenge 🚀.

# 🤝 Contribute

We welcome contributions from the community! Whether you're fixing bugs, adding new features, or improving documentation, your input is invaluable. Take a look at our [Contributing Guide](https://docs.ultralytics.com/help/contributing) to get started. Also, we'd love to hear about your experience with Ultralytics products. Please consider filling out our [Survey](https://ultralytics.com/survey?utm_source=github&utm_medium=social&utm_campaign=Survey). A huge 🙏 and thank you to all of our contributors!

<!-- Ultralytics contributors -->

<a href="https://github.com/ultralytics/yolov5/graphs/contributors">
<img width="100%" src="https://github.com/ultralytics/assets/raw/main/im/image-contributors.png" alt="Ultralytics open-source contributors"></a>

# ©️ License

Ultralytics is excited to offer two different licensing options to meet your needs:

- **AGPL-3.0 License**: Perfect for students and hobbyists, this [OSI-approved](https://opensource.org/licenses/) open-source license encourages collaborative learning and knowledge sharing. Please refer to the [LICENSE](https://github.com/ultralytics/ultralytics/blob/main/LICENSE) file for detailed terms.
- **Enterprise License**: Ideal for commercial use, this license allows for the integration of Ultralytics software and AI models into commercial products without the open-source requirements of AGPL-3.0. For use cases that involve commercial applications, please contact us via [Ultralytics Licensing](https://ultralytics.com/license).

# 📬 Contact Us

For bug reports, feature requests, and contributions, head to [GitHub Issues](https://github.com/ultralytics/xview-docker/issues). For questions and discussions about this project and other Ultralytics endeavors, join us on [Discord](https://ultralytics.com/discord)!

<br>
<div align="center">
  <a href="https://github.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-github.png" width="3%" alt="Ultralytics GitHub"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.linkedin.com/company/ultralytics/"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-linkedin.png" width="3%" alt="Ultralytics LinkedIn"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://twitter.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-twitter.png" width="3%" alt="Ultralytics Twitter"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://youtube.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-youtube.png" width="3%" alt="Ultralytics YouTube"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.tiktok.com/@ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-tiktok.png" width="3%" alt="Ultralytics TikTok"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://ultralytics.com/bilibili"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-bilibili.png" width="3%" alt="Ultralytics BiliBili"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://ultralytics.com/discord"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-discord.png" width="3%" alt="Ultralytics Discord"></a>
</div>
