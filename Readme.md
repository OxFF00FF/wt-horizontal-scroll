# Windows Terminal Horizontal Scroll

Windows Terminal does not support horizontal scrolling, which can cause long lines to wrap or if the window is too narrow:

This app will add horizontal scrolling and remove line wrap.
It monitors hotkeys clicks using the windows API and modifies the windows terminal settings file.

By default, scrolling is enabled at startup and disabled when exiting via the tray menu or `Alt + Q`


# Setup
 1. download and setup [python](https://www.python.org/downloads/release/python-310)
 2. download code:
    - from github. Click `Code -> Download zip` and unpack zip archive
    
    or
    
    - run command in cmd `git clone https://github.com/OxFF00FF/wt-horizontal-scroll` in target dir ([Git](https://git-scm.com/install) required)
 
 3. run `START_WT.bat` This will launch program with a window and shows logs.
    
    or
    
    `START_WT headless.bat` Will launch program in headless mode in windows tray.

 4. Install depencies. Run `INSTALL.bat`

 5. Cofnig located in `%userprofile%/appdata/local/Packages/Microsoft.WindowsTerminal_8wekyb3d8bbwe/LocalState` in file `settings.json`. 
    Make a backup of this file before you start working, in case of program failures, so that you can restore WT settings.

# Hot Keys
 - `ALT + Right arrow` or `Mouse Scroll Down` shift the content from right to left
 - `ALT + Left arrow` or `Mouse Scroll Up` shift the content from left to right
 - `ALT + Down arrow` reset position to default
 - `ALT + Up arrow` toggle scrolling and line wrap