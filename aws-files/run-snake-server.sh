#!/bin/bash
cd /home/ec2-user/snake
source ./bin/activate

cd src/server
# This way the output of main.py will be written to log.txt
# But, unfortunately, not before the process ends
sudo -u ec2-user python3 main.py > log.txt &
sudo -u ec2-user echo $! > pid.txt
