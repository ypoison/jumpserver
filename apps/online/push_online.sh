#!/bin/bash
platform='DaYun
King
DaLi
KK
DaNiu
XianNiu
JZJ
LianSHeng
Bobo
QuanMin
YinHe
XiaoMi
JinSha
WeiNiSi
ALi
'

#'
#1575594000000
#1575597600000
#1575601200000
#1575602724000
#'
time=1575907432000
d=3600000
function rand(){
  min=$1
  max=$(($2-$min+1))
  num=$(cat /proc/sys/kernel/random/uuid | cksum | awk -F ' ' '{print $1}')
  echo $(($num%$max+$min))
}
for p in ${platform}
do
	for ((i=1; i<=24; i++))
	do
		rnd=$(rand 1 500)
		l='{"time":'${time}',"online_num":'${rnd}',"push_num":1,"platform":"'${p}'"}'
		time=`expr ${time} + ${d}`
		echo ${l}
		curl -X POST \
		-H 'Authorization: Token af78aab83b5f71de9c68e2fa545b16d0a2ac0bd6' \
		-H "Content-Type:application/json" \
		http://192.168.1.230/api/online/v1/number/update/ -d ${l}
	done
done