# energy-sharing


# Packaging
Packaging consistes of three rather unintuitive steps. The first is to package the vue frontend, and place it in the Flask section of the app. The second is to take the Flask section (the backend model and webserver that serves the frontend ) and package these into a system-dependent executable using pyinstaller - to be places in the Electron section. Electron, on start, fires up this server (the model and the UI) and displays it in a nice electron window.

## Vue
To build the package, go to the Vue/app folder and run:
`npm run build`
This will package the entire web frontend and place it into the Flask/app/application/dist directory. 
From this directory, the FLASK server will serve the final version of the frontend.

## Python
All python packages must be installed on system python (due to a bug with pipenv / pyinstaller - this may be fixed in the future.)

Run the script found in package.sh, ie.
`pyinstaller deploy.spec --additional-hooks-dir hooks`

This will create a folder 'dist' in the Flask section, with an executable called 'run-dev'. Run it and we're up, up and away!

Copy the generated relevant files into the 'app/model' folder in Electron.

## Electron

Electron packaging can be done manually with instructions from the official electron documentation.

We have used the (Electron Packager | https://github.com/electron-userland/electron-packager) tool as it greatly simplifies the process.



