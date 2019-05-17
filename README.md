# Local Energy Sharing Simulator
This software is designed to model emerging business models, based on the concept of sharing energy between residences or businesses with solar and battery systems. 

It is based on the work of Mike Roberts, Luke Marshall and Naomi Stringer at the Center for Energy and Environmental Markets, UNSW. Additional software development has been completed by David Martin. 

![Screenshot 2019-05-17 12 04 13](https://user-images.githubusercontent.com/7201209/57900484-f52ad600-789b-11e9-98eb-91410324fad5.png)
![Screenshot 2019-05-17 12 03 19](https://user-images.githubusercontent.com/7201209/57900486-f5c36c80-789b-11e9-9a06-bd73106e7aa4.png)
![Screenshot 2019-05-17 12 03 01](https://user-images.githubusercontent.com/7201209/57900487-f5c36c80-789b-11e9-920c-e6515eea7915.png)
![Screenshot 2019-05-17 12 02 41](https://user-images.githubusercontent.com/7201209/57900488-f5c36c80-789b-11e9-9d8c-e53861a14708.png)
![Screenshot 2019-05-17 12 02 15](https://user-images.githubusercontent.com/7201209/57900489-f65c0300-789b-11e9-84e0-7fd8d3416ce7.png)

# Downloading
The current standalone release can be downloaded from the Releases page [here](https://github.com/luke-marshall/energy-sharing/releases).

# Running
1. Download and unzip the app. 
2. Double-Click the EnergySharing.command file. This will open a terminal window (the 'backend' calculator doing all the hard work) and the user interface. 
3. When you're finished, please quit both the user interface and the terminal app.


# Running from source
The application can also be run directly from the source code - this will be useful if there does not exist a packaged binary for your operating system, or if other issues are encountered running packaged versions. Running from source is relatively straightforward with basic knowledge of the terminal and common terminal apps. 

## Requirements:
node.js and npm
python 3 and pipenv
electron (for standalone)

## Steps
1. Navigate to Vue/app folder and run:
   `npm install`
   `npm run serve`
This serves the frontend portion of the app reactively, such that changes to the source code are reflected instantly in the browser / UI.

2. Navigate to Flask folder. Run:
   `pipenv install`
   `pipenv run python run-dev.py`

At this point, the frontend should be available by opening the Chrome browser and navigating to localhost:8080 in the address bar. localhost:5000 may also provide a version of the UI but this will not be in sync with the code in Vue/app, so this is not recommended. 


## Packaging
Packaging consistes of three rather unintuitive steps. The first is to package the vue frontend, and place it in the Flask section of the app. The second is to take the Flask section (the backend model and webserver that serves the frontend ) and package these into a system-dependent executable using pyinstaller - to be places in the Electron section. Electron, on start, fires up this server (the model and the UI) and displays it in a nice electron window.

The absic packaging steps for osx are captured in the 'deploy.sh' shell script. This requires that pyinstaller, plus all of the python dependencies for the app, are installed on a local python3 instance, as pyinstaller has pipenv conflicts. 

1. Vue
To build the package, go to the Vue/app folder and run:
`npm run build`
This will package the entire web frontend and place it into the Flask/app/application/dist directory. 
From this directory, the FLASK server will serve the final version of the frontend.

2. Python
All python packages must be installed on system python (due to a bug with pipenv / pyinstaller - this may be fixed in the future.)

Run the script found in package.sh, ie.
`pyinstaller deploy.spec --additional-hooks-dir hooks`

This will create a folder 'dist' in the Flask section, with an executable called 'run-dev'. Run it and we're up, up and away!

Copy the generated relevant files into the 'app/model' folder in Electron.

3. Electron

Electron packaging can be done manually with instructions from the official electron documentation.

We have used the (Electron Packager | https://github.com/electron-userland/electron-packager) tool as it greatly simplifies the process.



