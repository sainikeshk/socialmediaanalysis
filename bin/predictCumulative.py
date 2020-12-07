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

def sqlConnet(database,user,password,host):
	cnx = mysql.connector.connect(user=user, password=password,host=host,database=database,autocommit=True)
	cur=cnx.cursor()
	return cur,cnx

def tableCreation(tbcreate,database,tablename,cur,cnx):
	with open(tbcreate, "rt") as f:
		count=0
		for line in f:
			print("updating table with 7 days cumulative")
			l = line.strip()
			query = l.split(';')
			query=query[0]
			if count ==0:
				query=query.replace("?",database)
			if count >=1:
				query=query.replace("?",tablename)
			try:
				cur.execute(query)
				cnx.commit()
				print(query)
			except Exception as e:
				logger.exception('table creation error due to %s'% e)
				pass

			count = count+1

def main():
	hostname = readValue('hostname',section='mysql')
	database = readValue('database',section='mysql')
	username = readValue('username',section='mysql')
	password = readValue('password',section='mysql')
	tablename = readValue('sqltablename',section='mysql')

	tbcreate = readValue('cumulativetable',section='default')
	cur,cnx = sqlConnet(database,username,password,hostname)
	tablecreation=tableCreation(tbcreate,database,tablename,cur,cnx)
if __name__ == "__main__":
		main()