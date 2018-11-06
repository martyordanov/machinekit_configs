#!/bin/bash

delta0=$1 # Towet C Maybe x
delta1=$2 # Tower A Maybe y
delta2=$3 # Tower B Maybe z

home0=$(halcmd getp axis.0.home)   # Tower C
home1=$(halcmd getp axis.1.home)   # Tower A
home2=$(halcmd getp axis.2.home)   # Tower B
R=$(halcmd getp lineardeltakins.R) #
L=$(halcmd getp lineardeltakins.L) #


newHome0=$(echo "$home0 - $delta0" | bc) # Tower C
newHome1=$(echo "$home1 - $delta1" | bc) # Tower A
newHome2=$(echo "$home2 - $delta2" | bc) # Tower B
echo "#           old      new          lineardeltakins.R   lineardeltakins.L"      >> ~/machinekit/calibration.log
echo "home 0 : $home0     $newHome0     $R     $L" >> ~/machinekit/calibration.log
echo "home 1 : $home1     $newHome1     $R     $L" >> ~/machinekit/calibration.log
echo "home 2 : $home2     $newHome2     $R     $L" >> ~/machinekit/calibration.log

halcmd setp axis.0.home $newHome0
halcmd setp axis.0.home-offset $newHome0
echo "home 0 : $home0     $newHome0"

halcmd setp axis.1.home $newHome1
halcmd setp axis.1.home-offset $newHome1
echo "home 1 : $home1     $newHome1"

halcmd setp axis.2.home $newHome2
halcmd setp axis.2.home-offset $newHome2
echo "home 2 : $home2     $newHome2"
