#!/bin/sh
filefrom=$1
fileto=$2
fromheadstr=$3
fromtailstr=$4
toheadstr=$5
totailstr=$6

echo "filefrom : $filefrom fileto : $fileto "
echo "fromheadstr : $fromheadstr fromtailstr : $fromtailstr"
echo "toheadstr : $toheadstr totailstr : $totailstr"
from=`grep -nm 1 "$fromheadstr" $fileto|cut -d ':' -f 1`
echo $from
to=`grep -nm 1 "$fromtailstr" $fileto |cut -d ':' -f 1`
echo $to
sed -n "1,$from p" $fileto>>$fileto.bak
echo "write 1-$from to $fileto.bak"
sed -n "/$toheadstr/,/$totailstr/p" $filefrom>>$fileto.bak
sed -n "/$toheadstr/,/$totailstr/p" $filefrom
echo "write replace text  to $fileto.bak"
sed -n "$to,$ p" $fileto>>$fileto.bak
echo "write $to-last to $fileto.bak"
rm $fileto&&mv $fileto.bak $fileto
echo "change $fileto.bak to $fileto"

