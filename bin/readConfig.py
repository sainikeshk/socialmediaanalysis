#!/usr/bin/python3
# coding: utf-8
# packages
import warnings
warnings.filterwarnings("ignore")
import configparser
import logCreate
import logSettings

log = logCreate.getLogger(__name__,logSettings.mycomponent['logger'])

config = configparser.ConfigParser()
config.read('../etc/application.ini')
   
def readValue(option,section='default'):
    try:
        log.info("In the section %s the option %s is exists"%(section,option))
        return config.get(section, option)
    except:
        log.error("Exception::%s is not configured under %s" % (option , section))
        return None