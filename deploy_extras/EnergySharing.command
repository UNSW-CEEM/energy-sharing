#!/bin/bash
killall run-dev
echo $0
# Enter the project directory - need the extra dashes etc. to handle spaces in the path name.
cd -- "$(dirname -- "$0")"
pwd
cd src
open -a EnergySharing.app &
cd EnergySharing.app/Contents/Resources/app/model/run-dev/
./run-dev

