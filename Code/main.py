import cv2
import numpy as np
from PIL import Image
import urllib
from gtts import gTTS
import os
import codecs
import MySQLdb
import speech_recognition as sr
import codecs
import re
from pythongui import BuildGui
import time
import tkinter as tk
from PIL import Image, ImageTk
from VerifyImage import VerifyImage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class ProcessText(object):

    def __init__(self):
        self.r = sr.Recognizer()
        self.r.operation_timeout=5
        self.guiObj = BuildGui()
        self.conn = MySQLdb.connect(host="127.0.0.1",user="root",passwd="root",db="python")
        self.cur = self.conn.cursor()
        self.universalWords = {
                               'master','please','miss','mr','mrs','and','from','the','where','i','can','person','how','are','you','could','shall','should',
                               'find','is','who','for','best','teacher','teachers','professor','teach','subject','teaching','which','were','what','would','in',
                               'free','list','of','stitching','show','me','song','play','video','any','stand','department','cabin','sir','professors','block','shall','should',
                               'be','having','have','stand','block','blocks','department','school','engineering','science','hostel','hostels','office','faculty','is','the','faculties','deaching'
                               }
        self.filterUniversalWords = {
                               'master','miss','mr','mrs','and','from','the','where','i','can','person','how','are','you','could','shall','should',
                               'find','is','who','for','best','teacher','teachers','professor','teach','subject','teaching','which','were','what','would','in',
                               'free','list','of','stitching','show','me','song','play','video','any','stand','cabin','sir','professors','block','shall','should',
                               'be','having','have','stand','block','blocks','engineering','hostel','hostels','office','faculty','is','the','faculties','deaching'
                               }                       
        self.personDetails = []                    
        self.higherAuthList = []
        self.aboutCollege = []


    def fetchAllData(self,tableName):
        self.cur.execute("SELECT * FROM "+tableName)
        return  self.cur.fetchall()

    def fetchSpecificData(self,tableName,condition):
        self.cur.execute("SELECT * FROM "+tableName+" where "+condition)
        return  self.cur.fetchall()         

    def processData(self,textdata):

        findPerson  = 0

        if textdata.split("who is")[0] == textdata:
            inputList = textdata.split(' ')
        else:
            findPerson = 1  
            inputList = textdata.split(' ')

        inputList = [x.lower() for x in inputList]

        toFindAboutProject = ['what','name']
        toFindAboutCollege = ['chancellor','vice','pro','chairman','founder','dean']
        toFindPerson = ['person','find','where','can','search', 'name']
        toFindProf   = ['best','teacher','faculties','faculty','teachers','professor','teach','subject','teaching','show']
        toFindHigherAuth = ['hod','head','coordinator','hos','placement', 'dean']

        toFindBlock  = ['which','block','blocks','department','school','engineering','boys','boy','girl','girls','hostel','office']

        if 'program' in inputList or 'programs' in inputList:
            return
        if 'activate' in inputList or 'active' in inputList:
            return
        if 'thank' in inputList or 'thanks' in inputList:
            return    

        if findPerson:

            if any(x in toFindAboutCollege for x in inputList):
                print('About College')
                self.searchAboutCollege(inputList)
                return

            if any(x in toFindHigherAuth for x in inputList):
                print('Higher Authorities')
                self.searchHigherAuth(inputList)
                return

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

        elif any(x in toFindHigherAuth for x in inputList):
                print('Higher Authorities')
                self.searchHigherAuth(inputList)
                return

        elif any(x in toFindAboutCollege for x in inputList):
                print('About College')
                self.searchAboutCollege(inputList)
                return        
                
        else:
            self.guiObj.errorMessage('You search for : '+textdata)
            self.textToSpeech('Sorry unable to understand, please ask again.')



    def searchPerson(self,textdata):

        lastNames = ['patel','solanki','dave','saxena','gadhvi','suthar','khanna','manna','garg','malik','yadav','smith','raizada','shrivastava', 'preet','pataria','makhija','bakshi','mathur','mehta','maru']

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
                
                speechToText = ""
                uid = 0
                try:
                    pass
                except:
                    # raise
                    print('Voice Problem')            


            except:
                # raise
                msg = ""
                for item in searchData:
                    msg = msg + item + ' '
                self.guiObj.errorMessage('You search for : '+str(msg))
                self.textToSpeech('No person found, please ask again.')     

        except:
            # raise
            self.textToSpeech('Some problem occur, please ask again.')                  



    def searchPersonName(self,name,queryResult):
        flag = 0
        nameList = []
        # print(name)
        for i,item in enumerate(queryResult):
            it = iter(item[1].lower())
            if  all(any(c == ch for c in it) for ch in name):
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
                             ['networking','networking and security'],
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
        self.guiObj.errorMessage('You search for : '+str(subjectName))
        # queryResult = self.fetchSpecificData('occupation')
        # queryResult = sorted(queryResult)


    def searchHigherAuth(self,textdata):
        localWords = {
                       'block','blocks','department','engineering',
                       'hod','head','coordinator','hos','school','placements',
                       'placement'
                      }
        searchData = [x for x in textdata if x not in self.filterUniversalWords]
        datamat = [['SNo.','Name','Cabin','Email Address']]
        
        if 'hod' in searchData:
            self.searchHOD(localWords,searchData,datamat)   

        elif 'head' in searchData:

            if 'school' in searchData:

                searchData = [x for x in searchData if x not in localWords]
                depart = ''
                cdepart = ''
                for item in searchData:
                    depart += item
                    cdepart  = cdepart+item+' '

                if re.search(depart, 'computerscience') or re.search(depart, 'cse'):
                    sno = 111
                    flag = 0

                    for item in self.higherAuthList:

                        if item[0] == 'hos' and re.search('lfts',item[2]):
                            flag = 1
                            datamat.append([sno,item[3],item[4],item[5]])
                            sno += 1

                    if flag == 0:
                        self.guiObj.errorMessage('You search for :'+cdepart)
                        self.textToSpeech('Sorry unable to process!')
                        return

                    self.guiObj.buildTable(len(datamat), 4, datamat)

                    speechToText = ""
                    name = ''
                    email = ''

                    try:
                        while not (("yes" in speechToText.split(" ")) or ("no" in speechToText.split(" "))):
                            self.textToSpeech('Do you want to meet H.O.S?')
                            os.system('nohup play /home/swati/Documents/Project/FinalYProject/Notification/end.mp3 &')
                            speechToText = self.captureVoice()
                            if speechToText is not None:
                                pass
                            else:
                                speechToText = ""

                        if ("yes" in speechToText.split(" ")):  
                            if len(datamat) == 2:
                                message = ""
                                self.textToSpeech('Please wait i am notifying '+datamat[1][1]+' about meeting.')        
                                self.sendMail(datamat[1][3],message+'wants to meet you.')
                                self.confirmMeeting(datamat[1][1],datamat[1][2])
                            
                    except:
                        # raise
                        print('Voice Problem')
                return   

            elif 'department' in searchData:
                self.searchHOD(localWords, searchData, datamat)
                return

        elif 'coordinator' in searchData:

            if ('placement' in searchData) or ('placements' in searchData):
                searchData = [x for x in searchData if x not in localWords]
                depart = ''
                cdepart = ''
                for item in searchData:
                    depart += item
                    cdepart  = cdepart+item+' '

                if re.search(depart, 'computerscience') or re.search(depart, 'cse'):
                    sno = 111
                    flag = 0

                    for item in self.higherAuthList:

                        if item[0] == 'coordinator' and re.search('placement',item[1]) and re.search('cse',item[2]):
                            flag = 1
                            datamat.append([sno,item[3],item[4],item[5]])
                            sno += 1

                    if flag == 0:
                        self.guiObj.errorMessage('You search for :'+cdepart)
                        self.textToSpeech('Sorry unable to process!')
                        return

                    self.guiObj.buildTable(len(datamat), 4, datamat)

                    speechToText = ""
                    name = ''
                    email = ''
                    cabin = ''
                    try:
                        while not (("yes" in speechToText.split(" ")) or ("no" in speechToText.split(" "))):
                            self.textToSpeech('Do you want to meet Placement Coordinator?')
                            os.system('nohup play /home/swati/Documents/Project/FinalYProject/Notification/end.mp3 &')
                            speechToText = self.captureVoice()
                            if speechToText is not None:
                                if 'yes' in speechToText.split(' '):
                                    if len(datamat) == 2:
                                        message = ""
                                        self.textToSpeech('Please wait i am notifying '+datamat[1][1]+' about meeting.')        
                                        self.sendMail(datamat[1][3],message+'wants to meet you.')
                                        self.confirmMeeting(datamat[1][1],datamat[1][2])
                                    else:
                                        self.textToSpeech('Please take a look to details and tell me the serial number of Placement Coordinator whom you want to meet.')
                                        self.guiObj.buildTable(len(datamat), 4, datamat)
                                        self.textToSpeech('Which serial number ?')
                                        while True:
                                            try:
                                                os.system('nohup play /home/swati/Documents/Project/FinalYProject/Notification/end.mp3 &')        
                                                cspeechToText = self.captureVoice()
                                                print(cspeechToText)
                                                name =   datamat[int(cspeechToText)%10][1]
                                                email =  datamat[int(cspeechToText)%10][3]
                                                cabin =  datamat[int(cspeechToText)%10][4]
                                                break
                                            except:
                                                self.textToSpeech('Unable to understand, please mention serial number again.')        

                                        message=""
                                        self.textToSpeech('Please wait i am notifying '+name+' about meeting.')
                                        self.sendMail(email,message+'wants to meet you.')
                                        self.confirmMeeting(name,cabin)
                            else:
                                speechToText = ""

                    except:
                        print('Error')  

                return

            elif 'school' in searchData:

                searchData = [x for x in searchData if x not in localWords]
                depart = ''
                cdepart = ''
                for item in searchData:
                    depart += item
                    cdepart  = cdepart+item+' '

                if re.search(depart, 'computerscience') or re.search(depart, 'cse'):
                    sno = 111
                    flag = 0

                    for item in self.higherAuthList:

                        if item[0] == 'cos' and re.search('lfts',item[2]):
                            flag = 1
                            datamat.append([sno,item[3],item[4],item[5]])
                            sno += 1

                    if flag == 0:
                        self.guiObj.errorMessage('You search for :'+cdepart)
                        self.textToSpeech('Sorry unable to process!')
                        return

                    self.guiObj.buildTable(len(datamat), 4, datamat)

                    speechToText = ""
                    name = ''
                    email = ''

                    try:
                        while not (("yes" in speechToText.split(" ")) or ("no" in speechToText.split(" "))):
                            self.textToSpeech('Do you want to meet C.O.S?')
                            os.system('nohup play /home/swati/Documents/Project/FinalYProject/Notification/end.mp3 &')
                            speechToText = self.captureVoice()
                            if speechToText is not None:
                                pass
                            else:
                                speechToText = ""

                        if ("yes" in speechToText.split(" ")):  
                            if len(datamat) == 2:
                                detaillist = ""
                                message = "User"

                                self.textToSpeech('Please wait i am notifying '+datamat[1][1]+' about meeting.')        
                                self.sendMail(datamat[1][3],message+'wants to meet you.')
                                self.confirmMeeting(datamat[1][1],datamat[1][2])
                            
                    except:
                        # raise
                        print('Voice Problem')
                return  



    def searchHOD(self,localWords,searchData,datamat):
        
        searchData = [x for x in searchData if x not in localWords]
        depart = ''
        cdepart = ''
        for item in searchData:
            depart += item
            cdepart  = cdepart+item+' '

        flag = 0
        sno  = 111

        for item in self.higherAuthList:

            if item[0] == 'hod' and re.search(depart,item[1]):
                flag = 1
                datamat.append([sno,item[3],item[4],item[5]])
                sno += 1

        if flag == 0:
            self.guiObj.errorMessage('You search for :'+cdepart)
            self.textToSpeech('Sorry unable to process!')
            return

        self.guiObj.buildTable(len(datamat), 4, datamat)

        speechToText = ""
        name = ''
        email = ''
        cabin = ''

        try:
            while not (("yes" in speechToText.split(" ")) or ("no" in speechToText.split(" "))):
                self.textToSpeech('Do you want to meet H.O.D?')
                os.system('nohup play /home/swati/Documents/Project/FinalYProject/Notification/end.mp3 &')
                speechToText = self.captureVoice()
                if speechToText is not None:
                    pass
                else:
                    speechToText = ""

            if ("yes" in speechToText.split(" ")):  
                if len(datamat) == 2:
                    detaillist = ""
                    with open('image/persondata.txt','r') as file:
                        detaillist = file.readlines()
                        message = ""
                    for item in detaillist:
                        message = message+item+'\n'

                    self.textToSpeech('Please wait i am notifying '+datamat[1][1]+' about meeting.')        
                    self.sendMail(datamat[1][3],message+'wants to meet you.')
                    self.confirmMeeting(datamat[1][1],datamat[1][2])
                else:
                    self.textToSpeech('Please take a look to details and tell me the serial number of H.O.D whom you want to meet.')
                    self.guiObj.buildTable(len(datamat), 4, datamat)
                    self.textToSpeech('Which serial number ?')
                    while True:
                        try:
                            os.system('nohup play /home/swati/Documents/Project/FinalYProject/Notification/end.mp3 &')        
                            cspeechToText = self.captureVoice()
                            print(cspeechToText)
                            name =   datamat[int(cspeechToText)%10][1]
                            email =  datamat[int(cspeechToText)%10][3]
                            cabin =  datamat[int(cspeechToText)%10][4]
                            break
                        except:
                            self.textToSpeech('Unable to understand, please mention serial number again.')        

                    message=""
                    self.textToSpeech('Please wait i am notifying '+name+' about meeting.')
                    self.sendMail(email,message+'wants to meet you.')
                    self.confirmMeeting(name,cabin)
        except:
            # raise
            print('Voice Problem')
        return


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
            self.guiObj.errorMessage('You search for :'+str(searchData))
            self.textToSpeech('Sorry no block found, please ask again.')
            return

        self.guiObj.buildTable(len(datamat), 2, datamat)    


    def searchAboutCollege(self,textdata):
        if 'chairman' in textdata or 'founder' in textdata:
            print('Search for founder of College')
            for item in self.aboutCollege:
                if 'founder' == item[0]:
                    table = [['Image','Name','Designation'],['',item[1],'Founder of College']]
                    self.guiObj.buildTableWithImage(2, 3, table, item[4])
                    return
            self.guiObj.errorMessage('You search for :'+str(textdata))
            self.textToSpeech('Sorry some problem occur, please ask again.')        
            return

        if 'vice' in textdata and 'chancellor' in textdata:
            print('Search for vice chancellor') 
            for item in self.aboutCollege:
                if 'vicechancellor' == item[0]:
                    table = [['Image','Name','Designation'],['',item[1],'Vice-Chancellor of College']]
                    self.guiObj.buildTableWithImage(2, 3, table, item[4])
                    return
            self.guiObj.errorMessage('You search for :'+str(textdata))
            self.textToSpeech('Sorry some problem occur, please ask again.')        
            return

        if 'dean' in textdata:
            print('Search for dean') 
            for item in self.aboutCollege:
                if 'dean' == item[0]:
                    table = [['Image','Name','Designation'],['',item[1],'dean of college']]
                    self.guiObj.buildTableWithImage(2, 3, table, item[4])
                    return
            self.guiObj.errorMessage('You search for :'+str(textdata))
            self.textToSpeech('Sorry some problem occur, please ask again.')        
            return

        if 'chancellor' in textdata:
            print('Search for chancellor') 
            for item in self.aboutCollege:
                if 'chancellor' == item[0]:
                    table = [['Image','Name','Designation'],['',item[1],'Chancellor of College']]
                    self.guiObj.buildTableWithImage(2, 3, table, item[4])
                    return
            self.guiObj.errorMessage('You search for :'+str(textdata))
            self.textToSpeech('Sorry some problem occur, please ask again.')        
            return

    def confirmMeeting(self,name,cabin):
        self.textToSpeech('Thank you for waiting, notification send to'+name)
        self.guiObj.buildTable(2, 2, [['Details','Meeting Place'],['Your meeting is confirm\n',cabin]])

    def fetchPersonData(self):
        self.personDetails = self.fetchAllData('person')
        self.higherAuthList = self.fetchAllData('higherauth')    
        self.aboutCollege = self.fetchAllData('aboutCollege')


    def textToSpeech(self,textdata):
        tts = gTTS(text=textdata, lang='en-us')
        tts.save("hello.mp3")
        os.system('mpg123 hello.mp3')


    def captureVoice(self):
        with sr.Microphone(chunk_size=4096) as source:
            print("Say something!")
            try:
                with open('/home/swati/Documents/Project/FinalYProject/image/shortmessagefile.txt','r') as file:
                    processno = file.readline()
                os.system('kill '+processno)
            except:
                pass
            with open('/home/swati/Documents/Project/FinalYProject/image/shortmessagefile.txt','r') as file:
                processno = file.readline()
            os.system('kill '+processno)
            os.system('nohup python3 showshortmessage.py listening &')
            self.r.adjust_for_ambient_noise(source,1)
            audio = self.r.listen(source)   
            os.system('nohup play /home/swati/Documents/Project/FinalYProject/Notification/ting.mp3 &')
            with open('/home/swati/Documents/Project/FinalYProject/image/shortmessagefile.txt','r') as file:
                processno = file.readline()
            os.system('kill '+processno)
            os.system('nohup python3 showshortmessage.py processing &')
            print('Wait..')     
            try:
                return self.r.recognize_google(audio,language='en-GB')
            except:
                return None 

    def sendMail(self,toaddr,data):
        try:
            fromaddr = "project15email@gmail.com"          
            # instance of MIMEMultipart
            msg = MIMEMultipart()
             
            # storing the senders email address  
            msg['From'] = fromaddr
             
            # storing the receivers email address 
            msg['To'] = toaddr
             
            # storing the subject 
            msg['Subject'] = "Project 15 notification"
             
            # string to store the body of the mail
            body = data
             
            attachment = open('/home/swati/Documents/Project/FinalYProject/image/visitor.jpg')
            image=MIMEImage(attachment.read())
            attachment.close() 

            # attach the body with the msg instance
            msg.attach(MIMEText(body, 'plain'))
            msg.attach(image)
             
            # creates SMTP session
            s = smtplib.SMTP('smtp.gmail.com', 587)
             
            # start TLS for security
            s.starttls()
             
            # Authentication
            s.login(fromaddr, "Project_15")
             
            # Converts the Multipart msg into a string
            text = msg.as_string()
             
            # sending the mail
            s.sendmail(fromaddr, toaddr, text)
             
            # terminating the session
            s.quit()                 
        except:
            # raise
            print('Error occur while sending mail.')     


