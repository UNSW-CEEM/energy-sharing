cd Vue/app
echo "Installing Vue Dependencies"
npm install
echo "Building Vue app"
npm run build
cd ..
cd ..
echo "Removing Previous Builds"
rm -r Flask/dist
rm -r Flask/build
cd Flask
echo "Compiling Python Backend as standalone executable."
pyinstaller deploy.spec --additional-hooks-dir hooks
echo "Deleting previous versions of the compiled backend from the electron folder."
cd ..
rm -r Electron/app/model/*
echo "Copying the flask backend into the electron application folder."
mv Flask/dist/run-dev Electron/app/model/run-dev
echo "Creating OSX Application Bundle"
electron-packager Electron/app EnergySharing
# echo "Copying backend shell script into the .app package."
# cp EnergySharing ./EnergySharing-darwin-x64
# cd EnergySharing-darwin-x64
# cd EnergySharing.app
# cp ../EnergySharing ./EnergySharing #this gets a bit convoluted because cp sees the .app as a file and overwrites if you try to cp into it directly from root. 
# chmod +x EnergySharing
# cd ..
# rm EnergySharing
echo "Copying run command into the containing folder."
cp ./run.command ./EnergySharing-darwin-x64
chmod +x ./EnergySharing-darwin-x64/run.command
echo "Finished"



