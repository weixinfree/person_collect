package=$1
adb shell dumpsys gfxinfo ${package} | grep ${package} | tail -1 | awk -F / '{print $2}'
