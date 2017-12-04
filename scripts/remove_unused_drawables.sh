#!/usr/bin/env bash

# 删除不再使用的drawable资源

echo '开始扫描引用到的drawable资源...'

python3 track_code_gen/remove_unused_drawable.py

echo 'WARN: 寻找无用资源的算法，基于文本查找。存在2个问题：1. 潜在的文本匹配错误 2. 不能反映反射获取资源的情况'
echo '所以：需要删除的图片，确认无误后再进行删除'
echo ''
echo 'xiaoying***.png 系列图片存在反射调用，不应该删除'
echo 'yipitiezhi***.png 系列图片存在反射调用，不应该删除'
