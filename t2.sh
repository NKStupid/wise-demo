#!/bin/sh

echo Hello World	
echo ----------Begin curl through Private Link----------
curl http://vpce-0f9b25165e4882a9f-wtxlncsb-cn-northwest-1b.vpce-svc-0af8167c9dcc695ad.cn-northwest-1.vpce.amazonaws.com.cn:8080/order_mgmt/internal_events/v1/ce_im_dummy_request_1a55dded-2740-494e-a650-f34dc06a8282 --output baidu.txt
echo ----------End curl through Private Link----------

cat baidu.txt

nginx -g 'daemon off;'
