#!/usr/bin/python3
# coding: utf-8
# packages
import warnings
warnings.filterwarnings("ignore")
import os, sys, stat
import packageInstallation
pkginstall=packageInstallation.main()
import logCreate
import logSettings
from readConfig import readValue 
from writeConfig import changeinputs
import housekeeping
import backupfiles
import tableCreation
import load_data
import analysisRunall
import cronJobSetup

log = logCreate.getLogger(__name__,logSettings.mycomponent['logger'])

def applicationInfo(database):
	writeConf=input ("Do you want to change mysql credentials in applicationInfo ?:")
	appInf=writeConf.upper()
	if appInf == 'YES' or appInf == 'Y':
		appInfo=changeinputs()

	else:		
		print("Continueing with existing mysql server connection credentials")
		log.info("Continueing with existing mysql server connection credentials")

		cleanpkg=cleanpackage()
		createtb=tableCreation.main()
		ld=load(database)
		bkup=backupdp(database)
		analysis=appstore()
		cronsetup=cronsettings()

		
		
def cleanpackage():
	deletefiles=input ("Do you want to delete all existing files except backup data ?:")
	deletefile=deletefiles.upper()
	if deletefile == 'YES' or deletefile == 'Y':
		housekeep=housekeeping.main()
		print("Existing files deleted sucessfully")
		log.info("Existing files deleted sucessfully")
	else:		
		print("Not making any changes for existing files")
		log.info("Not making any changes for existing files")


def backupdp(database):
	bkup=input ("Do you want to take a backup of existing %s database ?:"% database)
	backupdb=bkup.upper()
	if backupdb == 'YES' or backupdb == 'Y':
		bkupdb=backupdata.main()
		print("Database backup taken sucessfully")
		log.info("Database backup taken sucessfully")
	else:		
		print("Not taking backup of",database,"database")
		log.info("Not taking backup of %s database",database)

def load(database):
	ld=input ("Do you want to load existing csv to %s database ?:"% database)
	load_csv=ld.upper()
	if load_csv == 'YES' or load_csv == 'Y':
		load_csv=load_data.main()
		print("CSV Loaded sucessfully")
		log.info("CSV Loaded sucessfully")
	else:		
		print("Not loading csv to database")
		log.info("Not loading csv to database")

def appstore():
	hisCreate=input("Do you want to do analysis for appreviews ?:")
	histload=hisCreate.upper()
	if histload == 'YES' or histload == 'Y':
		histload=analysisRunall.main()
		print("analysis data updated to database sucessfully")
		log.info("analysis data updated to database sucessfully")
	else:		
		print("analysis data are not inserted")
		log.info("analysis data are not inserted")


def cronsettings():
	cron=input ("Do you want to schedule the socialmedia script now?:")
	cronSet=cron.upper()
	if cronSet == 'YES' or cronSet == 'Y':
		cronSetup=cronJobSetup.main()
		print("socialmedia scripts scheduled sucessfully")
		log.info("socialmedia scripts scheduled sucessfully")
	else:		
		print("socialmedia scripts are not scheduled")
		log.info("socialmedia scripts are not scheduled")
	
def main():
	database = readValue('database',section='mysql')	
	appInfo=applicationInfo(database)
	
if __name__ == "__main__":
		main()
