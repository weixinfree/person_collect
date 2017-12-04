#!/usr/bin/env bash

file=large_png.txt
rm ${file}

echo "体积大的图片>>>" >> ${file}
echo '' >> ${file}

find . -name '*.png' | grep -v build | grep -v analyze | grep -v .9 | xargs ls -l | awk '/[1-9][1-9]{5,}/{printf "%s: %.2fK\n",$9, $5/1024}' >> ${file}

echo '' >> ${file}
echo "尺寸大的图片>>>" >> ${file}
echo '' >> ${file}

find . -name '*.png' | grep -v build | grep -v analyze | grep -v .9 | xargs -n1 file |  awk '/[1-9][0-9]{3,}/{print}' >> ${file}
