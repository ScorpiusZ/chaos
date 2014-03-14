#!/bin/bash


topfundir=${3%.zip}
if [ ! -d "$topfundir" ];then
unzip $3 && echo 'Unzip Success' || echo 'Unzip Failed'
echo "Topfun Sdk dir :$topfundir"
fi
cd $topfundir && echo "Cd $topfundir" || echo "Cd  $topfundir Failed"
java -jar gen.jar $1 && echo 'General project Succeful' ||echo 'General project Failed' 
projectdir=${1//./_}
echo "projectdir=$projectdir"


#delete old sdk.jar
rm $2/libs/topfunsdk*.jar

cp -av $projectdir/assets/webview/ $2/assets/webview/
echo cp -av $projectdir/assets/webview/ $2/assets/webview/
cp -av $projectdir/libs/ $2/libs/
echo cp -av $projectdir/libs/ $2/libs/
cp -av $projectdir/res/anim/ $2/res/anim/
echo cp -av $projectdir/res/anim/ $2/res/anim/
cp -av $projectdir/res/drawable/ $2/res/drawable/
echo cp -av $projectdir/res/drawable/ $2/res/drawable/
cp -av $projectdir/res/drawable-hdpi/ $2/res/drawable-hdpi/
echo cp -av $projectdir/res/drawable-hdpi/ $2/res/drawable-hdpi/
cp -av $projectdir/res/drawable-ldpi/ $2/res/drawable-ldpi/
echo cp -av $projectdir/res/drawable-mdpi/ $2/res/drawable-mdpi/
cp -av $projectdir/res/layout/ $2/res/layout/
echo cp -av $projectdir/res/layout/ $2/res/layout/
cp -av $projectdir/res/layout-480x320/ $2/res/layout-480x320/
echo cp -av $projectdir/res/layout-480x320/ $2/res/layout-480x320/
cp -av $projectdir/res/layout-800x480/ $2/res/layout-800x480/
echo cp -av $projectdir/res/layout-800x480/ $2/res/layout-800x480/
cp -av $projectdir/res/layout-854x480/ $2/res/layout-854x480/
echo cp -av $projectdir/res/layout-854x480/ $2/res/layout-854x480/
cp -av $projectdir/res/raw/ $2/res/raw/
echo cp -av $projectdir/res/raw/ $2/res/raw/
cp -av $projectdir/res/values/topfun* $2/res/values/
echo cp -av $projectdir/res/values/topfun* $2/res/values/
cp -av $projectdir/res/values-large/ $2/res/values-large/
echo cp -av $projectdir/res/values-large/ $2/res/values-large/
cp -av $projectdir/res/xml/ $2/res/xml/
echo cp -av $projectdir/res/xml/ $2/res/xml/
cp -av $projectdir/src/com/blsm/topfun/R.java $2/src/com/blsm/topfun/
echo cp -av $projectdir/src/com/blsm/topfun/R.java $2/src/com/blsm/topfun/

