import speech_recognition as sr
from gtts import gTTS
import os
import codecs
import MySQLdb
import re
from pythongui import BuildGui

class ProcessText(object):

	def __init__(self):
		self.guiObj = BuildGui()
		self.conn = MySQLdb.connect(host="127.0.0.1",user="root",passwd="root",db="python")
		self.cur = self.conn.cursor()
		self.universalWords = {
							   'master','miss','mr','mrs','and','from','the','where','i','can','person','how','are','you','could','shall','should',
							   'find','is','who','for','best','teacher','teachers','professor','teach','subject','teaching','which','were','what','would','in',
							   'free','list','of','stitching','show','me','song','play','video','any','stand','department','cabin','sir','professors','block','shall','should',
							   'be','having','have','stand','block','blocks','department','school','engineering','science','hostel','hostels','office','faculty','is','the','faculties','deaching'
							   }
		self.personDetails = []					   


	def fetchAllData(self,tableName):
		self.cur.execute("SELECT * FROM "+tableName)
		return 	self.cur.fetchall()

	def fetchSpecificData(self,tableName,condition):
		self.cur.execute("SELECT * FROM "+tableName+" where "+condition)
		return 	self.cur.fetchall()			

	def processData(self,textdata):

		findPerson  = 0

		if textdata.split("who is")[0] == textdata:
			inputList = textdata.split(' ')
		else:
			findPerson = 1	
			inputList = textdata.split(' ')

		inputList = [x.lower() for x in inputList]

		toFindPerson = ['person','find','where','can','search', 'name']
		toFindProf   = ['best','teacher','faculties','faculty','teachers','professor','teach','subject','teaching','show']

		toFindBlock  = ['which','block','blocks','department','school','engineering','boys','boy','girl','girls','hostel','office']

		if findPerson:
			if any(x in toFindProf for x in inputList):
				print('Teacher')
				self.searchTeacher(inputList)
				return	

		if any(x in toFindProf for x in inputList):
			print('Teacher')
			self.searchTeacher(inputList)
			return		

		elif findPerson or any(x in toFindPerson for x in inputList):
			if any(x in toFindBlock for x in inputList):
					print('Blocks')
					self.searchBlocks(inputList)	
					return
			else:		
				print('Person')
				self.searchPerson(inputList)
				return

		elif any(x in toFindBlock for x in inputList):
			print('Blocks')
			self.searchBlocks(inputList)	
			return		





	def searchPerson(self,textdata):

		lastNames = ['Khanna','Makhija','Vyas','Mahatma','Thakor','Saxena','Suthar','Dave', 'Patel','Solanki','Sharma']

		queryResult = self.personDetails

		searchData = [x for x in textdata if x not in self.universalWords]

		filterFName = []
		filterFullName = []

		def checkLastName(dlen,i,searchD,addName):
			if i<dlen and searchD[i] in lastNames:
				addName = addName +' '+ searchD[i] 
				return checkLastName(dlen, i+1, searchD, addName)
			return addName	

		for i,item in enumerate(searchData):
			addN = item
			finalName = checkLastName(len(searchData), i+1, searchData, addN)

			if item not in lastNames:
				filterFName.append(item)
				filterFullName.append(finalName)

		nameList = []

		try:

			for name in filterFName:
				nameList.append(self.searchPersonName(name,queryResult))

			datamat = [['UID','FNAME','MNAME','LNAME','DESIGNATION','CABIN']]	

			try:
				for lst in nameList:
					for item in lst:
						ls = []
						for el in item:
							ls.append(str(el))
						datamat.append(ls)
				
				self.guiObj.buildTable(len(datamat),6,datamat)	
			except:
				self.textToSpeech('No person found, please ask again.')		

		except:
			raise
			self.textToSpeech('Some problem occur, please ask again.')					


	def searchPersonName(self,name,queryResult):
		flag = 0
		nameList = []
		# print(name)
		for i,item in enumerate(queryResult):
			it = iter(item[1].lower())
			if 	all(any(c == ch for c in it) for ch in name):
				nameList.append(item)
				flag = 1

		if flag == 0:
			return None

		return nameList			


	def searchTeacher(self,textdata):

		subjectMainBranch = [
							 ['compilerdesigning','system programming'],
							 ['operatingsystem','system programming'],
							 ['systemprogramming','system programming'],
							 ['database','database system'],
							 ['cloudcomputing','database system'],
							 ['computernetworks','networking and security'],
							 ['computernetwork','networking and security'],
							 ['networks','networking and security'],
							 ['network','networking and security'],
							 ['networksecurity','networking and security'],
							 ['security','networking and security'],
							 ['cloud','database system']
							]

		searchData = [x for x in textdata if x not in self.universalWords]		

		subjectName = ''

		for item in searchData:
			subjectName = subjectName+item

		for item in subjectMainBranch:
			if re.search(subjectName, item[0]):
				self.textToSpeech('This is the list of Teachers who is teaching '+item[0])
				queryResult = self.fetchSpecificData('occupation','depart="'+item[1]+'"')
				
				datamat = [['UID','FNAME','MNAME','LNAME','DESIGNATION','CABIN']]	

				for personData in queryResult:
					# print(personData)
					for subquery in self.personDetails:
						# print(subquery)
						if personData[0]==subquery[0]:
							ls = []
							for item in subquery:
								ls.append(item)
							datamat.append(ls)
							break

				
				self.guiObj.buildTable(len(datamat), 6, datamat)	

				return

		self.textToSpeech('Sorry no teacher found, please ask again.')		

		# queryResult = self.fetchSpecificData('occupation')
		# queryResult = sorted(queryResult)


	def searchBlocks(self,textdata):
		searchData = [x for x in textdata if x not in self.universalWords]
		print(searchData)
		queryResult = self.fetchAllData('building')

		datamat = [['Block Number','Block Name']]

		flag = 0

		for item in queryResult:
			if re.search(searchData[0], item[1]):
				flag = 1
				datamat.append([item[0],item[1]])


		if flag == 0:		
			self.textToSpeech('Sorry no block found, please ask again.')
			return

		self.guiObj.buildTable(len(datamat), 2, datamat)	

				

	def fetchPersonData(self):
		self.personDetails = self.fetchAllData('person')	


	def textToSpeech(self,textdata):
		tts = gTTS(text=textdata, lang='en-us')
		tts.save("hello.mp3")
		os.system('mpg123 hello.mp3')	



class VoiceInteraction(object):

	def __init__(self):
		self.r = sr.Recognizer()
		self.r.operation_timeout=5

	def captureVoice(self):
		with sr.Microphone(chunk_size=4096) as source:
		    print("Say something!")
		    self.r.adjust_for_ambient_noise(source,1)
		    audio = self.r.listen(source)	
		    print('Wait..')	    
		    try:
		    	return self.r.recognize_google(audio,language='en-GB')
		    except:
		    	return None



if __name__ == "__main__":
	
	voiceObject = VoiceInteraction()		
	textObject  = ProcessText()
	textObject.fetchPersonData()

	speechToText = ""
	textObject.textToSpeech("Hi, How may i help you?")
	while not ("bye" in speechToText.split(" ")):
		speechToText = voiceObject.captureVoice()
		if speechToText is not None:
			print('You said : '+speechToText)
			print('')
			textObject.processData(speechToText)
		else: 
			print('Unable to understand.')	
			speechToText = ""
