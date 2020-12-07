#!/usr/bin/python3
# coding: utf-8
# packages
import warnings
warnings.filterwarnings("ignore")
import os
import configparser
import pathlib
import sys

def cronset():
	config = configparser.ConfigParser()
	config.read('../etc/application.ini')

	cwd = os.getcwd()
	runallpath = "python3 %s/analysisRunall.py > /tmp/cron.socialmedia.analysis.log  2>&1"%cwd
	runallpath1 =runallpath.replace(os.sep, '/')

	return runallpath1
	

changeDir=os.chdir(os.path.dirname(os.path.abspath(__file__)))
# print('working directory: ', os.getcwd())

import ratings_1_train
import ratings_12_predict
import ratings_5_train
import ratings_45_predict
import ratings_3_train
import rating_3_predict
import bert_train_data
import bert_predict_model
import update_table
import predictCumulative
import flagUpdate

def main():
	#train1=ratings_1_train.main()
	#pred12=ratings_12_predict.main()
	#train5=ratings_5_train.main()
	#pred45=ratings_45_predict.main()
	#train1=ratings_3_train.main()
	#pred3=rating_3_predict.main()
	#flag =flagUpdate.main()
	bert_train=bert_train_data.main()
	bert_predict=bert_predict_model.main()
	updat=update_table.main()
	# predictCumu=predictCumulative.main()
if __name__ == "__main__":
		main()
