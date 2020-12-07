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
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report
from sklearn.feature_extraction import text 
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords

from gensim import corpora
from gensim.utils import simple_preprocess

changeDir=os.chdir(os.path.dirname(os.path.abspath(__file__)))
def train_data(logger,data_master):
	logger.info('******************train model for ratings 3 is started***********************')
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
	    df1=df[['ReviewTitle','Review','TopicCategory','Topic','SubTopic']]
	    df1.ReviewTitle=df1.ReviewTitle.apply(lambda x : str(x).replace('NULL','')).fillna('')
	    df1.Review=df1.Review.fillna('')
	    for col in ['ReviewTitle','Review']:
	        df1[col]=df1[col].apply(lambda x : (re.findall(r'[a-zA-Z]+',(str(x)).lower())))
	    df1['txt']=df1['ReviewTitle'].apply(lambda x: str(x))+" "+df1['Review'].apply(lambda x: str(x))
	    df1['txt']=df1['txt'].apply(lambda x: stemSentence(x)).apply(lambda x: str(x)).apply(lambda x: re.sub(r'[^a-zA-Z]+',' ',x))
	    return(df1)

	master_data=preprocessData(data_master)

	lst=['from','other','others', 'subject', 'android', 'device', 're', 'edu', 'ocbc', 'citi', 'dbs', 'citibank', 'bank', 'mobile','apple', 'ios', 'playstore', 'play', 'store', 'app', 'apps', 'application', 'please', 'banking','ocbc','metro','monzo','adbc', 'abu', 'dhabi', 'cbd', 'hsbc', 'bochk', 'mashreq', 'barclays', 'singapore', 'uk', 'uae', 'sg', 'hk', 'ocbc']
	stop_words = text.ENGLISH_STOP_WORDS.union(lst)

	master_data['Feature']=master_data['TopicCategory']+"|"+master_data['Topic']+"|"+master_data['SubTopic']

	labels=master_data['Feature'].unique().tolist()
	n=master_data['Feature'].value_counts().max()
	df_mas=pd.DataFrame(columns=list(master_data.columns))
	for label in labels:
	    vars()['df_'+str(label)]=master_data[master_data.Feature==str(label)]
	    if vars()['df_'+str(label)].shape[0]!=n:
	        vars()['df_'+str(label)]=resample(vars()['df_'+str(label)],replace = True,n_samples = n,random_state = 42)
	    df_mas=pd.concat([df_mas,vars()['df_'+str(label)]])
	# print(df_mas.shape,master_data.shape)

	X=df_mas['txt'].values
	y=df_mas['Feature'].values

	cv = CountVectorizer(strip_accents='ascii',lowercase=True,stop_words=stop_words)
	X_cv = cv.fit_transform(X)
	pickle.dump(cv,open('../data/Rating3_Feature_CountVectorizer.pickle','wb+'))

	X_train,X_test,y_train,y_test=train_test_split(X_cv,y,test_size=0.25,random_state=42)

	rf=RandomForestClassifier(random_state=18)
	rf.fit(X_train,y_train)
	pickle.dump(rf,open('../data/Rating3_Feature_RandomForest.pickle','wb+'))
	print("ratings_3_train execution started")
	print("RandomForestClassifier Train Accuracy",rf.score(X_train,y_train))
	print("RandomForestClassifier test accuracy",rf.score(X_test,y_test))
	# print(rf)

	lgbc=lightgbm.LGBMClassifier()
	lgbc.fit(X_train.toarray(),y_train)
	pickle.dump(lgbc,open('../data/Rating3_Feature_LGBMClassifier.pickle','wb+'))
	print("LGBMClassifier train accuracy",lgbc.score(X_train.toarray(),y_train))
	print("LGBMClassifier test accuracy",lgbc.score(X_test.toarray(),y_test))

def main():    
	logger =logCreate.getLogger(__name__,logSettings.mycomponent['logger']) 
	data_master=pd.read_excel('../data/3_train_test.xlsx',index=None)
	train1=train_data(logger,data_master)
if __name__ == "__main__":
        main()