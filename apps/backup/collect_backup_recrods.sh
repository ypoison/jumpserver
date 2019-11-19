#!/bin/bash
platform='King'
base_dir='/data/backup'
files=$(find ${base_dir} -type f -mtime -100|grep -v redis|grep -v mysql)
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
curl -X POST -H 'Authorization: Token 700987c7e556d59521d61588881cbcc505a53ed2' -H "Content-Type:application/json" http://localhost/api/backup/v1/records/update/ -d ${l}
