from pythongui import BuildGui
import sys
import os

if __name__ == '__main__':
	with open('/home/swati/Documents/Project/FinalYProject/image/shortmessagefile.txt','w') as file:
		file.write(str(os.getpid()))
	if len(sys.argv)>1:
		s = 'Listening'
		guiObj = BuildGui()
		msg = '     '+sys.argv[1]
		guiObj.showShortMessage(msg)
	else:
		print('Please Pass Argument')	