class VoiceInteraction(object):

    def __init__(self):
        self.r = sr.Recognizer()
        self.r.operation_timeout=5

    def captureVoice(self):
    	with sr.Microphone(chunk_size=4096) as source:
            print("Say something!")
            try:
                with open('/home/swati/Documents/Project/FinalYProject/image/shortmessagefile.txt','r') as file:
                    processno = file.readline()
                os.system('kill '+processno)
            except:
            	pass    

            os.system('nohup python3 showshortmessage.py listening &')
            self.r.adjust_for_ambient_noise(source,1)
            audio = self.r.listen(source)   
            os.system('nohup play /home/swati/Documents/Project/FinalYProject/Notification/ting.mp3 &')
            with open('/home/swati/Documents/Project/FinalYProject/image/shortmessagefile.txt','r') as file:
                processno = file.readline()
            os.system('kill '+processno)
            os.system('nohup python3 showshortmessage.py processing &')
            print('Bye')
            try:
                return self.r.recognize_google(audio,language='en-GB')
            except:
            	return None

#-----------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------#


if __name__ == "__main__":
    os.system("nohup eog -f '/home/swati/Documents/Project/FinalYProject/image/wave.gif' &")
    time.sleep(7)
    voiceObject = VoiceInteraction()        
    textObject  = ProcessText()
    textObject.fetchPersonData()
    os.system('nohup python3 InstructionToUse.py &')
    while True:
        speechToText = ""
        try:
            while not ((("program" in speechToText.split(" "))) or ("active" in speechToText.split(" ") or "activate" in speechToText.split(" ")) or ("thank" in speechToText.split(" ") or "thanks" in speechToText.split(" ")) ):
                speechToText = voiceObject.captureVoice()
                if speechToText is not None:
                    if not ("activate" in speechToText.split(" ")):
                        print('You said : '+speechToText)
                        print('')
                        textObject.processData(speechToText)
                else: 
                    print('Unable to understand.')  
                    speechToText = ""
        except:
            print('Activation Error')
            raise
            break
            pass

        if ("thank" in speechToText.split(" ") or "thanks" in speechToText.split(" ")):
            break

        textObject.textToSpeech('Program is activated.Please wait for verification of image.')
        os.system('python3 VerifyImage.py')
        textObject.textToSpeech('Image verification is successfull.')
        
        os.system('nohup python3 ShowProfile.py &')
        speechToText = ""
        textObject.textToSpeech("Welcome User, How may i help you? Please Speak after notification tone.")
        os.system('nohup play /home/swati/Documents/Project/FinalYProject/Notification/end.mp3 &')    
        
        speechToText = ""        
        while not ("thank" in speechToText.split(" ") or "thanks" in speechToText.split(" ")):
            speechToText = voiceObject.captureVoice()
            if speechToText is not None:
                if not ("thanks" in speechToText.split(" ") or "thank" in speechToText.split(" ")):
                    print('You said : '+speechToText)
                    print('')
                    textObject.processData(speechToText)
            else: 
                print('Unable to understand.')  
                speechToText = ""
            os.system('nohup play /home/swati/Documents/Project/FinalYProject/Notification/end.mp3 &')
        processno = ""    
        with open('/home/swati/Documents/Project/FinalYProject/image/processnumber.txt','r') as file:
            processno = file.readline()
        os.system('kill '+processno)
    os.system('pkill eog')
    with open('/home/swati/Documents/Project/FinalYProject/image/processnumbera.txt','r') as file:
        processno = file.readline()
    os.system('kill '+processno)
    with open('/home/swati/Documents/Project/FinalYProject/image/shortmessagefile.txt','r') as file:
        processno = file.readline()
    os.system('kill '+processno) 
        # os.system('pkill python')
