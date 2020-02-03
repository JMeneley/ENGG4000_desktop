# ENGG4000_desktop
Repository for general desktop application resources

**You must run this on a computer that supports BLE, I don't think that any of the computers at the school do. This should work on MacOS but I am not entirely certain**

# Setup
 - Install python 3.7 (https://www.python.org/downloads/release/python-376/)
 - Clone this repo
 - Open a terminal and navigate to this folder, run the command `pip install -r requirements.txt`
  - pip is a package(library) manager for Python and the command above installs all the packages you need
  
# Testing
 - In the repo is a file called `api_test.py` that shows how the wearable_api should be used, running this file will connect to the wearable, enable notifications, receive data for 5 seconds, and then disconnect
 
