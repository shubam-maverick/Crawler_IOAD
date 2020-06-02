#webPageClassifier
import pandas as pd
import re
import requests
import xlsxwriter
from origin import *
from bs4 import BeautifulSoup
from xlutils.copy import copy    
from xlrd import open_workbook

def writeInExcel(url):
	print(url);
	global rowNum;
	book_ro = open_workbook("facultyListLinks.xls");
	book = copy(book_ro);  						# creates a writeable copy
	sheet = book.get_sheet(0);
	try:
		sheet.write(rowNum, 0, url);	
		rowNum = rowNum + 1;
	except:
		print("Write Error3");
	book.save("facultyListLinks.xls");

def computeTf(text,word):						# to count freq/prob of a keyword in a page
	# print text.encode("utf-8");
	count = 0;
	totalWords = len(text);
	for each in text.split("\n"):
		breakText = re.sub('[^A-Za-z]+',' ',text);
		#print (breakText.lower());
		breakText = breakText.split(' ');
		# print (breakText);
		#print totalWords;
		for i in range(len(breakText)):
			if(breakText[i].lower() == word.lower()):
				count = count + 1;
	try:
		prob = float(count)/totalWords;
	except:
		print("----------------divisionByZero--------------------")
		prob = 0;
	return prob;

def netProb(allCountProb):							#Cal total freq/prob of  all keywords
	n = len(allCountProb);
	sumOfProb = 0;
	for i in range(n):
		sumOfProb = sumOfProb + allCountProb[i];
	return sumOfProb;

def classify(url):
	try:
		req = requests.get(url);
	except requests.exceptions.ConnectionError:
		print("ConnectionError");
		return;
	except requests.exceptions.InvalidSchema:
		print("SchemaError");
		return;
	except:
		print("--------------------Error during request-------------------");
		return;

	data = req.text;
	soup = BeautifulSoup(data,'lxml');
	for script in soup(["script", "style"]):
		script.extract()    # rip it out
	text = soup.get_text()		# get text
	#print text.encode("utf-8");
	lines = (line.strip() for line in text.splitlines())		# break into lines and remove leading and trailing space on each
	#print lines;
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))	# break multi-headlines into a line each
	text = ' '.join(chunk for chunk in chunks if chunk)		# drop blank lines
	# print (text);

	keywords = pd.read_excel("E:/Project/Backend/TxtFiles/keywordsToClassify.xlsx");
	n = keywords.index;
	#print soup;
	#print keywords;
	allCountProb = [];
	for colInKeywords in n:
		count = computeTf(text,keywords["Key"][colInKeywords]);
		allCountProb.append(count);
	print (netProb(allCountProb));
	if(netProb(allCountProb) >= 0.0025):
		try:
			print("----------------WritingFacultyLink-----------------")
			writeInExcel(url);
		except:
			print("------------WriteError2----------------");	
		getName(text,keywords,n);

workbook = xlsxwriter.Workbook("facultyListLinks.xls");
sheet = workbook.add_worksheet();
workbook.close();
rowNum = 0;
writeInExcel("Faculty List Links");
# classify("http://www.uct.ac.za/main/research/leading-researchers/assaf");