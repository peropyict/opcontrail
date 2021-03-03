#!/bin/bash
#LD_PRELOAD=/check_pf.so /hello &
#/hello &
#ssh -fNT -J root@10.219.117.11,stack@192.168.122.240 heat-admin@192.168.24.9 -L8095:127.0.0.1:8082
#ssh -fNT -J root@10.219.117.14 -L8095:10.219.117.14:8082 
ssh -J root@10.219.117.11,stack@192.168.122.241 heat-admin@192.168.24.6 -L8084:127.0.0.1:8083 -L8087:127.0.0.1:8087 -L15673:127.0.0.1:15673 -L8095:127.0.0.1:8095
tail -f /dev/null