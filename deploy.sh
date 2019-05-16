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
mv Flask/dist/run-dev Electron/app/model/run-dev
echo "Creating OSX Application Bundle"
electron-packager Electron/app EnergySharing



