#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home
# chmod 755 launcher.sh
# sudo crontab -e
# @reboot sh /home/pi/bbt/launcher.sh >/home/pi/logs/cronlog 2>&1


cd /
cd home/pi/bbt
sudo python bbt.py
cd /