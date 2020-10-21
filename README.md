# wp_hunter ![Supported Python versions](https://img.shields.io/badge/python-3.6+-blue.svg?style=flat-square&logo=python)

Static analysis to search for vulnerabilities in Wordpress plugins.

```
 __      ____________  ___ ___               __                
/  \    /  \______   \/   |   \ __ __  _____/  |_  ___________ 
\   \/\/   /|     ___/    ~    \  |  \/    \   __\/ __ \_  __ \
 \        / |    |   \    Y    /  |  /   |  \  | \  ___/|  | \/
  \__/\  /  |____|____\___|_  /|____/|___|  /__|  \___  >__|   
       \/       /_____/     \/            \/          \/       
       
|__ Author: @JosueEncinar
    
    
[*] Starting the process
[*] Total plugins 87509
[*] Starting the analisys
```

## How to add a module

The tool has been uploaded without regex, for the search you need to add your regular expressions. The key to reduce false positives is here, go for it.

To know how to do this, check out modules/php/test.py and modules/js/test.py. It is not complicated.


## How to use

To use the tool, follow the instructions below:

```
git clone https://github.com/Josue87/wp_hunter.git
cd wp_hunter
pip3 install -r requirements.txt
python3 wp_hunter.py
```

The tests have been carried out with the Linux operating system

