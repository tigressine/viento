# AutoClone
Python utility to automate copies, syncs, and moves performed by rclone. This tool will allow you to sync local files to remote cloud servers (like Google Drive, OneDrive and Amazon) and vice versa. The file transfers occur at custom intervals and the finished product will include some psuedo-machine learning, where the scripts are able to predict heavy usage periods for file directories and increase transfer intervals during these times.  

Beta release. Everything works, but manual installation is still required. Move 'autoclone', 'acdaemon.py', and 'acsetup.py' to '/usr/bin'. Move autoclone.service to '~/.config/systemd/user' (create it if it doesn't exist). Finally run the command 'autoclone setup' and you should see the setup utility. Requires python 3.6, rclone, and termcolor installed. You can get python 3.6 through Pacman (I'm building this on Arch Linux at the moment, so that's all I currently support. May expand later). rclone is located in the AUR. Install termcolor through PIP ('pip install termcolor'). If you don't have pip you'll have to install that too, and I believe it is available through Pacman. Setup rclone before setting up AutoClone (follow his documentation).

Author: tgsachse (Tiger Sachse)  
Initial Release: 7/13/2017  
Current Release: 7/13/2017  
Version: 0.1.0-beta 
License: GNU GPLv3  
