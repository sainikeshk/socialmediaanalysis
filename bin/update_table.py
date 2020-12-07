import warnings
warnings.filterwarnings('ignore')

from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR
from sqlalchemy.types import String
import pymysql

import os
import logCreate
import logSettings
import mysql.connector
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from readConfig import readValue
from datetime import timedelta
import threading

changeDir=os.chdir(os.path.dirname(os.path.abspath(__file__)))
def sqlConnet(database,user,password,host,logger):
	logger.info("******************connected to mysql******************")
	cnx = mysql.connector.connect(user=user, password=password,host=host,database=database,autocommit=True)
	cur=cnx.cursor()
	return cur,cnx
def update_table(logger,cur,cnx,databasename,sqltable,hostname,dbusername,dbpassword):
	logger.info('******************update_table execution is started***********************')
	usedb="USE %s "% (databasename)
	cur.execute(usedb)
	fsql="select * from "+sqltable+";"
	#fsql="select * from "+sqltable+" where Cumulative7Days is NULL OR Cumulative7DaysPos is NULL OR Cumulative7DaysNeu is NULL OR Cumulative7DaysNeg is NULL;"
	cur.execute(fsql)
	column_names = [i[0] for i in cur.description]
	df=pd.DataFrame(cur.fetchall())
	df.columns=column_names
	df=df.sort_values(['ApplicationName','Region','Source','VersionNo','DateTime'],ascending=True).reset_index(drop=True)
	def create_col(df):
	    for i in range(len(df)):
	        df.iloc[i,-8]=len(df[(df.DateTime>=df.iloc[i,1]+timedelta(days=-7))&
	                                   (df.DateTime<df.iloc[i,1])])
	        df.iloc[i,-7]=len(df[(df.DateTime>=df.iloc[i,1]+timedelta(days=-7))&
	                                   (df.DateTime<df.iloc[i,1])&
	                                   (df.ScoreCom>0.2)])
	        df.iloc[i,-5]=len(df[(df.DateTime>=df.iloc[i,1]+timedelta(days=-7))&
	                                   (df.DateTime<df.iloc[i,1])&
	                                   (df.ScoreCom<=0.2)&
	                                   (df.ScoreCom>=-0.2)])
	        df.iloc[i,-6]=len(df[(df.DateTime>=df.iloc[i,1]+timedelta(days=-7))&
	                                   (df.DateTime<df.iloc[i,1])&
	                                   (df.ScoreCom<-0.2)])
	        
	    #print(i+1,str(time.time()-tic))
	    return df
	df_final=pd.DataFrame()
	tic=time.time()
	df_apple=df[df['Source']=='Applestore']
	apple_appname=df_apple.ApplicationName.unique().tolist()
	apple_region=df_apple.Region.unique().tolist()
	apple_version=df_apple.VersionNo.unique().tolist()
	df_play=df[df['Source']=='Playstore']
	play_appname=df_play.ApplicationName.unique().tolist()
	play_region=df_play.Region.unique().tolist()
	play_version=df_play.VersionNo.unique().tolist()
	for source in ['apple','play']:
	    for reg in vars()[source+'_region']:
	        for app in vars()[source+'_appname']:
	            for ver in vars()[source+'_version']:
	                sub=vars()['df_'+source][((vars()['df_'+source].Region==str(reg)) & (vars()['df_'+source].ApplicationName==str(app)) & (vars()['df_'+source].VersionNo==str(ver)))]
	                if sub.empty==True:
	                    continue
	                else:
	                    dft=create_col(sub)
	                    df_final=pd.concat([df_final,dft]) 
	print(str(time.time()-tic))
	print(df_final[['Cumulative7Days','Cumulative7DaysPos','Cumulative7DaysNeu','Cumulative7DaysNeg']].head())
	start=time.time()
	#rows_lst=[list(df_final.iloc[i,:]) for i in range(len(df_final))]  
	rows_lst=[(int(df_final.iloc[i,-8]),int(df_final.iloc[i,-7]),int(df_final.iloc[i,-5]),int(df_final.iloc[i,-6]),str(df_final.iloc[i,0])) for i in range(len(df_final))]
	print(df_final.shape)
	processes = []
	#query="""UPDATE %s SET Cumulative7Days=%s,Cumulative7DaysPos=%s,Cumulative7DaysNeu=%s,Cumulative7DaysNeg=%s WHERE UniqueID='%s';"""    
	temp=df_final[['UniqueID','Cumulative7Days','Cumulative7DaysPos','Cumulative7DaysNeg','Cumulative7DaysNeu']]
	engine = create_engine("mysql+pymysql://%s:%s@%s/%s"%(dbusername,dbpassword,hostname,databasename),encoding='utf8',convert_unicode=True)
	temp.to_sql('appreviewstemp',engine,index=False,if_exists='replace')
	#print('temp table created')
	query = """UPDATE %s.%s AS f,%s.appreviewstemp AS t
		    SET f.Cumulative7Days = t.Cumulative7Days,
		    f.Cumulative7DaysPos = t.Cumulative7DaysPos,
		    f.Cumulative7DaysNeu = t.Cumulative7DaysNeu,
		    f.Cumulative7DaysNeg = t.Cumulative7DaysNeg
		     WHERE f.UniqueID = t.UniqueID;"""%(databasename,sqltable,databasename)
	print(query)
	cur.execute(query)
	print(cur.rowcount)
	cur.execute("DROP TABLE %s.appreviewtemp;"%(databasename))
	print(f'Time taken: {time.time() - start}')
def main():    
	logger =logCreate.getLogger(__name__,logSettings.mycomponent['logger']) 
	hostname = readValue('hostname',section='mysql')
	database = readValue('database',section='mysql')
	username = readValue('username',section='mysql')
	password = readValue('password',section='mysql')
	tablename = readValue('sqltablename',section='mysql')    
	cur,cnx = sqlConnet(database,username,password,hostname,logger)
	logger =logCreate.getLogger(__name__,logSettings.mycomponent['logger'])
	updat=update_table(logger,cur,cnx,database,tablename,hostname,username,password)

if __name__ == "__main__":
    	main()


