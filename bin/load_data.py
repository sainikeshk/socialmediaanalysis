#!/usr/bin/python3
# coding: utf-8
# packages
import warnings
warnings.filterwarnings("ignore")
import logCreate
import logSettings
import mysql.connector
import pymysql
import pickle
import datetime
import time
import operator
#import predict_model
import os
import numpy as np
import pandas as pd
import json
import platform
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR
from sqlalchemy.types import String,DateTime
from pprint import pprint
from readConfig import readValue


changeDir=os.chdir(os.path.dirname(os.path.abspath(__file__)))

def sqlConnet(database,user,password,host,logger):
    logger.info("******************connected to mysql******************")
    cnx = mysql.connector.connect(user=user, password=password,host=host,database=database,autocommit=True)
    cur=cnx.cursor()
    return cur,cnx
def df_to_mysql(table_name,cur,cnx,dbname,dbusername,dbpassword,hostname,logger,df):
	engine = create_engine("mysql+pymysql://{}:{}@{}/{}".format(dbusername,dbpassword,hostname,dbname),encoding='utf8',convert_unicode=True)
	num_rows = len(df)
	#Iterate one row at a time
	for i in range(num_rows):
		try:
			df.iloc[i:i+1].to_sql(name=table_name,con = engine,if_exists ='append',index=False)
		except:pass
	logger.info('****inserted table****')

def main():
	logger =logCreate.getLogger(__name__,logSettings.mycomponent['logger']) 
	hostname = readValue('hostname',section='mysql')
	database = readValue('database',section='mysql')
	username = readValue('username',section='mysql')
	password = readValue('password',section='mysql')
	tablename = readValue('sqltablename',section='mysql')    
	cur,cnx = sqlConnet(database,username,password,hostname,logger)

	df=pd.read_excel('../data/dbbackup/appreviewsAnalysis.xlsx')

	query='select count(*) from %s.%s;'%(database,tablename)
	
	cur=cnx.cursor()
	cur.execute(query)
	n=cur.fetchone()
	db_cnt=n[0]
	csv_cnt=df.shape[0]
	if db_cnt<csv_cnt:
		print("loading csv data to database")
		df_to_mysql(tablename,cur,cnx,database,username,password,hostname,logger,df)
	else:
	    print('already database has more records than csv')
if __name__ == "__main__":
        main()