#!/bin/bash
platform='DaYun'
base_dir='/data/backup'

#获取多少天内的日志信息
few_days=1

files=$(find ${base_dir} -type f -mtime -${few_days}|grep -v redis|grep -v mysql)
for f in ${files}
do
    md5=$(md5sum ${f}|awk {'print $1'})
    size=$(du -sh ${f}|awk {'print $1'})
    f=$(echo ${f}|sed "s!${base_dir}!${platform}!g")
    name=$(echo ${f}|awk -F / {'print $NF'})
    path=$(echo ${f%/*}/)
    l=${l}'{"'name'":"'${name}'","'path'":"'${path}'","'md5'":"'${md5}'","'size'":"'${size}'"},'
done
l=$(echo ${l}|sed 's/,$//')
l='{"'platform'":"'${platform}'","'data'":['${l}']}'
#echo ${l}
curl -X POST \
-H 'Authorization: Token af78aab83b5f71de9c68e2fa545b16d0a2ac0bd6' \
-H "Content-Type:application/json" \
http://192.168.1.169/api/log-mis/v1/records/update/ -d ${l}
