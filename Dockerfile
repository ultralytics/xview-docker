# Build from a recent python3 version (64 bit python required for Tensorflow)
FROM python:3.6.5-onbuild

# Install required python modules
# RUN pip3 install http://download.pytorch.org/whl/cpu/torch-0.4.0-cp36-cp36m-linux_x86_64.whl 
# RUN pip3 install torchvision opencv-python  # numpy scipy matplotlib tqdm


# Move image to root dir where inference code (and tutorial) expects to find it
RUN mv 1047.tif /1047.tif

# Rename the trained checkpoint from the baseline model release to `model.pb`
# so that the `run.sh` file will find and use it
# RUN mv multires.pb model.pb
# Note: you can swap in one of your own checkpoints instead, just change the line above
