#!/bin/bash

delta1=$1
z00=$2
R=$(halcmd getp lineardeltakins.R)


newR=$(echo "$R - $delta1" | bc)
#echo "#old  new          [below = 0, above = 1]"      >> ~/machinekit/calibration.log
echo "$R    $newR   $z00" >> ~/machinekit/calibrationR.log


halcmd setp lineardeltakins.R $newR
echo "lineardelta.R : $R $newR"
