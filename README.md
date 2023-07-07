# Instal on Jetson Nano, the YOLOv8, IntelL515 and Ned2

Ouvrir un terminale
sudo apt-get update && sudo apt-get upgrade

### 1) Change the environement desktop

```
sudo apt remove --purge ubuntu-desktop
sudo apt install lxdm
sudo apt remove --purge gdm3
sudo apt install lxde
sudo apt install --reinstall lxdm
```

#### 2) install nano to cha

```
sudo apt install nano
nano ~/.bashrc
```

### 3) add more swap memory

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


### 4) install python3 and create env

```
sudo apt install python3-setuptools
sudo apt install python3-pip
sudo apt install python3.8
sudo apt install python3.8-dev
sudo apt install python3.8-venv
python3.8 -m venv myenv
source myenv/bin/activate
python3 -m pip install -U pip
pip3 install --upgrade pip
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
git clone --recursive --branch 1.7 http://github.com/pytorch/pytorch
cd pytorch
python3.8 -m pip install -r requirements.txt
python3.8 setup.py install
python3.8 setup.py develop && python -c "import torch"
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