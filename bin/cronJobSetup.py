#!/usr/bin/python3
# coding: utf-8
# packages
import warnings
warnings.filterwarnings("ignore")
from crontab import CronTab
import os
import logCreate
import logSettings
import analysisRunall 
from readConfig import readValue

def main():
	runall = analysisRunall.cronset()
	print(runall)
	usr = os.getlogin()
	print("login username is :",usr)
	mycron = CronTab(user=usr)
	filename=runall.split(">")[0].split("/")[-1]
	mycron.remove_all(command=filename)

	job = mycron.new(command=runall)
	job.every(8).hours()
	mycron.write()

if __name__ == "__main__":
		main()
