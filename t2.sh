#!/bin/sh

apt install -y wget
echo Hello World	
echo ----------Begin curl through Private Link----------
echo ----------End curl through Private Link----------

nginx -g 'daemon off;'
