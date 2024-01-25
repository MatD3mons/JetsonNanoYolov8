# Instal on Jetson Nano, the YOLOv8, IntelL515 and Ned2

### 1) Change the environement desktop

// https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwiKwYDHn_ODAxUuTaQEHdOZB5UQFnoECBIQAQ&url=https%3A%2F%2Fjetsonhacks.com%2F2020%2F11%2F07%2Fsave-1gb-of-memory-use-lxde-on-your-jetson%2F&usg=AOvVaw3gYeR8tqblUYOyIO8kvTVI&opi=89978449

reboot, select LXDE,
```
sudo dpkg-reconfigure lightdm
```

### 2) add more swap memory

// https://qengineering.eu/install-opencv-on-jetson-nano.html

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

sudo apt remove python2
sudo apt autoremove --purge

update to ubuntu 20.04

## OTHER

```
sudo apt install python3-setuptools
sudo apt install python3-pip
pip3 install -U pip
reboot
```

le pip ne fonctionne qu'après le reboot

https://github.com/NVIDIA/TensorRT/tree/release/8.2/python 

#### 4) build TensorRT

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

if bug change by this :

// https://forums.developer.nvidia.com/t/tensorrt-on-jetson-with-python-3-9/196131/9

python3 -m pip install build/dist/tensorrt-8.2.1.9-cp38-none-linux_aarch64.whl

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

!
! change gcc en 8 et g++ 8
!

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

```
Used with PyTorch 1.13.0

Only for a Jetson Nano with Ubuntu 20.04

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

pip install --no-dependencies ultralytics

use gcc and g++ 8

https://github.com/Quengineering/Jetson-Nano-Ubuntu-20-images/issues/40
install cmake 3.21.1


pip3 install onnxsim
pip3 install 

before : 

```
git clone --recursive --branch 1.7 http://github.com/pytorch/pytorch
cd pytorch
python3.8 -m pip install -r requirements.txt
python3.8 setup.py install
python3.8 setup.py develop && python -c "import torch"
```

### 5) Ultralytics

```
pip install ultralytics
```














### 4) install python3 and create env

```
sudo apt install python3.8
sudo apt install python3.8-dev
sudo apt install python3.8-venv
python3.8 -m venv test
source test/bin/activate
pip3 install -U pip
```

je sais plus a quoi sa sert ??
```
//sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${version} 0
//sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
//sudo update-alternatives --config python3
```

### 5) install OpenCV

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
