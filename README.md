# WebRemote

A python application that allows creating custom macros accessible in local network via web interface.

## Why using it?

Sometimes we have to manually perform various operations on the computer that could be automated with a single button press. Sometimes the task can be accomplished by pressing a sometimes inconvenient combination of keys, and sometimes our keyboard doesn't have the necessary keys for the job (e.g. numpad). At the same time, we may have an old but working smartphone lying idle somewhere, which, thanks to `WebRemote`, could become a remote control for your computer. By pressing a single button on the smartphone, a whole sequence of events can be executed on the computer, or any key on the keyboard can be emulated, and a specified application or applications can be launched. No applications need to be installed on the phone, as the control is performed through the local web interface. The main requirement is that the computer and the smartphone are connected to the same local network.

## How to use it?

Before you start using it, make sure you have Python installed on your system. Then open a terminal in the application folder and install all dependencies using the command:
```sh
pip install -r requirements.txt
```

If you are using a *nix system or WSL, it is recommended to run the application through a script file called `start`. It will deploy the Flask web server under the local address of your device and provide you with the IP address and port to connect to.

At the moment the application has not been tested in the Windows environment, so there are no instructions for running it on that system, although the process should be no different for *nix systems, except for the lack of support for the `start` script.

## Setting it up

For storing configuration data, `WebRemote` uses JSON config file named `config.json`. It has following fields and parameters:
* `rows` specifies amount of rows in the web interface;
* `columns` specifies amount of columns in the web interface;
* `title` specifies tab title of the web interface;
* `background` sets background color of the web interface;
* `default_button_color` sets default background color for the buttons without color specifically defined;
* `wake_up_phone` is a function that toggles your phone screen on/off on computer keyboard shortcut, if your phone is configured to work with ADB;
* `wake_up_shortcut` keyboard shortcut that should toggle your phone screen;
* `macros` contains information about macros.

### Creating your own macros

Let's take a look at an example macro and examine its parameters:

```js
"0,0": {
    "name": "Macro",
    "color": "#9900cc",
    "actions": [
        "key a",
        "sleep 1",
        "run /home/user/script.sh"
    ]
}
```

In this example: 
* `0,0` indicates the position of the macro on the grid. The position starts at zero, the number before the comma indicates a column, and the number after the decimal point indicates a row;
* `name` is the name of the macro, the button on the grid will have this text on it;
* `color` sets custom color of the button. Leave empty to use default color;
* `actions` represents a sequence of actions macro will do when ran.

#### Macro actions

Each macro action has the following syntax:
[command] [argument 1] [argument 2] .. [argument n].

Currently available actions are:
* `key [key 1] [key 2] [..] [key n]` emulates keyboard presses. You can pass as many arguments to it as you want and the macro will press them _simultaneously_. A key can be an alphanumeric character or, if it's a special symbol or a key, a string that represents pynput's `Key` class member.
Available values for special symbols or keys:
```
alt
alt_l
alt_r
alt_gr
backspace
caps_lock
cmd
cmd_l
cmd_r
ctrl
ctrl_l
ctrl_r
delete
down
end
enter
esc
f1
f2
f3
f4
f5
f6
f7
f8
f9
f10
f11
f12
f13
f14
f15
f16
f17
f18
f19
f20
home
left
page_down
page_up
right
shift
shift_l
shift_r
space
tab
up
media_play_pause
media_volume_mute
media_volume_down
media_volume_up
media_previous
media_next
insert
menu
num_lock
pause
print_screen
scroll_lock
```

* `sleep [seconds]` delays execution of the following actions by specified amount of seconds.
* `run [app] [argument 1] [argument 2] [..] [argument n]` runs specified application (or command) with given arguments. Please note that the `~` symbol is not supported and will not point to the user home directory. Consider writing an absolute path instead.