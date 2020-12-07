#!/usr/bin/python3
# coding: utf-8
# packages
import os
import sys
import shutil
import logCreate
import logSettings

logger = logCreate.getLogger(__name__,logSettings.mycomponent['logger'])

def cleanlog():
	try:
		path="../log"
		for filename in os.listdir(path):
			if filename.endswith('.log'):
				file=str(path)+"/"+str(filename)
				try:
					os.unlink(file)
				except:break
	except Exception as e:
		logger.exception('Alert for removing log due to %s',e)
		raise e

def cleanfolder():
	try:
		if not os.path.exists("../data/dbbackup/"):
			os.makedirs("../data/dbbackup/")

		for filename in os.listdir("../data/dbbackup/"):
			if filename.endswith('.csv'):
				file="../data/dbbackup/"+str(filename)
				try:
					os.unlink(file)
				except:break

	except Exception as e:
		logger.exception('Alert for removing files due to %s',e)
		raise e
