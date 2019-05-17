# cd Vue/app
# echo "Installing Vue Dependencies"
# npm install
# echo "Building Vue app"
# npm run build
# cd ..
# cd ..
# echo "Removing Previous Builds"
# rm -r Flask/dist
# rm -r Flask/build
# cd Flask
# echo "Compiling Python Backend as standalone executable."
# pyinstaller deploy.spec --additional-hooks-dir hooks
# echo "Deleting previous versions of the compiled backend from the electron folder."
# cd ..
# rm -r Electron/app/model/*
# echo "Copying the flask backend into the electron application folder."
# mv Flask/dist/run-dev Electron/app/model/run-dev
# echo "Creating OSX Application Bundle"
# electron-packager Electron/app EnergySharing
# echo "Copying run command into the containing folder."
# cp ./deploy_extras/* ./EnergySharing-darwin-x64
echo "Setting executable permissions on the run command."
chmod +x ./EnergySharing-darwin-x64/EnergySharing.command
echo "Moving the .app file into a subfolder"
mkdir ./EnergySharing-darwin-x64/src
mv ./EnergySharing-darwin-x64/EnergySharing.app ./EnergySharing-darwin-x64/src
echo "Finished"



