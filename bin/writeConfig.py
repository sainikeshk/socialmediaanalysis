#!/usr/bin/python3
# coding: utf-8
# packages
import warnings
warnings.filterwarnings("ignore")
import configparser
import logCreate
import logSettings
import pymysql
from readConfig import readValue 
import sys

log = logCreate.getLogger(__name__,logSettings.mycomponent['logger'])

config = configparser.ConfigParser()
config.read('../etc/application.ini')

def db_connet(newdbname,newuser,newpassword,newhost):
	try:
		cnx = pymysql.connect(user=user, password=password,host=host,database=database)
		cur=cnx.cursor()
		return cur,cnx
	except :
		print("updating the new username,password,host and database to application file")
		print("Please logout and execute setup.py again...")
		pass

def changeinputs():
	try:
		newuser=input("Please enter MYSQL username:")
		newpassword=input ("Please enter MYSQL password:")
		newdbname=input ("Please enter MYSQL database name:")
		newhost=input ("Please enter MYSQL host name:")

		config['mysql']['username'] = newuser 
		config['mysql']['password'] = newpassword 
		config['mysql']['database'] = newdbname
		config['mysql']['hostname'] = newhost     


		with open('../etc/application.ini', 'w') as configfile:
			config.write(configfile)

		print("Mysql server connection credentials are changed sucessfully")
		print("logging out setup.py and please execute setup.py again...No need to change applicationInfo (click 'no') second time execution")
		sys.exit("logging out setup.py and please execute setup.py again...No need to change applicationInfo (click 'no') second time execution")

	except:
		pass
			
