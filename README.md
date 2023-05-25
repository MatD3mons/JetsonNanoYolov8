# JetsonNanoYolov8

Ouvrir un terminale
sudo apt-get update && sudo apt-get upgrade

sudo apt install python3-setuptools
sudo apt install python3-pip
sudo apt install python3.8
python3.8 -m pip install pip
sudo apt install nano
nano ~/.bashrc
#add in the section # some more aliases a new line containing
"
alias python='python3.8'
alias python3='python3.8'
"

sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${version} 0
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
sudo update-alternatives --config python3

sudo apt-get install -y dphys-swapfile
sudo nano /sbin/dphys-swapfile
Change CONF_MAXSWAP to 4096, save and exit
sudo nano /etc/dphys-swapfile
Enable CONF_SWAPSIZE and put 4096, save and exit
Run sudo reboot . to restart Jetson Nano 7.Run free -m and check the Swap total

wget https://github.com/Qengineering/Install-OpenCV-Jetson-Nano/raw/main/OpenCV-4-7-0.sh 
add this flag https://forums.developer.nvidia.com/t/cannot-build-opencv-for-python3-9/211072/10
sudo chmod 755 ./OpenCV-4-7-0.sh 
./OpenCV-4-7-0.sh



https://docs.ultralytics.com/yolov5/tutorials/running_on_jetson_nano/
sudo apt install python3.8
sudo apt install python3.8-dev
sudo apt install python3.8-venv
python3.8 -m venv yolov5-env
source yolov5-env/bin/activate

j'ai pas réussi donc je teste yolov5 avec Ultralicts
sudo apt update
sudo apt upgrade
sudo apt install -y python3-pip
pip3 install --upgrade pip
sudo apt install nano
git clone https://github.com/ultralytics/yolov5
cd yolov5
nano requirements.txt
pip install cython
pip install scikit-build
pip install wheel
pip install numpy
pip install pybind11
pip install cppy
pip install versioneer
pip install -r requirement.txt

gitpython >= 3.1.20
# torch>=1.7.0
# torchvision>=0.8.1

cd ~

pip install pyyaml
git clone --recursive --branch 1.7 http://github.com/pytorch/pytorch
cd pytorch
python3.8 -m pip install -r requirements.txt
python3.8 setup.py install
python3.8 setup.py develop && python -c "import torch"



# Installs librealsense and pyrealsense2 on the Jetson NX running Ubuntu 18.04
# and using Python 3
# Tested on a Jetson NX running Ubuntu 18.04 and Python 3.6.9

sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install -y --no-install-recommends \
    python3 \
    python3-setuptools \
    python3-pip \
	python3-dev

# Install the core packages required to build librealsense libs
sudo apt-get install -y git libssl-dev libusb-1.0-0-dev pkg-config libgtk-3-dev
# Install Distribution-specific packages for Ubuntu 18
sudo apt-get install -y libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev

# Install LibRealSense from source
# We need to build from source because
# the PyPi pip packages are not compatible with Arm processors.
# See link [here](https://github.com/IntelRealSense/librealsense/issues/6964).

# First clone the repository
git clone https://github.com/IntelRealSense/librealsense.git
cd ./librealsense

# Make sure that your RealSense cameras are disconnected at this point
# Run the Intel Realsense permissions script
./scripts/setup_udev_rules.sh

# Now the build
mkdir build && cd build
## Install CMake with Python bindings (that's what the -DBUILD flag is for)
## see link: https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python#building-from-source
cmake ../ -DBUILD_PYTHON_BINDINGS:bool=true
## Recompile and install librealsense binaries
## This is gonna take a while! The -j4 flag means to use 4 cores in parallel
## but you can remove it and simply run `sudo make` instead, which will take longer
sudo make uninstall && sudo make clean && sudo make -j4 && sudo make install

## Export pyrealsense2 to your PYTHONPATH so `import pyrealsense2` works
export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.8/pyrealsense2

rm -rf folder

pip install pyniryo
pip install pillow

sudo apt-get install python4-pybind11

$ sudo apt-get install libjpeg-dev zlib1g-dev libpython3-dev libavcodec-dev libavformat-dev libswscale-dev
$ git clone --branch v0.8.1 https://github.com/pytorch/vision torchvision   # see below for version of torchvision to download
$ cd torchvision
$ export BUILD_VERSION=0.8.0  # where 0.x.0 is the torchvision version  
$ python3 setup.py install
$ cd ../  # attempting to load torchvision from build dir will result in import error
$ pip install 'pillow<7' # always needed for Python 2.7, not needed torchvision v0.5.0+ with Python 3.6

pip install pandas
pip install tqdm
pip install matplotlib
