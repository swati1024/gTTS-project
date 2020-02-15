from tkinter import *
from PIL import Image,ImageTk

class BuildGui(object):
	def __init__(self):
		pass

	def showProfile(self):
		root = Tk()
		root.title('Current User Session')
		root.geometry("%dx%d+%d+%d" % (270,270, 1000, 20))
		image = Image.open('/home/swati/Documents/Project/FinalYProject/image/visitor.jpg')
		image = image.resize((250,200))
		photo = ImageTk.PhotoImage(image)
	
		b = Label(root,image=photo)
		b.image = photo
		b.grid(row=1,column=0,padx=10, pady=10)
		message = "Welcome User"
		b = Label(root,text=message,anchor=CENTER,font=("Helvetica", 11))
		b.grid(row=2,column=0,padx=10, pady=10)
		root.mainloop()

	def showShortMessage(self,msg): 
		frame = Tk()
		frame.title('Status')
		x = (frame.winfo_screenwidth() - frame.winfo_reqwidth()) / 2
		y = (frame.winfo_screenheight() - frame.winfo_reqheight()) / 2
		frame.geometry("%dx%d+%d+%d" % (150, 50, x-280, y-90))
		label = Label(frame,text=msg,anchor=CENTER,font=("Helvetica", 10))
		label.grid(row=0,column=0,padx=10, pady=10)
		frame.mainloop()

	def buildInstructionTable(self,irow,jcol,data):
		root = Tk()
		root.title('Instruction Table')
		# root.geometry("250x500")
		root.geometry('%dx%d+%d+%d' % (250, 600, 50, 10))
		labelframe = LabelFrame(root, text="Instruction for use")
		labelframe.pack(fill="both", expand="yes")

		for i in range(irow):
			for j in range(jcol):
				b = Label(labelframe,text=data[i][j],wraplength=240,justify=LEFT,anchor=NW,font=("Helvetica", 13))
				b.grid(row=i,column=j)				
		root.mainloop()	

	def buildTable(self,irow,jcol,data):
		root = Tk()
		root.title('Auto close in 5 seconds')
		root.after(5000, lambda: root.destroy())
		x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
		y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
		root.geometry("+%d+%d" % (x-300, y-100))

		for i in range(irow):
			for j in range(jcol):
				b = Label(root,text=data[i][j],anchor=CENTER,font=("Helvetica", 11))
				b.grid(row=i,column=j,padx=10, pady=10)				
		root.mainloop()

	def buildTableWithImage(self,irow,jcol,data,imageurl):
		root = Tk()
		root.title('Auto close in 5 seconds')
		root.after(5000, lambda: root.destroy())
		x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
		y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
		root.geometry("+%d+%d" % (x-300, y-100))
		image = Image.open(imageurl)
		image = image.resize((250,200))
		photo = ImageTk.PhotoImage(image)
		
		b = Label(root,image=photo)
		b.image = photo
		b.grid(row=1,column=0,padx=10, pady=10)

		for i in range(irow):
			for j in range(jcol):
				if i==1 and j==0:
					pass
				else:	
					b = Label(root,text=data[i][j],anchor=CENTER,font=("Helvetica", 11))
					b.grid(row=i,column=j,padx=10, pady=10)				
		root.mainloop()				

	def errorMessage(self,msg):
	    frame = Tk()
	    frame.title('Error, Auto close in 2 seconds')
	    frame.after(2000, lambda: frame.destroy())
	    x = (frame.winfo_screenwidth() - frame.winfo_reqwidth()) / 2
	    y = (frame.winfo_screenheight() - frame.winfo_reqheight()) / 2
	    frame.geometry("+%d+%d" % (x-300, y-100))
	    label = Label(frame,text=msg,anchor=CENTER,font=("Helvetica", 10))
	    label.grid(row=0,column=0,padx=10, pady=10)
	    frame.mainloop()


if __name__ == '__main__':
	guiObj = BuildGui()
	# guiObj.errorMessage('error')
	data = [['Image','Name','Designation'],['','Swati','Chancellor']]
	guiObj.buildTableWithImage(2,3, data, '/home/swati/Documents/Project/FinalYProject/image/chancellor.jpg')
