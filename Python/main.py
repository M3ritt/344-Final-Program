import os.path
import subprocess
import re	
import shutil
import json
from json2html import*
import json		
from subprocess import check_output

def lineCounter( path ):
	
	os.chdir(path)
	for root, subdirs, files in os.walk(path):
		for f in files:
			if f.endswith(('.py', '.c', '.clj', '.pl~', '.scala')):
				if not f.startswith(('c_standard_headers_indexer')):
					#subprocess.call(['wc', '-l', os.path.join(root,f)])
					lineCount = subprocess.check_output(['wc', '-l', os.path.join(root,f)])
					count = lineCount[:3]
					words = gettingWords(path, f)
					data = { 'name': f, 
						'Lines' : str(count), 
						'Words' : words}
					if f.endswith('.c'):
						toHTML('C',data)
					if f.endswith('.py'):
						toHTML('Python',data)
					if f.endswith('.clj'):
						toHTML('Clojure',data)
					if f.endswith('.pl~'):
						toHTML('Prolog',data)
					if f.endswith('.scala'):
						toHTML('Scala',data)
					writeToJSONFile('./',f+'JSON',data)
					
		
def gettingWords(path ,file_name):
	AllWords = list()
	Result = list()
	os.chdir(path)
	for root, subdirs, files in os.walk(path):
		for f in files:
			if f==file_name:
				with open(os.path.join(root,file_name), 'r') as myfile:
					for line in open(os.path.join(root,f)):
						if not line.startswith('#'):
							words = line.split()
							AllWords.extend(words)
						if not line.startswith('//'):
							words = line.split()
							AllWords.extend(words)
						if not line.startswith('%'):
							words = line.split()
							AllWords.extend(words)
	
	for word in AllWords:
		if word not in Result:           
			Result.append(word)
	return Result
	
def words(data):
	words = set()
	result = ''
	for word in data.split():
		if word not in words:
			if line.find('#') > 0 and line.find('//') > 0 and line.find('%') > 0 and line.find(';;') >0:
				result = result + word + ' '
				words.add(word)
	print(result)
	
def zipFile(dir_name):
	shutil.make_archive('Zipped344', 'zip', dir_name)
	


def writeToJSONFile(path, fileName, data):
	if fileName.endswith('.pyJSON'):
		filePathNameWExt = './' + path + '/' + 'python/' + fileName + '.json'
		with open(filePathNameWExt, 'w') as fp:
			json.dump(data, fp)
	if fileName.endswith('.cJSON'):
		filePathNameWExt = './' + path + '/' + 'C/' + fileName + '.json'
		with open(filePathNameWExt, 'w') as fp:
			json.dump(data, fp)
	if fileName.endswith('.cljJSON'):
		filePathNameWExt = './' + path + '/' + 'Clojure/' + fileName + '.json'
		with open(filePathNameWExt, 'w') as fp:
			json.dump(data, fp)
	if fileName.endswith('.pl~JSON'):
		filePathNameWExt = './' + path + '/' + 'Prolog/' + fileName + '.json'
		with open(filePathNameWExt, 'w') as fp:
			json.dump(data, fp)
	if fileName.endswith('.scalaJSON'):
		filePathNameWExt = './' + path + '/' + 'Scala/' + fileName + '.json'
		with open(filePathNameWExt, 'w') as fp:
			json.dump(data, fp)
		
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
def sendEmail( sendTo ):
	myAddress = 'jmeritt@oswego.edu'
	subject = 'My Project!'
	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = myAddress
	msg['To'] = sendTo
	msg.preamble = "test " 
	part = MIMEBase('application', "octet-stream")
	part.set_payload(open('C:/Users/Josh/344/Zipped344.zip', 'rb').read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', 'attachment; filename="C:/Users/Josh/344/Zipped344.zip"')
	msg.attach(part)
	#try:
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login(user = 'jmeritt@oswego.edu', password = 'Jam3ritt')
	s.sendmail(myAddress, sendTo, msg.as_string())
	s.quit()
	print('sent')
	#except smtplib.SMTPException as error:
	print ("Not able to send")
	
def toHTML(lang,data):
	if lang == 'C':
		f = open('C:/Users/Josh/344/C/C.html','w')
	if lang == 'Python':
		f = open('C:/Users/Josh/344/Python/Python.html','w')
	if lang == 'Clojure':
		f = open('C:/Users/Josh/344/Clojure/Clojure.html','w')
	if lang == 'Prolog':
		f = open('C:/Users/Josh/344/Prolog/Prolog.html','w')
	if lang == 'Scala':
		f = open('C:/Users/Josh/344/Scala/Scala.html','w')
	message = json2html.convert(json = data)
	f.write(message)
	f.close()
	
#main entry point to the program
def main():
	lineCounter('C:/Users/Josh/344');
	zipFile('C:/Users/Josh/344');
	
	#need Altair
	#sendTo = input("What is your email?")
	#print("sending to: "+sendTo)
	#sendTo = 'merittjosh@gmail.com'
	#sendEmail(sendTo);
	
main();
