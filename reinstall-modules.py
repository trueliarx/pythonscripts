# info@bnit.it
import os, sys

# target folder for the default python "Scripts" where the executables will be rebuilt
scripts_folder = 'Scripts' + os.path.sep

# file where we are going to store the current path of python
pythonpathfile = '.pythonpath'

# python stored base path. An empty string as Default
pythonstoredbasepath = ''

# Getting the current environment variable PYTHONPATH
pythonbasepath = os.getenv('PYTHONPATH') + os.path.sep

checkpythonpathfile = False

storepythonpathfile = False

deletepythonpathfile = False

pipnocache = False
pipnodeps = False
verbose = False
verbose = True
_execute = False

def printhelp():
    print('\nreinstall-modules.py\n')
    print('The script reinstalls all the installed python modules (As pip with --force-reinstall).\n')
    print('   -e    Executes the reinstallation of the modules\n')
    print('   -ps   Compares PYTHONPATH with the path inside the file PYTHONPATH\\' + pythonpathfile + '.')
    print('         If they are not matching the new path is saved and the modules are reinstalled,')
    print('         otherwise it exits with code 909090\n')
    print('   -ns   Works as -ps but does not save the path file in PYTHONPATH\\' + pythonpathfile + '\n')
    print('   -d    Deletes the PYTHONPATH\\' + pythonpathfile + ' file with the stored path and Exits\n')
    print('   -nc   reinstall the modules without cache (Use with -e or -ps or -ns).')
    print('         Modules will be re-downloaded and the pip\'s cache ignored.\n')
    print('   -nd   For each module do not reinstall the dependencies (Use with -e or -ps or -ns).\n')
    print('   -v    Verbose\n')
    print('   -h    Shows this help')
    exit()
# end of printhelp()

for arg in sys.argv:
    if arg == '-e': # verbose
        _execute = True
    elif arg == '-ps': # verify the existance of the pythonpathfile
        checkpythonpathfile = True
        storepythonpathfile = True
        _execute = True
    elif arg == '-ns': # skip the storage of the python path
        checkpythonpathfile = True
        _execute = True
    elif arg == '-d': # delete the file with the stored path and exit
        deletepythonpathfile = True
        _execute = True
    elif arg == '-nc': # verbose
        pipnocache = True
    elif arg == '-nd': # verbose
        pipnodeps = True
    elif arg == '-v': # verbose
        verbose = True
    elif arg == '-h': # help
        printhelp()
# end of arguments


if not _execute: printhelp()


# python path is needed
if not os.path.isdir(pythonbasepath) :
    print('The folder specified in "PYTHONPATH" does not exists!\nSet the correct Path before executing the script\n\nCurrent PYTHONPATH: ' + pythonbasepath )
    exit(1)



# if we have to delete the python path file - and exit
if deletepythonpathfile == True and os.path.exists(pythonbasepath + pythonpathfile):
    try:
        os.remove(pythonbasepath + pythonpathfile)
        print('Python path file correctly removed')
        if verbose: print('File: ' + pythonbasepath + pythonpathfile)
        exit()
    except Exception as errinfo:
        print( 'Error (' + str(errinfo.args[0]) + '): ' + errinfo.args[1] )
        print('Cannot delete the file: ' + pythonbasepath + pythonpathfile)
        exit(errinfo.args[0])


# if we need to check/read the stored path file
if checkpythonpathfile == True and os.path.exists(pythonbasepath + pythonpathfile):

    try:
        with open(pythonbasepath + pythonpathfile) as f:
            # reading the stored base path of python stripping carriage returns and line feeds
            pythonstoredbasepath = f.readline().rstrip("\r\n")
            f.close()
            if verbose: print( 'Stored Path ' + pythonstoredbasepath + '\nreaded from ' + pythonbasepath + pythonpathfile + '\n')
    except Exception as errinfo:
        print('Error (' + str(errinfo.args[0]) + '): ' + errinfo.args[1])
        print('Cannot read the file: ' + pythonbasepath + pythonpathfile)
        # exiting with the specific error number
        exit(errinfo.args[0])
# end of if checkpythonpathfile == True 



if checkpythonpathfile == True:
    # if the PYTHONPATH and the stored python path are matching
    if pythonbasepath == pythonstoredbasepath:
        if verbose: print('PYTHONPATH and the stored Python path are matching. Ok - Exiting with code 909090.')
        # exiting with a 909090 error code
        exit(909090)

    elif storepythonpathfile == True:
        try:
            # generating the pythonpathfile if missing or if the storedpath and PYTHONPATH are not matching
            # we store the pythonpathfile in python's folder so that the script can be run from any location
            with open( pythonbasepath + pythonpathfile, "w") as f:
                f.write(pythonbasepath)
                f.close()
                if verbose: print ("PYTHONPATH saved in " + pythonbasepath + pythonpathfile + '\n')
        except Exception as errinfo:
            print( 'Error (' + str(errinfo.args[0]) + '): ' + errinfo.args[1] )
            print('Cannot write the file: ' + pythonbasepath + pythonpathfile)
            # exiting with the specific error number
            exit(errinfo.args[0])
    # end of if checkpythonpathfile == True:


#
# importing pip after overriding the function fix_script

# this part is like running PIP from command line.
# importing the main of the PIP module
from pip._internal.cli.main import main as pip_entry_point

# importing the distlib database to get the modules
from pip._vendor.distlib.database import DistributionPath
# importing from the distlib util to parse the modules names
from pip._vendor.distlib.util import parse_name_and_version

from pip._vendor.distlib.scripts import ScriptMaker


# setting the base arguments for pip.
pipargs = ["install", "--force-reinstall"]

# No deps will not reinstall dependencies
if pipnodeps: pipargs += ["--no-deps"]
# No cache will not use the local cache and will download the modules
if pipnocache: pipargs += ["--no-cache-dir"]

# getting all the installed modules
my_distributions = DistributionPath()

for dist in my_distributions.get_distributions():
    if not hasattr(dist, 'provides'):
        print('No "provides": %s', dist)
        pass
    else:
        provided = dist.provides
        for p in provided:
            p_name, p_ver = parse_name_and_version(p)
            # adding the modules' names as argument for pip
            pipargs += [p_name]
# test only pip
#pipargs += ["pip"]


if verbose: print('Modules have been reinstalled')

# using the PIP module like the command line and returning the respective error code on exit
exit( pip_entry_point(pipargs) )
