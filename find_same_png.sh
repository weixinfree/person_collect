#!/usr/bin/env bash

index=0
temp_file=temp
find . -name '*.png' | grep -v build | grep -v analyze | xargs -n1 md5 | awk '{print $2,$4}' > ${temp_file}

cat ${temp_file} | awk '{print $2}' | while read md5; do
    count=`cat ${temp_file} | grep ${md5} | wc -l`

    if [ ${count} -gt 1 ]; then
        index=`expr ${index} + 1`
        echo
        echo '\033[31m '${index}' find duplicate png files (md5: '${md5}')(duplicate count: '${count}') : \033[0m'
        cat ${temp_file} | grep ${md5} | awk '{print $1}' | awk -F '[()]' '{print $2}' | xargs -n1 ls -l | awk '{printf "%s %.2fK\n", $9 , $5/1024.0}'
        echo
    fi
done

rm ${temp_file}