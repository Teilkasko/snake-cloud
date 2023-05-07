#!/bin/bash

# Userdata script to deploy the app on an AWS EC2 machine running Amazon Linux

yum install -y git python3-pip
sudo -u ec2-user pip3 install virtualenv

cd /home/ec2-user
git clone --branch develop https://github.com/fsolaroli/SnAkE.git snake
cd snake/
virtualenv .
chown -R ec2-user:ec2-user .

source ./bin/activate
sudo -u ec2-user pip3 install -r requirements.txt

cp aws-files/startup.service /lib/systemd/system/startup.service
systemctl enable startup.service --now
