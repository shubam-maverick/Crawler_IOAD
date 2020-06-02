#Crawler
import requests
import queue as Queue
import re
import xlsxwriter
import tldextract
from webPageClassifier import *
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from trie import *
from textClassifier import *
from xlutils.copy import copy    
from xlrd import open_workbook
from infoStore import *
#import exceptions

def listToString(s):  
	str = "";    
	for ele in s:  
		str += ele;
		str += " ";
    
	return str

def isVisited(url):
	#print url
	if find(visitedLinks,url)  == True:
		return True
	else:
		insert(visitedLinks,url)
		return False

def checkDepth(linkQueue, targetDepth):
	link = linkQueue.queue[0];
	if(link.depth == targetDepth):
		return True;
	else:
		return False;

def notInDomain(url):
	global domain;
	if(tldextract.extract(url).domain != domain):
		return True;
	return False;

def getParent(url):									#Parent is the base url
	url = urlparse(url);
	parent = url.scheme + "://" + url.netloc;
	return parent;

def newParent(url):									#For http to https and vica versa
	url = urlparse(url);
	if(url.scheme == "https"):
		parent = "http://" + url.netloc;
	else:
		parent = "https://" + url.netloc;
	return parent;

def writeInExcel(url):
	print(url);
	global rowNum;
	book_ro = open_workbook("validLinks.xls");
	book = copy(book_ro);  						# creates a writeable copy
	sheet = book.get_sheet(0);
	try:
		sheet.write(rowNum, 0, url);	
		rowNum = rowNum + 1;
	except:
		print("Write Error3");
	book.save("validLinks.xls");

def createURL(link):
	url = link.child;
	url = urlparse(url);
	#print url;
	if(url.scheme == ""):
		if(len(link.child) > 0 and link.child[0] != '/'):
			newURL = link.parent + '/' + link.child;
		else:
			newURL = link.parent + link.child;
	else:
		newURL = link.child;
	return newURL;

def validLinks(linkQueue, soup, parent, link):
	for anchorTag in soup.find_all('a'):
		anchorLink = anchorTag.get('href');
		if anchorLink is None:
			continue;
		anchorText = anchorTag.text;
		newLink = infoLink();
		newLink.info(parent, anchorLink, link.depth+1, anchorText);        #Link refers to info about parent, child, depth, text
		newLink1 = infoLink();
		parent = newParent(parent);											
		newLink1.info(parent, anchorLink, link.depth+1, anchorText);
		#print validityCheck(link)
		if((isVisited(createURL(newLink)) == False) and validityCheck(newLink)):
			linkQueue.put(newLink);
			try:
				print("--------------WritingPossibleLink----------------");
				writeInExcel(createURL(newLink));
			except:
				print("--------------WriteError1-----------------------");
				#print e;
				continue;
			classify(createURL(newLink));

		if((isVisited(createURL(newLink1)) == False) and validityCheck(newLink1)):
			linkQueue.put(newLink1);
			try:
				print("--------------WritingPossibleLink----------------");
				writeInExcel(createURL(newLink));
			except:
				print("--------------WriteError1-----------------------");
				#print e;
				continue;
			classify(createURL(newLink1));
	return linkQueue;

def crawlNewURL(linkQueue, targetDepth = 10):
	print('Yes');
	while(linkQueue.empty() == False):
		print("------------------FromQueue-------------------------");
		if(checkDepth(linkQueue, targetDepth)):
			return linkQueue;
		link = linkQueue.get();
		url = createURL(link);
		print ("-----------------New Request: " + url + "----------------------------");
		if(notInDomain(url)):
			continue;	
		parent = getParent(url);											#URL is the one to which request will be made
		try:
			print("---------------Requesting-------------------");
			req = requests.get(url,timeout=5);
			print(req);
		except requests.exceptions.ConnectionError:
			print("ConnectionError");
			continue;
		except requests.exceptions.InvalidSchema:
			print("schemeError");
			continue;
		except:
			print("--------------------Error during request-------------------");
			continue;
	
		data = req.text;
		soup = BeautifulSoup(data,'lxml');
		linkQueue = validLinks(linkQueue, soup, parent, link);
		#Checking if web page contains name will come here
	return linkQueue;

workbook = xlsxwriter.Workbook("validLinks.xls");
sheet = workbook.add_worksheet();
workbook.close();
rowNum = 0;
writeInExcel("Valid Links")
linkQueue = Queue.Queue(maxsize = 0);
visitedLinks = trieNode('*')
seedURL = "http://www.pec.ac.in";							#Trie to check visited links
seedLink = infoLink();
domain = tldextract.extract(seedURL).domain;
#print domain;
seedLink.info("",seedURL,0,"This is China");
isVisited(createURL(seedLink));
# isVisited("http://www.uct.ac.za/");
# isVisited("http://www.uct.ac.za/main");
# isVisited("http://www.uct.ac.za/#");
# isVisited("http://www.uct.ac.za/#main-content");
linkQueue.put(seedLink);
linkQueue = crawlNewURL(linkQueue);