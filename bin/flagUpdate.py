#!/usr/bin/python3
# coding: utf-8
# packages
import warnings
warnings.filterwarnings('ignore')
import os
changeDir=os.chdir(os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
import logCreate
import logSettings
import mysql.connector
import pymysql

from readConfig import readValue



def sqlConnet(database,user,password,host,logger):
    cnx = mysql.connector.connect(user=user, password=password,host=host,database=database,autocommit=True)
    cur=cnx.cursor()
    return cur,cnx

def flagupdate(cur,cnx,databasename,sqltable,flagdata):
	usedb="USE %s "% (databasename)
	cur.execute(usedb)
	fsql="select * from "+str(sqltable)
	cur.execute(fsql)
	column_names = [i[0] for i in cur.description]
	df=pd.DataFrame(cur.fetchall())
	df.columns=column_names
	data_master=df[['UniqueID','TopicCategory','Topic','SubTopic']]
	for j in range(0,len(flagdata)):
		for i in range(0,len(data_master)):
			if flagdata['Topic'][j] == data_master['Topic'][i]:
				UniqueID=data_master['UniqueID'][i]
				flag=flagdata['Flag'][j]
				feat_upd="update %s set Flag= '%s' where UniqueID='%s';"%(sqltable,flag,UniqueID)
				print(feat_upd)
				# try:
				cur.execute(feat_upd)
				# except:continue	

def main():
	logger =logCreate.getLogger(__name__,logSettings.mycomponent['logger']) 
	hostname = readValue('hostname',section='mysql')
	database = readValue('database',section='mysql')
	username = readValue('username',section='mysql')
	password = readValue('password',section='mysql')
	tablename = readValue('sqltablename',section='mysql')

	flagdata=pd.read_excel("../data/FeatureLevelsFinal.xlsx") 

	cur,cnx = sqlConnet(database,username,password,hostname,logger)
	safe_update1="set sql_safe_updates = 0;"
	safe_update2="set sql_safe_updates = 1;"
	try:
	    cur.execute(safe_update1)
	    sql1="ALTER TABLE {}.{} ADD Topic varchar(70);".format(database,tablename)
	    cur.execute(sql1)
	    cur.execute(safe_update1)
	    sql2="ALTER TABLE {}.{} ADD SubTopic varchar(70);".format(database,tablename)
	    cur.execute(sql2)
	    cur.execute(safe_update1)
	except:pass
	predict=flagupdate(cur,cnx,database,tablename,flagdata)
if __name__ == "__main__":
        main()