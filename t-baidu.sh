#!/bin/sh

echo Hello World	
echo ----------Begin curl through Private Link----------
curl https://www.baidu.com --output baidu.txt
echo ----------End curl through Private Link----------

cat baidu.txt

nginx -g 'daemon off;'
