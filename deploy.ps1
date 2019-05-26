Write-Host "Starting deploy script. "
cd .\Vue\app
Write-Host "Installing Vue Dependencies"
# npm install
Write-Host "Building Vue Project"
npm run build
cd ..
cd ..
Write-Host "Removing Previous Python Excutable Builds"
Remove-Item .\Flask\dist -Recurse -Force
Remove-Item .\Flask\build -Recurse -Force
cd Flask
Write-Host "Compiling Python Backend as standalone executable."
pyinstaller deploy.spec --additional-hooks-dir hooks
Write-Host "Deleting previous versions of the compiled backend from the electron folder."
cd ..
Remove-Item .\Electron\app\model\* -Recurse -Force
Write-Host "Copying the flask backend into the electron application folder."
Move-Item -Path .\Flask\dist\run-dev -Destination .\Electron\app\model\run-dev
echo "Creating Windows Application Bundle"
electron-packager .\Electron\app EnergySharing
echo "Creating new directory for compiled app."
New-Item -ItemType directory -Path .\EnergySharing
echo "Moving compiled app and contents into the new folder."
Move-Item -Path .\EnergySharing-win32-ia32 -Destination .\EnergySharing
echo "Copying run command into the containing folder."
cp .\deploy_extras_windows\* .\EnergySharing