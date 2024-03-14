# Instal on Jetson Nano, the YOLOv9 - v8 - V7 - V6 - V5, IntelL515 and Ned2

# Commandes ( After installation and move in good folder ):

#### YOLOv9
```
wget https://github.com/WongKinYiu/yolov9/releases/download/v0.1/yolov9-c-converted.pt
python detect.py --source 0 --img 640 --device 0 --weights './yolov9-c-converted.pt'
```
or
```
yolo detect predict model=yolov9c.pt source=0 show=True nms=True
```

#### YOLOv8
```
yolo detect predict model=yolov8n.pt source=0 show=True nms=True
yolo detect predict model=yolov8s.pt source=0 show=True nms=True
yolo detect predict model=yolov8m.pt source=0 show=True nms=True
```

#### YOLOv7
```
wget wget https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7-tiny.pt
python3 detect.py --weights yolov7-tiny.pt --conf 0.25 --img-size 640 --source 0
```

#### YOLOv6
```
wget https://github.com/meituan/YOLOv6/releases/download/0.4.0/yolov6n.pt
python tools/infer.py --weights yolov6s.pt --webcam --webcam-addr 0
```

#### YOLOv8
```
yolo detect predict model=yolov5n.pt source=0 show=True nms=True
yolo detect predict model=yolov5s.pt source=0 show=True nms=True
yolo detect predict model=yolov5m.pt source=0 show=True nms=True
```

### 1) Change the environement desktop

reboot, select LXDE,
```
sudo dpkg-reconfigure lightdm
```

### 2) add more swap memory

```
sudo apt-get install -y dphys-swapfile
sudo nano /sbin/dphys-swapfile
```
Change CONF_MAXSWAP to 4096, save and exit
```
sudo nano /etc/dphys-swapfile
```
Enable CONF_SWAPSIZE and put 4096, save and exit

reboot  Jetson Nano.

### 3) Update

Ouvrir un terminale
```
# refresh your system
sudo apt-get update
sudo apt-get upgrade
sudo apt-get autoremove
```

### update ubuntu to 20.04

//https://qengineering.eu/install-ubuntu-20.04-on-jetson-nano.html

## OTHER

```
sudo apt install python3-setuptools
sudo apt install python3-pip
pip3 install -U pip
reboot
```

le pip ne fonctionne qu'après le reboot

#### 4) build TensorRT 8.2.1.9
```
git clone -b releae/8.0 https://github.com/NVIDIA/TensorRT.git
cd  TensorRT
git submodule update --init --recursive

export EXT_PATH=~/external

mkdir -p $EXT_PATH && cd $EXT_PATH
git clone https://github.com/pybind/pybind11.git

wget https://www.python.org/ftp/python/3.10.11/Python-3.8.10.tgz
tar -xvf Python-3.8.10.tgz
mkdir -p $EXT_PATH/python3.8/include
cp -r Python-3.8.11/Include/* $EXT_PATH/python3.8/include

wget http://ports.ubuntu.com/pool.main/p/python3.8/libpython3.8-dev_3.8.10-0ubuntu1~20.04.9_arm64.deb // not aarch64 ????
ar x libpython3.8-dev*.deb
mkdir debian && tar -xf data.tar.xz -C debian
cp debian/usr/include/aarch64-linux-gnu/python3.8/pyconfig.h python3.8/include/

cd $TRT_OSSPATH/python
TENSORRT_MODULE=tensorrt PYTHON_MAJOR_VERSION=3 PYTHON_MINOR_VERSION=8 TARGET_ARCHITECTURE=aarch64 ./build.sh 
```
if bug change by this :

// https://forums.developer.nvidia.com/t/tensorrt-on-jetson-with-python-3-9/196131/9
```
python3 -m pip install build/dist/tensorrt-8.2.1.9-cp38-none-linux_aarch64.whl
```
### 6) install librairie python 

```
pip install cython
pip install scikit-build
pip install wheel
pip install numpy
pip install pybind11
pip install cppy
pip install versioneer
pip install pyyaml
pip install pyniryo
pip install pillow
pip install pandas
pip install tqdm
pip install matplotlib
pip install 'pillow<7'
```

### 7) install pytorch librarie
```
change gcc en 8 et g++ 8
```

```
pip install imutils
```
https://qengineering.eu/install-pytorch-on-jetson-nano.html

```
# install the dependencies (if not already onboard)
$ sudo apt-get install python3-pip libjpeg-dev libopenblas-dev libopenmpi-dev libomp-dev
$ sudo -H pip3 install future
$ sudo pip3 install -U --user wheel mock pillow
$ sudo -H pip3 install testresources
# above 58.3.0 you get version issues
$ sudo -H pip3 install setuptools==58.3.0
$ sudo -H pip3 install Cython
# install gdown to download from Google drive
$ sudo -H pip3 install gdown
# download the wheel
$ gdown https://drive.google.com/uc?id=1e9FDGt2zGS5C5Pms7wzHYRb0HuupngK1
# install PyTorch 1.13.0
$ sudo -H pip3 install torch-1.13.0a0+git7c98e70-cp38-cp38-linux_aarch64.whl
# clean up
$ rm torch-1.13.0a0+git7c98e70-cp38-cp38-linux_aarch64.whl
```

