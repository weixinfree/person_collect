ls | while read name; do  echo -n "$name :  "; find $name -name '*.java' | xargs -n1 wc -l | awk '{sum+=$1}END{print sum}'; done | sort -n -k 2 -t :
