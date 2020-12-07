#!/usr/bin/python3
# coding: utf-8
# packages
import warnings
warnings.filterwarnings("ignore")
import pymysql
import pandas as pd
import os
import logCreate
import logSettings
from datetime import datetime
from readConfig import readValue 

logger = logCreate.getLogger(__name__,logSettings.mycomponent['logger'])

def sqlconnet(database,user,password,host):
	try:
		cnx = pymysql.connect(user=user, password=password,host=host,database=database)
		cur=cnx.cursor()
		return cur,cnx
	except Exception as e:
		raise e
	
def histodataFetch(cur,cnx,dbBackup,tablename):
	fetchdata="select * from %s;"% (tablename)
	# fetchdata="select * from appreviews.socialmedia where Region = 'uae' and DateTime >= '2020-01-01 00:00:00';"
	df=pd.read_sql(fetchdata , cnx)

	filename="appreviewsAnalysis.csv"
	print(filename)
	df.to_csv(str(dbBackup)+'/'+str(filename), index=False)
		
	
def main():
	hostname = readValue('hostname',section='mysql')
	database = readValue('database',section='mysql')
	username = readValue('username',section='mysql')
	password = readValue('password',section='mysql')
	tablename = readValue('sqltablename',section='mysql')

	dbBackup = readValue('backupfromdb',section='default')
	
	cur,cnx = sqlconnet(database,username,password,hostname) 
	fetchdata=histodataFetch(cur,cnx,dbBackup,tablename)
	
if __name__ == "__main__":
		main()	
