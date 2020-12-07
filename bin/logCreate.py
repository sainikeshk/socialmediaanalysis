#!/usr/bin/python3
# coding: utf-8
# packages
import warnings
warnings.filterwarnings("ignore")
import logging.handlers
import sys
import os
import logSettings
import logging
import datetime as dt

def getStreamHandler(logger,name, config, stream):
    if not os.path.exists('../log'):
        os.makedirs('../log')
    datetString = str(dt.datetime.now()).replace('-','').replace(':', '').split('.')[0].replace(' ', '.' )
    formatter = logging.Formatter(config['format'])
    fl=logging.handlers.TimedRotatingFileHandler(filename='../log/'+str(datetString)+'.socialmedia.appstore.log',when="d",interval=7)
    fl.setFormatter(formatter)
    if 'level' in config:
        fl.setLevel(config['level'])
    return fl

def getLogger(name, config):
    logger = logging.getLogger(name)
    logger.addHandler(
            getStreamHandler(logger,name, config['stdout'], sys.stdout))
    logger.setLevel(config['level'])
    logger.isEnabledFor(config['level'])
    return logger

def isDebugEnabled():
    if(config['level']==True):
        return True
    else:
        return False