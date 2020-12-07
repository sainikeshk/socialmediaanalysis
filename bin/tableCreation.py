#!/usr/bin/python3
# coding: utf-8
# packages
import warnings
warnings.filterwarnings("ignore")
import mysql.connector
import pandas as pd
import os
import logCreate
import logSettings
from readConfig import readValue 

logger = logCreate.getLogger(__name__,logSettings.mycomponent['logger'])

def sqlConnet(user,password,host):
	try:
		cnx = mysql.connector.connect(user=user, password=password,host=host)
		cur=cnx.cursor()
		return cur,cnx
	except Exception as e:
		logger.exception('connection error due to  %s',e)
		raise e

def tableCreation(tbcreate,database,tablename,cur,cnx):
	try:
		with open(tbcreate, "rt") as f:
			count=0
			for line in f:
				l = line.strip()
				query = l.split(';')
				query=query[0]
				if count <=1:
					query=query.replace("?",database)
				if count ==2:
					query=query.replace("?",tablename)
				try:
					cur.execute(query)
					cnx.commit()
				except Exception as e:
					logger.exception('table creation error due to %s'% e)
					pass
				count = count+1
	except Exception as e:
		logger.exception('table creation error due to %s'% e)
		raise e

def main():
	hostname = readValue('hostname',section='mysql')
	database = readValue('database',section='mysql')
	username = readValue('username',section='mysql')
	password = readValue('password',section='mysql')
	tablename = readValue('sqltablename',section='mysql')

	tbcreate = readValue('sqlconnection',section='default')

	cur,cnx = sqlConnet(username,password,hostname)
	tablecreation=tableCreation(tbcreate,database,tablename,cur,cnx)
if __name__ == "__main__":
		main()
