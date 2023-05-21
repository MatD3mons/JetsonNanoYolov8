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

sudo apt-get install -y dphys-swapfile
sudo nano /sbin/dphys-swapfile
Change CONF_MAXSWAP to 4096, save and exit
sudo nano /etc/dphys-swapfile
Enable CONF_SWAPSIZE and put 4096, save and exit
Run sudo reboot . to restart Jetson Nano 7.Run free -m and check the Swap total

wget https://github.com/Qengineering/Install-OpenCV-Jetson-Nano/raw/main/OpenCV-4-7-0.sh 
sudo chmod 755 ./OpenCV-4-7-0.sh 
./OpenCV-4-7-0.sh
