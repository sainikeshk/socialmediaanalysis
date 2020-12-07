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
import logCreate
import logSettings
import mysql.connector
from readConfig import readValue
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report,f1_score
from sklearn.feature_extraction import text 
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords

from gensim import corpora
from gensim.utils import simple_preprocess
from simpletransformers.classification import ClassificationModel

changeDir=os.chdir(os.path.dirname(os.path.abspath(__file__)))
def sqlConnet(database,user,password,host,logger):
	logger.info("******************connected to mysql******************")
	cnx = mysql.connector.connect(user=user, password=password,host=host,database=database,autocommit=True)
	cur=cnx.cursor()
	return cur,cnx

def predict_data(logger,df_new_feat,cur,cnx,databasename,sqltable,hostname,dbusername,dbpassword):
	logger.info('******************predict_using_bert execution is started***********************')
	usedb="USE %s "% (databasename)
	cur.execute(usedb)
	fsql="select * from "+sqltable+" where Topic is NULL or SubTopic is NULL;"
	cur.execute(fsql)
	column_names = [i[0] for i in cur.description]
	df_valid=pd.DataFrame(cur.fetchall())
	df_valid.columns=column_names

	def stemSentence(sentence):
	    token_words=word_tokenize(sentence)
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
		df1=df[['ReviewTitle','Review','Topic','SubTopic']]
		df1.ReviewTitle=df1.ReviewTitle.apply(lambda x : str(x).replace('NULL','')).fillna('')
		df1.Review=df1.Review.fillna('')
		for col in ['ReviewTitle','Review']:
		    df1[col]=df1[col].apply(lambda x : (re.findall(r'[a-zA-Z]+',(str(x)).lower())))
		df1['txt']=df1['ReviewTitle'].apply(lambda x: str(x))+" "+df1['Review'].apply(lambda x: str(x))
		df1['txt']=df1['txt'].apply(lambda x: stemSentence(x)).apply(lambda x: str(x)).apply(lambda x: re.sub(r'[^a-zA-Z]+',' ',x))
		return(df1)
	valid_data=preprocessData(df_valid)
	lst=['from','other','others', 'subject', 'android', 'device', 're', 'edu', 'ocbc', 'citi', 'dbs', 'citibank', 'bank', 'mobile',
     'apple', 'ios', 'playstore', 'play', 'store', 'app', 'apps', 'application', 'please', 'banking','ocbc','metro','monzo',
     'adbc', 'abu', 'dhabi', 'cbd', 'hsbc', 'bochk', 'mashreq', 'barclays', 'singapore', 'uk', 'uae', 'sg', 'hk', 'ocbc','nan']
	stop_words = text.ENGLISH_STOP_WORDS.union(lst)
	
	model=pickle.load(open('../data/Bert_model.pickle','rb'))
	feat_dct=pickle.load(open('../data/feat_dct.pickle','rb'))
	X_valid=valid_data['txt'].values
	predictions, raw_outputs=pd.Series(model.predict(X_valid))
	test_class = predictions.tolist()
	df_valid['Feature']=[feat_dct[i] for i in test_class]
	df_valid['Topic']=df_valid.Feature.apply(lambda x : x.split("|")[0])
	df_valid['SubTopic']=df_valid.Feature.apply(lambda x : x.split("|")[1])
	df_valid.drop(['TopicCategory', 'Feature'], axis=1, inplace=True)
	data_master=df_valid.merge(df_new_feat,on=['Topic', 'SubTopic'])
	#df_maste=df_maste.rename(columns={'TopicCategory':'TopicCategory(L1)','Topic':'Topic(L2)','SubTopic':'SubTopic(L3)'})
	data_master=data_master[['UniqueID','DateTime','UserRating','ReviewTitle','Review','TopicCategory','Topic','SubTopic']]
	add_columns="alter table "+sqltable+" add columns TopicCategory int not null,Topic int not null,SubTopic int not null;"
	#try:
		#cur.execute(add_columns)
	#except:pass
	feat_upd="update %s set TopicCategory= '%s',Topic='%s',SubTopic='%s' where UniqueID='%s';"
	for i in data_master.index:
		try:
			cur.execute(feat_upd%(sqltable,data_master.iloc[i,-3],data_master.iloc[i,-2],data_master.iloc[i,-1],data_master.iloc[i,0]))
		except:continue

def main():    
	logger =logCreate.getLogger(__name__,logSettings.mycomponent['logger']) 
	hostname = readValue('hostname',section='mysql')
	database = readValue('database',section='mysql')
	username = readValue('username',section='mysql')
	password = readValue('password',section='mysql')
	tablename = readValue('sqltablename',section='mysql')    
	cur,cnx = sqlConnet(database,username,password,hostname,logger)
	logger =logCreate.getLogger(__name__,logSettings.mycomponent['logger']) 
	df_new_feat=pd.read_excel('../data/FeatureLevelsFinal.xlsx')
	predict=predict_data(logger,df_new_feat,cur,cnx,database,tablename,hostname,username,password)

if __name__ == "__main__":
        main()