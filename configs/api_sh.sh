#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Error, usage: $0 <your url>"
    exit 1
fi

url=$1
# curl
short=`curl -s http://t34.me/api/?u=${url}`
echo $short
# wget
short=`wget -qO- http://t34.me/api/?u=${url}`
echo $short
exit 0
