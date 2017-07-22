# Installation
**Arch Linux:**  
Viento can be found in the AUR by following [this link](https://aur.archlinux.org/packages/viento-git/)! To install, make sure you've read through the Arch Linux [wiki page](https://wiki.archlinux.org/index.php/Arch_User_Repository#Installing_packages) on how to install packages from the AUR. In short, run these commands inside a directory in your home folder where you'd like to save your AUR files (such as *~/AUR*):
```
$ git clone https://aur.archlinux.org/viento-git.git
$ cd viento-git
$ makepkg -si
```
After making the package and installing it through Pacman you'll need to configure rclone. Run this command:
```
$ rclone config
```
Now everything is ready to go! Execute one of the following commands to get started:
```
$ viento help
or
$ viento setup
```

**(Soon) PyPI:**  
I plan to add PyPI/pip support soon to reach as large a Linux audience as possible.

**Manual Install:**  
Only install this way if I have not yet added support for your distro and you cannot install through pip. Before you start, make sure you have *python 3.6*, *python-termcolor*, and *rclone* properly installed. I highly recommend installing these through your distro's package manager rather than trying to manually install them.

To begin, change to a directory where you'd like to download the setup files (like *~/tmp*) then execute these commands:
```
$ git clone https://github.com/tgsachse/viento.git
$ cd viento
```
Now you have all the necessary files in a directory named *viento*. To grant execute permissions to all *.py* files:
```
$ chmod +x viento viento_daemon.py viento_setup.py viento_utils.py
```
Next you will move the 4 included *.py* files to their final location. The first file, named *viento* with no file extension, must be moved to */usr/bin*. The remaining 3 files, *viento_daemon.py*, *viento_setup.py*, and *viento_utils.py* all have to be sent to your Python install's *site-packages* folder. Execute the following commands to move everything (these use *site-packages*'s default location, however this location could be different for you if you have a weird python setup:
```
$ sudo mv viento /usr/bin
$ sudo mv viento_daemon.py /usr/lib/python3.6/site-packages
$ sudo mv viento_setup.py /usr/lib/python3.6/site-packages
$ sudo mv viento_utils.py /usr/lib/python3.6/site-packages
```
Almost done! Assuming everything went well, you'll need to configure rclone before you can use viento. Run this command:
```
$ rclone config
```
Setup is finished and now you can use viento! Run one of these commands to get started, or check out the user manual:
```
$ viento help
or
$ viento setup
or
$ man viento #NOT YET IMPLEMENTED
```
Feel free to delete the *viento* directory that you made when you ran the *git clone* command.
