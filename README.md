# JetsonNanoYolov8

Ouvrir un terminale
sudo apt-get update && sudo apt-get upgrade

sudo apt install python3-pip
sudo apt install python3.8
sudo apt install nano
nano ~/.bashrc
#add in the section # some more aliases a new line containing
"
alias python='python3.8'
alias python3='python3.8'
alias pip='python3.8 -m pip'
"

ls /usr/bin/python* #pour savoir les version presente sur la carte
sudo apt-get remove python2.7
sudo apt-get remove --auto-remove python2.7
sudo apt-get purge python2.7
sudo apt-get purge --auto-remove python2.7

sudo apt-get install -y dphys-swapfile
sudo nano /sbin/dphys-swapfile
Change CONF_MAXSWAP to 4096, save and exit
Run sudo gedit /etc/dphys-swapfile
Enable CONF_SWAPSIZE and put 4096, save and exit
Run sudo reboot . to restart Jetson Nano 7.Run free -m and check the Swap total

wget https://github.com/Qengineering/Install-OpenCV-Jetson-Nano/raw/main/OpenCV-4-7-0.sh 
sudo chmod 755 ./OpenCV-4-7-0.sh 
