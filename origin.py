#Get Indian Names
from __future__ import print_function
import time
import re
import xlsxwriter
import nltk
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize 
from xlutils.copy import copy    
from xlrd import open_workbook

from pprint import pprint
from trie import *

def isVisited(fullName):
	#print url
	if find(visitedNames,fullName)  == True:
		return True;
	else:
		insert(visitedNames,fullName);
		return False;

def isName(fullName):
	# print(fullName);
	stop_words = set(stopwords.words('english'))   
	# sent_tokenize is one of instances of PunktSentenceTokenizer from the nltk.tokenize.punkt module   
	tokenized = sent_tokenize(fullName); 
	for i in tokenized:
	    # Word tokenizers is used to find the words and punctuation in a string 
	    wordsList = nltk.word_tokenize(i); 
	    # removing stop words from wordList 
	    wordsList = [w for w in wordsList if not w in stop_words];  
	    #  Using a Tagger. Which is part-of-speech tagger or POS-tagger.  
	    tagged = nltk.pos_tag(wordsList)
	try:
		if(tagged[0][1] == 'NNP' and tagged[1][1] == 'NNP'):
			return True;
		elif(tagged[0][1] == 'NN' and tagged[1][1] == 'NNP'):
			return True;
		elif(tagged[0][1] == 'NNP' and tagged[1][1] == 'NN'):
			return True;
		else:
			return False;
	except:
		return False;


def writeInExcelAllNames(fullName):
	global rowNum1;
	book_ro = open_workbook("allNames.xls");
	book = copy(book_ro);  						# creates a writeable copy
	sheet = book.get_sheet(0);
	try:
		sheet.write(rowNum1, 0, fullName);	
		rowNum1 = rowNum1 + 1;
	except:
		print("Write Error3");
	book.save("allNames.xls");

def writeInExcel(fullName):
	global rowNum;
	book_ro = open_workbook("Names.xls");
	book = copy(book_ro);  						# creates a writeable copy
	sheet = book.get_sheet(0);
	try:
		sheet.write(rowNum, 0, fullName);	
		rowNum = rowNum + 1;
	except:
		print("Write Error3");
	book.save("Names.xls");

def checkOrigin(title,firstName, lastName):
	# apiInstance = openapi_client.PersonalApi(openapi_client.ApiClient(configuration));
	# print (title);
	fullName = title + ' ' + firstName + ' ' + lastName;
	fullName = fullName.lstrip();
	if(isVisited(fullName.lower())):
		return;
	if(isName(fullName) == False):
		return;
	else:
		writeInExcelAllNames(fullName);
	# try:
	# 	# [USES 10 UNITS] Infer the likely country of origin of a personal name. Assumes names as they are in the country of origin..
	# 	apiResponse = apiInstance.origin(firstName, lastName);
	# 	return apiResponse.country_origin;
	# except ApiException as e:
	# 	print("Exception when calling PersonalApi->origin: %s\n" % e);
		return None;

def getName(text,keywords,n):											#to skip titles
	breakText = re.sub('[^A-Za-z]+',' ',text);
	#print breakText.lower();
	breakText = breakText.split(' ');
	flag = 0;
	forFirstTime = 0;
	firstName1 = ""
	lastName1 = ""
	title = ""
	for i in range(len(breakText)):
		setVar = 0;
		for colInKeywords in n:
			word = keywords["Key"][colInKeywords];
			if(word.lower() == breakText[i].lower()):
				if(flag==0):
					try:
						firstName1 = breakText[i-2]
						lastName1 = breakText[i-1] 
					except:
						print("No names behind")
				flag = 1;
				setVar = 1;
				title = title + ' ' + word;
				# print (title);
				break;
		if(setVar == 0 and flag == 1):
			firstName = breakText[i];
			lastName = breakText[i+1];
			flag = 0;
			if(checkOrigin(title,firstName,lastName) == "IN"):
				fullName = title + ' ' + firstName + ' ' + lastName;
				fullName = fullName.lstrip();
				writeInExcel(fullName);
				print (fullName);
			if(checkOrigin(title,firstName1,lastName1) == "IN"):
				fullName = title + ' ' + firstName1 + ' ' + lastName1;
				fullName = fullName.lstrip();
				writeInExcel(fullName);
				print (fullName);
			title = ""

workbook = xlsxwriter.Workbook("Names.xls");
sheet = workbook.add_worksheet();
workbook.close();
rowNum = 0;

workbook1 = xlsxwriter.Workbook("allNames.xls");
sheet1 = workbook1.add_worksheet();
workbook1.close();
rowNum1 = 0

writeInExcel("Names");
writeInExcelAllNames("ALL_NAMES")
# configuration = openapi_client.Configuration();
# configuration.api_key['X-API-KEY'] = '50c03592319958b1cfd2950bab55592b';
visitedNames = trieNode('*')


# if(checkOrigin("Ismaeel","Abrahams") == "IN"):
#  	print ("Valah")