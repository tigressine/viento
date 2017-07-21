# Viento Cloud Management Utility

Viento (Spanish for 'wind') allows you to move through the clouds with ease! This utility is designed on top of [rclone](https://rclone.org/), and is intended to allow users to automatically sync/copy/move files and directories to and from local and remote destinations. Here are a few examples of what Viento can do.

-Copy your music files from your Amazon Drive to Microsoft OneDrive every 2 hours.  
-Sync your Google Photos with Dropbox every 10 minutes.  
-Backup your Microsoft OneDrive and Dropbox onto a local drive every 24 hours.  
-Copy your dotfiles into a dotfile folder on your Google Drive.  

Viento is under active development and, with each update, aims to support more and more of rclone's extensive features, as well as add some features of its own. Viento is a daemon, so after setup it will continually run in the background to keep your stuff synced. When viento is not syncing it is asleep, which means it has a very small footprint on your machine. I'd like to give a big shoutout to [Nick Craig-Wood](https://github.com/ncw) and all his [contributing authors](https://rclone.org/authors/) for building an amazing piece of software in rclone!

[Installation](INSTALL.md)

TODO:  
[] Finish command interface.  
[] Warn shutdown process if transfer is happening.  
[] Implement machine learning to change intervals based on use patterns.  
[] Add rclone setup into Viento setup.  

Author: tgsachse (Tiger Sachse)  
Initial Release: 7/13/2017  
Current Release: 7/21/2017  
Version: 0.4.0-beta  
License: GNU GPLv3 
