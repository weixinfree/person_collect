adb shell dumpsys gfxinfo com.meelive.ingkee | grep com.meelive.ingkee | tail -1 | awk -F / '{print $2}'
