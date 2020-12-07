#!/usr/bin/python3
# coding: utf-8
# packages
import os
import cleanPackage
import logCreate
import logSettings

logger = logCreate.getLogger(__name__,logSettings.mycomponent['logger'])

def main():
	removelog=cleanPackage.cleanlog()
	removefiles=cleanPackage.cleanfolder()

if __name__ == "__main__":
		main()