import warnings
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import re
import pickle
import lightgbm
import nltk
import os
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report
from sklearn.feature_extraction import text 

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords

from gensim import corpora
from gensim.utils import simple_preprocess

import logCreate
import logSettings
import mysql.connector
import pymysql

from readConfig import readValue

changeDir=os.chdir(os.path.dirname(os.path.abspath(__file__)))

def sqlConnet(database,user,password,host,logger):
    logger.info("******************connected to mysql******************")
    cnx = mysql.connector.connect(user=user, password=password,host=host,database=database,autocommit=True)
    cur=cnx.cursor()
    return cur,cnx

def add_features(logger,cur,cnx,databasename,sqltable,hostname,dbusername,dbpassword):
	logger.info('******************Get the data from playstore and applestore***********************')
	usedb="USE %s "% (databasename)
	cur.execute(usedb)
	fsql="select * from "+sqltable+" where (UserRating =1 or UserRating=2);"
	cur.execute(fsql)
	column_names = [i[0] for i in cur.description]
	df=pd.DataFrame(cur.fetchall())
	df.columns=column_names
	logger.info("****************Required data fetched from database and stored in dataframe*********************")
	data_master=df[['UniqueID','ReviewTitle','Review']]
	def stemSentence(sentence):
	    token_words=word_tokenize(sentence)
	    token_words
	    stem_sentence=[]
	    for word in token_words:
	        stem_sentence.append(porter.stem(word))
	        stem_sentence.append(" ")
	    return "".join(stem_sentence)

	porter = PorterStemmer()
	lancaster=LancasterStemmer()
	w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
	lemmatizer = nltk.stem.WordNetLemmatizer()
	def preprocessData(dframe):
	    df=dframe
	    df1=df[['UniqueID','ReviewTitle','Review']]
	    df1.ReviewTitle=df1.ReviewTitle.apply(lambda x : str(x).replace('NULL','')).fillna('')
	    df1.Review=df1.Review.fillna('')
	    for col in ['ReviewTitle','Review']:
	        df1[col]=df1[col].apply(lambda x : (re.findall(r'[a-zA-Z]+',(str(x)).lower())))
	    df1['txt']=df1['ReviewTitle'].apply(lambda x: str(x))+" "+df1['Review'].apply(lambda x: str(x))
	    df1['txt']=df1['txt'].apply(lambda x: stemSentence(str(x))).apply(lambda x: str(x)).apply(lambda x: re.sub(r'[^a-zA-Z]+',' ',x))
	    return(df1)
	master_data=preprocessData(data_master)
	lst=['from','other','others', 'subject', 'android', 'device', 're', 'edu', 'ocbc', 'citi', 'dbs', 'citibank', 'bank', 'mobile',
     'apple', 'ios', 'playstore', 'play', 'store', 'app', 'apps', 'application', 'please', 'banking','ocbc','metro','monzo',
     'adbc', 'abu', 'dhabi', 'cbd', 'hsbc', 'bochk', 'mashreq', 'barclays', 'singapore', 'uk', 'uae', 'sg', 'hk', 'ocbc']
	stop_words = text.ENGLISH_STOP_WORDS.union(lst)
	X=master_data['txt'].values
	cv = pickle.load(open('../data/Neg_Feature_CountVectorizer.pickle','rb'))
	rf = pickle.load(open('../data/Neg_Feature_RandomForest.pickle','rb'))
	lgbc = pickle.load(open('../data/Neg_Feature_LGBMClassifier.pickle','rb'))
	X_cv = cv.transform(X)
	y_rf=rf.predict(X_cv)
	y_lgbc=lgbc.predict(X_cv.todense())
	data_master['TopicCategory']=pd.Series(y_lgbc).apply(lambda x : x.split("|")[0])
	data_master['Topic']=pd.Series(y_lgbc).apply(lambda x : x.split("|")[1])
	data_master['SubTopic']=pd.Series(y_lgbc).apply(lambda x : x.split("|")[2])
	# print(data_master.columns)
	print("ratings_12_predict upload")
	feat_upd="update %s set TopicCategory= '%s',Topic='%s',SubTopic='%s' where UniqueID='%s';"
	for i in data_master.index:
		try:
			cur.execute(feat_upd%(sqltable,data_master.iloc[i,3],data_master.iloc[i,4],data_master.iloc[i,5],data_master.iloc[i,0]))
		except:continue
def main():
	logger =logCreate.getLogger(__name__,logSettings.mycomponent['logger']) 
	hostname = readValue('hostname',section='mysql')
	database = readValue('database',section='mysql')
	username = readValue('username',section='mysql')
	password = readValue('password',section='mysql')
	tablename = readValue('sqltablename',section='mysql')    
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
	predict=add_features(logger,cur,cnx,database,tablename,hostname,username,password)
if __name__ == "__main__":
        main()
