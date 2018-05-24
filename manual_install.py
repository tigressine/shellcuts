"""
"""
import compileall
from sys import argv as args
from pathlib import Path
import subprocess
#from tarfile import TarFile
import tarfile
import shutil
import os

VERSION_NUMBER = '1.2.1'
VERSION = 'v' + VERSION_NUMBER
paths = {
    'bin' : Path('/usr/bin'),
    'share' : Path('/usr/share'),
    #'trigger' : Path('/home/tgsachse/Dropbox/Code/Shellcuts/junk')
}

printf()



RELEASES = 'https://github.com/tgsachse/shellcuts/releases/download/{}/'.format(VERSION)

INSTALLERS = {
    'dpkg' : ('wget',
              RELEASES + 'shellcuts.deb',
              '&&',
              'dpkg',
              '-i',
              'shellcuts.deb'),
    'rpm' : ('wget',
             RELEASES + 'shellcuts-{}-1.fc27.noarch.rpm'.format(VERSION_NUMBER),
             '&&',
             'rpm',
             '-i',
             'shellcuts-{}-1.fc27.noarch.rpm'.format(VERSION_NUMBER))
}#add packmans

def check_local_install():
    """
    """
    if len(args) > 1:
        if args[1] == '--local':
            return True
        elif args[1] == '--global':
            return False
        else:
            print("Unknown arguments passed to script.")
            exit(0)
    else:
        return False

def check_paths():
    """
    """
    for key, path in paths.items():
        if not path.exists():
            return False
    else:
        return True

def check_package_managers():
    """
    """
    managers = []

    for installer in INSTALLERS.keys():
        if shutil.which(installer):
            managers.append(installer)
    
    return managers

def install_global():
    """
    """
    #check if running sudo
    managers = check_package_managers()
    print(managers)

def install_local():
    """
    """
    D_SHELLCUTS = Path('~/.shellcuts').expanduser()
    D_SHELLCUTS.mkdir(parents=True, exist_ok=True)

    os.chdir(str(D_SHELLCUTS))# dont need

    #DEST = D_SHELLCUTS.joinpath('git_temp')
    command = ('wget', 
               'https://github.com/tgsachse/shellcuts/archive/{}.tar.gz'.format(VERSION),
               )#'-P',
               #str(DEST))#check this isnt possible with a lib

    # separate function unzip tarball
    subprocess.run(command)
    tarball = D_SHELLCUTS.joinpath('{}.tar.gz'.format(VERSION))
    tar = tarfile.open(str(tarball), 'r:gz')
    tar.extractall()
    ###############################

    WD = D_SHELLCUTS.joinpath('shellcuts-{}'.format(VERSION_NUMBER))
    os.chdir(str(WD))

    
    LOCAL_TREE = (
        ('bin', 'bin/'),
        ('share', 'share/'),
        ('docs', 'docs/'),
        ('man', 'man/man1')
    )

    # make sure weve got this bitch downloaded ####
    # compile the binaries
    # move bytecode to bin
    # move share tree to share
    # move docs to docs
    # mkdir for man and move man to man
    ####### add to bash plugin and rest to update bin path
    # destroy git


def main():
    """
    """
    if check_local_install():
        install_local()
    elif check_paths():
        install_global()
    else:
        print("Filesystem unsupported. Try installing locally.")

main()
