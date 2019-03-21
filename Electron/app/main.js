const {app, BrowserWindow} = require('electron')

let win = null;


var executablePath = "model/run-dev/run-dev";
var child = require('child_process').spawn(executablePath);


app.on('ready', function () {
    // Initialize the window to our specified dimensions
    win = new BrowserWindow({width: 1000, height: 600});

    // Specify entry point to default entry point of vue.js
    // win.loadURL('http://localhost:8080'); //this one for the hot-loading dev server run via npm run serve in the vue directory
    win.loadURL('http://localhost:5000'); //this one for production, post-build, from the python directory.

    // Remove window once app is closed
    win.on('closed', function () {
        win = null;
    });

});

//create the application window if the window variable is null
app.on('activate', () => {
    if (win === null) {
        createWindow()
    }
})

//quit the app once closed
app.on('window-all-closed', function () {
    child.kill('SIGINT');
    if (process.platform !== 'darwin') {
        
        app.quit();
    }
});
