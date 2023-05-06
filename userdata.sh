#!/bin/bash

# Userdata script to deploy the app on an AWS EC2 machine running Amazon Linux

yum install -y git python3-pip
pip3 install virtualenv

cd /home/ec2-user
git clone --branch develop https://github.com/fsolaroli/SnAkE.git snake
cd snake/
virtualenv .
chown -R ec2-user:ec2-user .

source ./bin/activate
sudo -u ec2-user pip3 install -r requirements.txt
cd src/server
# This way the output of main.py will be written to log.txt
# But, unfortunately, not before the process ends
sudo -u ec2-user python3 main.py > log.txt &
sudo -u ec2-user echo $! > pid.txt
