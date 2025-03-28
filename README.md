<a href="https://www.ultralytics.com/"><img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg" width="320" alt="Ultralytics logo"></a>

# Introduction 👋

Welcome to the Ultralytics software directory! This codebase is open-source and 🔓 **distributed under the [AGPL-3.0 license](https://www.ultralytics.com/legal/agpl-3-0-software-license)**. Discover more about Ultralytics and our innovative projects by visiting our official website at [https://www.ultralytics.com](https://www.ultralytics.com/).

[![Ultralytics Actions](https://github.com/ultralytics/xview-docker/actions/workflows/format.yml/badge.svg)](https://github.com/ultralytics/xview-docker/actions/workflows/format.yml)
[![Ultralytics Discord](https://img.shields.io/discord/1089800235347353640?logo=discord&logoColor=white&label=Discord&color=blue)](https://discord.com/invite/ultralytics)
[![Ultralytics Forums](https://img.shields.io/discourse/users?server=https%3A%2F%2Fcommunity.ultralytics.com&logo=discourse&label=Forums&color=blue)](https://community.ultralytics.com/)
[![Ultralytics Reddit](https://img.shields.io/reddit/subreddit-subscribers/ultralytics?style=flat&logo=reddit&logoColor=white&label=Reddit&color=blue)](https://reddit.com/r/ultralytics)

# Project Overview 📄

This repository, hosted at [https://github.com/ultralytics/xview-docker](https://github.com/ultralytics/xview-docker), provides the necessary tools to dockerize and deploy [machine learning](https://www.ultralytics.com/glossary/machine-learning-ml) models specifically for the [xView detection challenge](https://challenge.xviewdataset.org/) 🔍. It is intended to be used alongside the trained models available in our [xView YOLOv3 repository](https://github.com/ultralytics/xview-yolov3).

# Prerequisites 🔖

Before you begin, ensure you have [Docker](https://www.docker.com/) and [Python](https://www.python.org/) 3.6 or newer installed. You'll also need several Python packages. Install them using pip:

```bash
pip3 install -U -r requirements.txt
```

Make sure you have the following essential packages installed:

- **numpy**: For efficient numerical operations.
- **scipy**: Used for various scientific and technical computations.
- **torch**: The core [deep learning](https://www.ultralytics.com/glossary/deep-learning-dl) framework ([PyTorch](https://pytorch.org/)).
- **opencv-python**: A library for [computer vision](https://www.ultralytics.com/glossary/computer-vision-cv) tasks.

# Dockerization Steps 🐳

Follow these steps to containerize this repository using the provided `run.sh` script for the xView challenge.

### Step 1: Copy Best Model Checkpoint

Retrieve the best performing model checkpoint from the training process conducted in our [xView YOLOv3 repository](https://github.com/ultralytics/xview-yolov3) and place it in the designated checkpoints directory:

```bash
mkdir xview-docker/checkpoints
cp xview-yolov3/checkpoints/best.pt xview-docker/checkpoints
```

### Step 2: Build and Tag The Docker Container

This sequence of commands removes any old [Docker images](https://docs.docker.com/get-started/docker-overview/#images), grants execution permissions to the `run.sh` script, builds the new Docker image, and applies a specific [tag](https://docs.docker.com/reference/cli/docker/image/tag/) (e.g., `ultralytics/xview:v30`):

```bash
sudo docker image prune -a
cd xview-docker && chmod +x run.sh
sudo docker build -t friendlyhello .
sudo docker tag friendlyhello ultralytics/xview:v30
```

### Step 3: Run Container on Example Image

Test the newly built container using an example image. This command runs the container, specifying CPU and memory limits via the [Docker run command](https://docs.docker.com/engine/containers/run/), executes the `run.sh` script on a sample TIFF image, and displays the output text file:

```bash
time sudo docker run -it --memory=8g --cpus=1 ultralytics/xview:v30 bash -c './run.sh /1047.tif /tmp && cat /tmp/1047.tif.txt'
```

Here's a sample output visualization:

![Example Detection](https://github.com/ultralytics/xview-docker/blob/main/output_img/1047.jpg)

### Step 4: Push to Docker Hub

After successful testing, upload your container image to [Docker Hub](https://hub.docker.com/), making it ready for submission to the xView challenge:

```bash
sudo docker push ultralytics/xview:v30
```

Your container can now be found hosted at [https://hub.docker.com/r/ultralytics/xview/](https://hub.docker.com/r/ultralytics/xview/), prepared for the challenge 🚀.

# Contribute 🤝

We warmly welcome contributions from the community! Whether it's fixing bugs, adding new features, or enhancing documentation, your input is highly valuable. Please refer to our [Contributing Guide](https://docs.ultralytics.com/help/contributing/) to get started. We're also keen to hear about your experiences with Ultralytics products—please consider filling out our [Survey](https://www.ultralytics.com/survey?utm_source=github&utm_medium=social&utm_campaign=Survey). A huge 🙏 thank you to all our contributors!

[![Ultralytics open-source contributors](https://raw.githubusercontent.com/ultralytics/assets/main/im/image-contributors.png)](https://github.com/ultralytics/ultralytics/graphs/contributors)

# License ©️

Ultralytics provides two licensing options to accommodate diverse needs:

- **AGPL-3.0 License**: Ideal for students and enthusiasts, this [OSI-approved](https://opensource.org/license/agpl-v3) open-source license promotes collaboration and knowledge sharing. See the [LICENSE](https://github.com/ultralytics/xview-docker/blob/main/LICENSE) file for details.
- **Enterprise License**: Designed for commercial applications, this license permits the integration of Ultralytics software and AI models into commercial products without the open-source obligations of AGPL-3.0. For commercial use cases, please contact us via [Ultralytics Licensing](https://www.ultralytics.com/license).

# Contact Us 📬

For bug reports, feature requests, and contributions, please visit [GitHub Issues](https://github.com/ultralytics/xview-docker/issues). For broader questions and discussions regarding this project or other Ultralytics initiatives, join our vibrant community on [Discord](https://discord.com/invite/ultralytics)!

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
  <a href="https://discord.com/invite/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-discord.png" width="3%" alt="Ultralytics Discord"></a>
</div>
