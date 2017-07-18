# Installation
**NOTICE**
None of these methods work yet. I'm still working on uploading to both the AUR and PyPI. I will update this as I make progress.

**(Soon) Arch Linux:**  
Viento can be found in the AUR! Follow [this link](https://www.google.com). To install, make sure you've read through the Arch Linux [wiki page](https://wiki.archlinux.org/index.php/Arch_User_Repository#Installing_packages) on how to install packages from the AUR. In short, run these commands inside a directory in your home folder where you'd like to save AUR files:
```
$ git clone url
$ cd viento
$ makepkg -si

$ viento help
or
$ viento setup
```

**(Soon) PyPI:**  
As far as I can tell, if you install viento through PIP it should work for any Linux distribution. Install python 3.6 and pip through your distribution's package manager, then run these commands:
```
$ pip install viento

$ viento help
or
$ viento setup
```
