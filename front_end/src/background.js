'use strict'

import { app, protocol, BrowserWindow } from 'electron'
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib'
import installExtension, { VUEJS_DEVTOOLS } from 'electron-devtools-installer'
import path from 'path'
const isDevelopment = process.env.NODE_ENV !== 'production'

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } }
])

async function createWindow() {
  // Create the browser window.
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      
      // Use pluginOptions.nodeIntegration, leave this alone
      // See nklayman.github.io/vue-cli-plugin-electron-builder/guide/security.html#node-integration for more info
      nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION,
      contextIsolation: !process.env.ELECTRON_NODE_INTEGRATION
    }
  })

  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // Load the url of the dev server if in development mode
    await win.loadURL(process.env.WEBPACK_DEV_SERVER_URL)
    if (!process.env.IS_TEST) win.webContents.openDevTools()
  } else {
    createProtocol('app')
    // Load the index.html when not in development
    win.loadURL('app://./index.html')
  }
}

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) createWindow()
})

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', async () => {
  if (isDevelopment && !process.env.IS_TEST) {
    // Install Vue Devtools
    try {
      await installExtension(VUEJS_DEVTOOLS)
    } catch (e) {
      console.error('Vue Devtools failed to install:', e.toString())
    }
  }
  createWindow()
  // .then(sendToPython()); // python読み込み
})

// Set up Python
// C:\Users\RUTILEA\Desktop\o-katotech-panel-measurement\python
let pyProc = null;
let pyPort = null;

const PY_DIST_FOLDER = "dist_python";

const guessPackaged = () => {
  const fullPath = path.join(__dirname, PY_DIST_FOLDER);
  return require("fs").existsSync(fullPath);
};

const sendToPython = () => {
  pyProc = require('child_process').spawn('python', ['/Users/johnli/Documents/projects/rutilea_work/ic_chip/chip_project/front_end/dist_python/chip_backend.py']);
  pyProc.stdout.on('data', function (data) {
    console.log("Python response: ", data.toString('utf8'));
    result.textContent = data.toString('utf8');
  });

  pyProc.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pyProc.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
  });
}

const createPyProc = () => {
  let script = "chip_backend.py"
  let port = "" + 5000;
  let isTerminal = false;
  console.log(path.join(__dirname, "../" + PY_DIST_FOLDER))
  if (guessPackaged()) {
    console.log('packaged')
    pyProc = require("child_process").execFile(script, [port], {
      cwd: path.join(__dirname, "../" + PY_DIST_FOLDER)
    });
  } else {
    isTerminal = true;
    if (process.platform === "win32") {
      console.log('win32')
      pyProc = require("child_process").spawn(
        "python",
        [script], {
          cwd: path.join(__dirname, "../" + PY_DIST_FOLDER)
        }
      );
    } else {
      console.log('else type')
      pyProc = require("child_process").spawn("python", [script], {
        cwd: path.join(__dirname, "../" + PY_DIST_FOLDER)
      });
    }
  }

  if (pyProc != null) {
    //console.log(pyProc)
    console.log("child process success on port " + port);

    // FIXME
    if (isTerminal) {
      pyProc.stdout.on("data", data => {
        console.log(data);
      });
      pyProc.stderr.on("data", data => {
        pyProc.kill();
        pyProc = null;
        const option = {
          type: "warning",
          buttons: ["確認"],
          defaultId: 0,
          title: "エラー",
          message: "予期せぬエラーが発生しました。アプリを再度起動してください。"
        };
        dialog.showMessageBox(option).then(
          () => {
            allowQuit = true
            win.close()
          }
        );
        console.log(data);
      });
      pyProc.on("error", err => {
        console.log(err);
      });
    }
  }
};

// const exitPyProc = () => {
//   pyProc.kill();
//   pyProc = null;
//   pyPort = null;
// };

// app.on("will-quit", exitPyProc);

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
  if (process.platform === 'win32') {
    process.on('message', (data) => {
      if (data === 'graceful-exit') {
        app.quit()
      }
    })
  } else {
    process.on('SIGTERM', () => {
      app.quit()
    })
  }
}
