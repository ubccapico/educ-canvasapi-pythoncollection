All of the following scripts were written in Python 3.6.5. If anything used in the scripts is deprecated in newer versions of Python or the non-standard modules, please feel free to send in a pull request with the updated code if none of the authors have updated them.

There is a little bit of setup before you can run the scripts from the command line.

## Installing Python:
Before you can run any of the scripts, you will need to install a version of the language that the scripts are written in. You can find the latest releases here (Links to an external site.)Links to an external site.. When installing make sure to get the latest 3.x.x version of Python. Python 2.7 has been relegated to legacy at this point in time. To install, find the the executable installer for the system you are currently using and download it. While installing the downloaded version of python, you should go for a custom installation. Make sure to uncheck "for all users (requires elevation)" in optional features. If you uncheck it, you can install python without admin privileges. Under advanced option, also make sure that "install for all users" is unchecked. Make sure the install button does not show the Admin shield on the button, if it appears then one of the previously mentioned options is still checked. You can then continue with installation with the default options. Now you have the lastest 3.x.x version of Python installed!

## Installing Non-Standard Modules That The Scripts Are Dependent On:
There are three non-standard modules being used in the following scripts. You can install them using CMD and the following terminal commands:

```
pip3 install Unidecode
pip3 install beautifulsoup4
pip3 install requests
```

## Running the scripts
In your shell or terminal, go into the folder where all these scripts are located and run the Main.py file using the commend:
```
python3 Main.py
```
You'll then be presented with a menu asking which script you'd like to run along with some other prompts to complete what you're working on.
