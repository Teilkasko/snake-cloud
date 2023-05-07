#!/bin/bash

# Userdata script to deploy the app on an AWS EC2 machine running Amazon Linux

# Set up system dependencies
yum install -y git python3-pip
sudo -u ec2-user pip3 install virtualenv

# Clone project and set up project dependencies
cd /home/ec2-user
git clone --branch develop https://github.com/fsolaroli/SnAkE.git snake
cd snake/
virtualenv .
chown -R ec2-user:ec2-user .
source ./bin/activate
sudo -u ec2-user pip3 install -r requirements.txt

# Make sure that the app server can be launched from a system service
cp aws-files/run-snake-server.sh /usr/local/bin/
chmod u+x /usr/local/bin/run-snake-server.sh 

# Start app automatically after booting
cp aws-files/startup.service /lib/systemd/system/startup.service
systemctl enable startup.service
systemctl start startup.service
