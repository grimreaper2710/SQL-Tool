from xml2xlsx import xml2xlsx
from openpyxl import Workbook
import xml.etree.ElementTree as ET
import os
import datetime

def backup_query(p_query,p_instance):
        if os.path.isdir('Query_History'):
                None
        else:
                os.makedirs('Query_History')
        aa = open('Query_History/'+p_instance+'_'+'{0:%d%m%Y%H%M%S}'.format(datetime.datetime.now())+'.txt','w')
        aa.write(p_query)
        aa.close()

def readFile(p_xml):
	'''
		Checks if file exists, parses the file and extracts the needed data
		returns a 2 dimensional list without "header"
	'''
	
	tree = ET.ElementTree(ET.fromstring(str(p_xml)))
	root = tree.getroot()
	#you may need to adjust the keys based on your file structure
	dict_keys = [] #all keys to be extracted from xml
	for type_tag in root.findall('ROW'):
		for i in type_tag.iter():
			dict_keys.append(i.tag)
		break
	mdlist = []
	mdlist.append(dict_keys)
	for child in root.findall('ROW'):
		temp = []
		for key in child.iter():
			temp.append(key.text)
		mdlist.append(temp)
	return mdlist

def to_Excel(mdlist,p_name):
	'''
		Generates excel file with given data
		mdlist: 2 Dimenusional list containing data
	'''
	wb = Workbook()
	ws = wb.active
	for i,row in enumerate(mdlist):
		for j,value in enumerate(row):
			ws.cell(row=i+1, column=j+1).value = value
	if os.path.isdir('Export_Excel'):
		None
	else:
		os.makedirs('Export_Excel')
	newfilename = os.path.abspath('Export_Excel/'+p_name+".xlsx")
	wb.save(newfilename)
	#print("complete")
	return True

def main(p_xml,p_name):
        try:
                to_Excel(readFile(p_xml),p_name)
                return True
        except:
                return False


