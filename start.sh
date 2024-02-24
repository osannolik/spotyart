#!/bin/bash

echo "Start display application..."

export DISPLAY=:0.0

cd /home/pi/repos/spotyart/

source auth.sh

python app_gtk3.py
