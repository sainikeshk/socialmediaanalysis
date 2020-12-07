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

def train_valid_data(logger,data_master,df_new_feat):
	logger.info('******************classify_using_bert execution is started***********************')

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
	master_data=preprocessData(data_master)
	lst=['from','other','others', 'subject', 'android', 'device', 're', 'edu', 'ocbc', 'citi', 'dbs', 'citibank', 'bank', 'mobile',
     'apple', 'ios', 'playstore', 'play', 'store', 'app', 'apps', 'application', 'please', 'banking','ocbc','metro','monzo',
     'adbc', 'abu', 'dhabi', 'cbd', 'hsbc', 'bochk', 'mashreq', 'barclays', 'singapore', 'uk', 'uae', 'sg', 'hk', 'ocbc','nan']
	stop_words = text.ENGLISH_STOP_WORDS.union(lst)
	master_data['Feature']=master_data['Topic']+"|"+master_data['SubTopic']

	master_data['Feature']=master_data['Topic']+"|"+master_data['SubTopic']
	labels=master_data['Feature'].unique().tolist()
	n=master_data['Feature'].value_counts().max()
	print(n)
	df_mas=pd.DataFrame(columns=list(master_data.columns))
	for label in labels:
	    vars()['df_'+str(label)]=master_data[master_data.Feature==str(label)]
	    if vars()['df_'+str(label)].shape[0]!=n:
	        vars()['df_'+str(label)]=resample(vars()['df_'+str(label)],replace = True,n_samples = n,random_state = 42)
	    df_mas=pd.concat([df_mas,vars()['df_'+str(label)]])
	print(df_mas.shape,master_data.shape)
	
	X=df_mas['txt'].values
	Y=df_mas['Feature'].values
	fac_feat = pd.factorize([*df_mas.Feature])
	df_mas['new']=fac_feat[0]
	x=df_mas['txt'].tolist()
	y=df_mas['new'].values
	df_mas=df_mas[['txt','new']]
	train_df, eval_df = train_test_split(df_mas, test_size=0.25)
	# define hyperparameter
	train_args ={"reprocess_input_data": True,
	             "fp16":False,
	             "num_train_epochs": 6}

	# Create a ClassificationModel
	model = ClassificationModel(
	    "bert", "distilbert-base-german-cased",
	    num_labels=len(df_mas.new.unique()),
	    args=train_args,use_cuda=False)
	model.train_model(train_df)
	def f1_multiclass(labels, preds):
		return f1_score(labels, preds, average='micro')
    
	result, model_outputs, wrong_predictions = model.eval_model(eval_df, f1=f1_multiclass, acc=accuracy_score)
	print(result)
	pickle.dump(model,open('../data/Bert_model.pickle','wb+'))
	enc_lst=list(set(fac_feat[0]))
	feat_dct=dict()
	for i,j in zip(enc_lst,fac_feat[1]):
	    feat_dct[i]=j
	pickle.dump(feat_dct,open('../data/feat_dct.pickle','wb+'))

def main():    
	logger =logCreate.getLogger(__name__,logSettings.mycomponent['logger']) 
	data_master=pd.read_excel('../data/ratings_merged_final.xlsx')
	df_new_feat=pd.read_excel('../data/FeatureLevelsFinal.xlsx')
	data_master=data_master[(data_master.SubTopic!='Not user friendly') & (data_master.SubTopic!='User friendly interface') & (data_master.SubTopic!='Overall a good application')]
	train_valid=train_valid_data(logger,data_master,df_new_feat)

if __name__ == "__main__":
        main()