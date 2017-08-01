# Change Log
**0.5.0 Beta**  
* Added UPCOMING.md and CHANGES.md  
* Revamped the docstrings for all methods across the program  
* Centralized all logging for clarity and scalability  
* Added statistics  
* Renamed 'links' to 'drafts' (a wind pun I'm pretty proud of)  
* Completely rewrote the viento_daemon  
* Properly implemented signal handling for SIGUSR1 and SIGUSR2  
* BUGFIX: no more infinite loop when trying to edit a draft in viento_setup  
* BUGFIX: the correct number of logs will now persist, instead of 2 fewer than desired (default 5)  

**0.4.0 Beta**  
* Added new force command  
* Created a viento_utils module to house methods being used across all 3 other scripts  
* BUGFIX: fixed weird behavior being caused by job.dat files not being overwritten properly  
* BUGFIX: fixed some issues arising from spelling errors  

**0.3.0 Beta**  
* Renamed to viento  
* Fixed issues with installation paths  

**0.2.0 Beta**  
* Renamed to wind  

**0.1.0 Beta**  
* First beta release  
* Mostly functional, but requires manual installation  

**0.0.1 Alpha**  
* Named AutoClone  
* Scripts are functioning  
