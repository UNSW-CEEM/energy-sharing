#!/bin/bash
killall run-dev
cd `dirname $0`
open -a EnergySharing.app &
pwd
cd EnergySharing.app/Contents/Resources/app/model/run-dev/
./run-dev
killall run-dev

