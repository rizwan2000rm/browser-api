from flask import Flask, request
import subprocess
import psutil
import os
import signal
import shutil

app = Flask(__name__)


browserData = {
    "firefox": {
        "process-name": "firefox",
        "data-dir": ""
    },
    "chromium": {
        "process-name": "chromium",
        "data-dir": os.environ['HOME'] + "/.config/chromium/Default",
        "session-dir": os.environ['HOME'] + "/.config/chromium/Default/Session/"
    },
    "microsoft-edge": {
        "process-name": "microsoft-edge",
        "session-dir": os.environ['HOME'] + "/.config/microsoft-edge-dev/Default"
    },
}


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/start")
def start_browser():
    browser = request.args.get('browser')
    url = request.args.get('url')

    subprocess.Popen([browser, url])

    return "<p>Browser started on server</p>"


@app.route("/stop")
def stop_browser():
    browser = request.args.get('browser')

    for pid in (process.pid for process in psutil.process_iter() if process.name() == browser):
        os.kill(pid, signal.SIGKILL)

    return "<p>Browser stopped</p>"


@app.route("/cleanup")
def clean_browser():
    browser = request.args.get('browser')
    dataDir = browserData[browser]["data-dir"]
    try:
        shutil.rmtree(dataDir)
    except OSError as e:
        print("Error: %s : %s" % (dataDir, e.strerror))

    return "<p>Browser history cleared</p>"


@app.route("/geturl")
def get_last_url():
    browser = request.args.get('browser')

    sessionDir = browserData[browser]["session-dir"]
    # db = plyvel.DB(sessionDir, create_if_missing=False)
    # sn = db.snapshot()

    snss_path = "/Path/To/Library/Application Support/Google/Chrome/Default/Current Session"
    snss_file = snss.SNSSFile(open(sessionDir))

    print(snss_file[0])

    # for key, value in sn:
    #     print(key)
    #     print(value)

    return "<p>Browser data printed</p>"