Used with PyTorch 1.13.0

Only for a Jetson Nano with Ubuntu 20.04

```
# the dependencies
$ sudo apt-get install libjpeg-dev zlib1g-dev libpython3-dev
$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev
$ sudo pip3 install -U pillow
# install gdown to download from Google drive, if not done yet
$ sudo -H pip3 install gdown
# download TorchVision 0.14.0
$ gdown https://drive.google.com/uc?id=19UbYsKHhKnyeJ12VPUwcSvoxJaX7jQZ2
# install TorchVision 0.14.0
$ sudo -H pip3 install torchvision-0.14.0a0+5ce4506-cp38-cp38-linux_aarch64.whl
# clean up
$ rm torchvision-0.14.0a0+5ce4506-cp38-cp38-linux_aarch64.whl
```

use gcc and g++ 8

https://github.com/Quengineering/Jetson-Nano-Ubuntu-20-images/issues/40
install cmake 3.21.1

###  onnxsim
```
pip3 install onnxsim
```
### onnxruntime_gpu
```
https://github.com/microsoft/onnxruntime/issues/6124
wget https://nvidia.box.com/shared/static/iizg3ggrtdkqawkmebbfixo7sce6j365.whl -o onnxruntime_gpu-1.16.0-cp38-cp38-linux_aarch64.whl
python3 -m pip install onnxruntime_gpu-1.16.0-cp38-cp38-linux_aarch64.whl
```
#Bug 
!! il faut numpy==1.23.1, la 1.24 est bugé due au remove du numpy.bool
```
sudo apt-get install curl ( si vous voulez test des images )
```

# install pycuda

```
$ export PATH=/usr/local/cuda-10.2/bin${PATH:+:${PATH}}
$ export LD_LIBRARY_PATH=/usr/local/cuda-10.2/lib64:$LD_LIBRARY_PATH
$ python3 -m pip install pycuda --user
```

## YOLOv9

```
pip3 install IPython
git clone https://github.com/WongKinYiu/yolov9
```

## YOLOv8

```
pip install --no-dependencies ultralytics
```

## Yolov7

```
git clone https://github.com/WongKinYiu/yolov7
```

## YOLOV6
```
git clone https://github.com/meituan/YOLOv6
```

## YOLOv5
```
pip install --no-dependencies ultralytics
```

# jtop !!

attention la dernière mise a jour ne fonctionne pas, la 4.0.0 si 


# YoloX
```
pip install tabulate
pip install pycocotools
pip install loguru
git clone https://github.com/Megvii-BaseDetection/YOLOX.git
cd YOLOX
wget https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_nano.pth
wget https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_tiny.pth

cd tools
python3 demo.py webcam -n yolox-nano -c ../yolox_nano.pth --camid 0 --conf 0.25 --nms 0.45 --tsize 640 --save_result --device
```
### install OpenCV

```
wget https://github.com/Qengineering/Install-OpenCV-Jetson-Nano/raw/main/OpenCV-4-7-0.sh 
add this flag https://forums.developer.nvidia.com/t/cannot-build-opencv-for-python3-9/211072/10
sudo chmod 755 ./OpenCV-4-7-0.sh 
./OpenCV-4-7-0.sh
```

# Installs librealsense and pyrealsense2

#### Install the core packages required to build librealsense libs
```
sudo apt-get install -y git libssl-dev libusb-1.0-0-dev pkg-config libgtk-3-dev
```
#### Install Distribution-specific packages for Ubuntu 18
```
sudo apt-get install -y libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev
```

# Install LibRealSense from source
```
git clone https://github.com/IntelRealSense/librealsense.git
cd ./librealsense
```

#### Make sure that your RealSense cameras are disconnected at this point
```
./scripts/setup_udev_rules.sh
```

#### Now the build
```
mkdir build && cd build
```

#### Install CMake with Python bindings (that's what the -DBUILD flag is for)
#### see link: https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python#building-from-source
```
cmake ../ -DBUILD_PYTHON_BINDINGS:bool=true
```
#### Recompile and install librealsense binaries
#### This is gonna take a while! The -j4 flag means to use 4 cores in parallel
#### but you can remove it and simply run `sudo make` instead, which will take longer
```
sudo make uninstall && sudo make clean && sudo make -j4 && sudo make install
```

## Export pyrealsense2 to your PYTHONPATH so `import pyrealsense2` works
```
export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.8/pyrealsense2
```

# install torchvision librairie
```
sudo apt-get install python4-pybind11
sudo apt-get install libjpeg-dev zlib1g-dev libpython3-dev libavcodec-dev libavformat-dev libswscale-dev
git clone --branch v0.8.1 https://github.com/pytorch/vision torchvision   # see below for version of torchvision to download
cd torchvision
export BUILD_VERSION=0.8.0  # where 0.x.0 is the torchvision version  
python3 setup.py install
```
