#!/bin/bash
# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

# WARNING: Run 'chmod +x run.sh' BEFORE BUILDING DOCKER CONTAINER

# example:
# bash run.sh ./1047.tif ./tmp

# Remove Optimizer:
# mkdir xview/checkpoints && cp yolo/checkpoints/best.pt xview/checkpoints/latest.pt
# cd xview/checkpoints && python3
# import torch; a=torch.load('latest.pt', map_location='cpu'); a['optimizer']=None; torch.save(a,'latest.pt'); exit()

# sudo rm -rf xview && git clone https://github.com/ultralytics/xview
# gsutil cp gs://ultralytics/best_lite.pt xview/checkpoints/checkpoint.pt # && gsutil cp gs://ultralytics/6leaky681_stripped.pt xview/checkpoints/classifier.pt
# mkdir xview/checkpoints && cp yolo/checkpoints/best.pt xview/checkpoints/best.pt
# sudo docker image prune -a && cd xview && chmod +x run.sh && sudo docker build -t friendlyhello . && sudo docker tag friendlyhello ultralytics/xview:v30
# time sudo docker run -it --memory=8g --cpus=1 ultralytics/xview:v30 bash -c './run.sh /1047.tif /tmp && cat /tmp/1047.tif.txt'
# sudo docker push ultralytics/xview:v30

python3 detect.py -image_folder $1 -output_folder $2
