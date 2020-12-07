#!/usr/bin/python3
# coding: utf-8
# packages
import warnings
warnings.filterwarnings("ignore")
import logging

mycomponent = {
    'logger' : {
        'stdout' : {
            'format' : "%(asctime)s %(name)s.%(funcName)s() %(levelname)s\t%(message)s",
        },
        'level' : logging.INFO,
    },
}