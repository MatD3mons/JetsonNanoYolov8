# JetsonNanoYolov8

Ouvrir un terminale
sudo apt-get update && sudo apt-get upgrade

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
sudo apt-get install -y libopenblas-base libopenmpi-dev
wget https://nvidia.box.com/shared/static/fjtbno0vpo676a25cgvuqc1wty0fkkg6.whl -O torch-1.10.0-cp36-cp36m-linux_aarch64.whl
pip3 install torch-1.10.0-cp36-cp36m-linux_aarch64.whl
