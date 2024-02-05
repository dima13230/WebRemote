from pynput import keyboard
from pynput.keyboard import Key, Controller
import json
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from flask import Flask, request, render_template
import re
import socket

from vkkeys import VKKey

class MyWatchdogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        load_config()

def split_string_ignore_quotes(string):
    # Regular expression pattern to match quoted strings or non-quoted sequences of characters
    pattern = r'(\'[^\']*\'|"[^"]*"|\S+)'
    matches = re.findall(pattern, string)
    return [match.strip('\'"') for match in matches]

macros = {}
config_path = "config.json"
def load_config():
    global macros
    global listener
    global config_data
    config = open(config_path)
    config_data = json.load(config)
    macros = config_data["macros"]
    
    if config_data["wake_up_phone"]:
        hotkey = keyboard.HotKey(
            keyboard.HotKey.parse(config_data["wake_up_shortcut"]),
            on_activate)
        listener = keyboard.Listener(on_press=for_canonical(hotkey.press), on_release=for_canonical(hotkey.release))
        listener.start()

# Global variables
app = Flask(__name__)
keyb = Controller()
macros = dict()
# #

# General macrofunctions
def key_press(args):
    pressed_keys = []
    for arg in args:
        key = ""
        if arg in Key.__members__:
            key = Key.__members__[arg]
        elif arg in VKKey.__members__:
            key = VKKey.to_KeyCode(VKKey.__members__[arg])
        else:
            key = arg
        keyb.press(key)
        pressed_keys.append(key)
    
    for key in pressed_keys:
        keyb.release(key)
    
def run_command(args):
    subprocess.run(args, stdout = subprocess.DEVNULL)
    
def mysleep(args):
    sleep_time = int(args[0])
    time.sleep(sleep_time)
    
str_to_funcref = {
    "key": key_press,
    "run": run_command,
    "sleep": mysleep
}
# #

# Flasky stuff
@app.route("/", methods=["GET", "POST"])
def flask_main():
    return render_template('webui.html')

@app.route("/request", methods=["POST"])
def run_macro():
    macro_arg = request.form.get('macro', type=str)
    if macro_arg != None:
        if macro_arg in macros:
            actions = macros[macro_arg]["actions"]
            for action in actions:
                action_tokens = split_string_ignore_quotes(action)
                command = str_to_funcref[action_tokens[0]]
                args = action_tokens[1:]
                command(args)
                
    else:
        print("Couldn't run macro")
    return ""

@app.route("/get_macro_info", methods=["POST"])
def get_macro_info():
    macro_arg = request.form.get('macro', type=str)
    if macro_arg != None:
        if macro_arg in macros:
            response = {
                "name": macros[macro_arg]["name"],
                "color": macros[macro_arg]["color"] if "color" in macros[macro_arg] else ""
            }
            return json.dumps(response)
    return ""

@app.route("/get_page_info", methods=["POST"])
def get_page_info():
    response = {
        "rows": config_data["rows"],
        "columns": config_data["columns"],
        "title": config_data["title"],
        "background": config_data["background"],
        "default_button_color": config_data["default_button_color"]
    }
    return json.dumps(response)

# #

# Key shortcut phone screen activation via ADB
def on_activate():
    subprocess.run(["adb", "shell", "input", "keyevent", "KEYCODE_POWER"])
def for_canonical(f):
    return lambda k: f(listener.canonical(k))
# #

event_handler = MyWatchdogHandler()
observer = Observer()
observer.schedule(event_handler, path=config_path, recursive=False)
observer.start()

load_config()

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()

    print("Your local IP address is {0}".format(ip))
    print("To access control panel, make sure that the device you connect from is in the same network. In web browser on end device type http://{0}:5000".format(ip))
    print("Currently there is no HTTPS support for this script, but it should be fine for as long as it is used inside local network only, so you can ignore the following warning about development server.")
    app.run(host=ip, port=5000)