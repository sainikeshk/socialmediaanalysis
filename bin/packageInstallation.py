#!/usr/bin/python3
# coding: utf-8
# packages
import warnings
warnings.filterwarnings("ignore")
import subprocess
import sys
import os
import traceback
import logCreate
import logSettings
from pkg_resources import WorkingSet , DistributionNotFound
from setuptools.command.easy_install import main as install
from readConfig import readValue 

log = logCreate.getLogger(__name__,logSettings.mycomponent['logger'])

def sys_installed_packages():
    try:
        reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']) 
    except Exception as e:
        log.error("Please ensure that pip or pip3 is installed on your system and redo the setup - Alert message is"% (i))
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    return installed_packages

def sys_install_packages(installed_packages,requirements):
    packages=[]
    with open(requirements, "rt") as f:
        for line in f:
            l = line.strip()
            package = l.split(',')
            package=package[0]
            packages.append(package)

    for i in packages:
        if i in installed_packages:
            continue
            log.info("The %s package is already installed" % (i))
        if i not in installed_packages:
            working_set = WorkingSet()
            try:
                dep = working_set.require('paramiko>=1.0')
            except DistributionNotFound:
                pass

            whoami=os.getlogin()
            if whoami =='root':
                installPackage=install([i])
                log.info("Newlly installation of %s is sucessfully done"% (installPackage))
            if whoami !='root':
                try:
                    installPackage=subprocess.check_call(["pip", "install","--user", i])
                    log.info("Newlly installation of %s is sucessfully done"% (installPackage))
                except:
                    try:
                        installPackage=subprocess.check_call(["pip3", "install","--user", i])
                        log.info("Newlly installation of %s is sucessfully done"% (installPackage))
                    except Exception as e:
                        e = sys.exc_info()
                        log.error("the above error occured while installing %s package"% (e))

def main():
    requirements =readValue('requirements',section='default')
    installed_packages= sys_installed_packages()
    install_packages=sys_install_packages(installed_packages,requirements)
if __name__ == "__main__":
    main()
