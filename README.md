# pythonscripts
Basic Python scripts

A few days ago I started to write in python from scratch.
I've  done those python scripts just for my personal (basic) needs and to learn something new.

reinstall-modules.py
--

Reinstalls all the currently installed python modules.
I started to do it just to fix an error on windows after changing the python's folder since "pip" adds the full path to the executables (.exe) generated in "\Scripts".

( For ex. - Fatal error in launcher: Unable to create process using x:\xyz\python.exe )

With this script you can reinstall all of them without using the (non working?) pip executable (the module must be available).

You can achieve the same results (with the -e parameter) with those commands if you don't like to use the script

`python -m pip freeze --local >modules.txt`

`python -m pip install --force-reinstall -r modules.txt`


With other parameters the script could check if the current PYTHONPATH has changed and then launchs reinstalls the modules.
It's quite useful, on Windows, when the scripts (converted in exe files) are not working anymore due to the different path of python.


*This is my first, ever, script done in python.*




**The scripts should not be used in production**
