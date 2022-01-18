#!/bin/sh

yum install -y wget
echo Hello World	
echo ----------Begin curl through Private Link----------
wget https://www.google.com
echo ----------End curl through Private Link----------

nginx -g 'daemon off;'
