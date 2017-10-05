import thread, Queue, Main
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkFileDialog import askopenfilename

def statusConsole(text):
	try:
		data = dataQueue.get(block=False)
	except Queue.Empty:
		pass
	else:
		text.config(state=NORMAL)
		
		if "%" in str(data):
			text.insert(END,'%s\n' % str(data), "highlight")
		else:
			text.insert(END,'%s\n' % str(data))
			
		text.see(END)
		text.config(state=DISABLED)
		text.tag_configure("highlight", foreground="green")
	text.after(250, lambda: statusConsole(text))

def chooseButtonCallback(path):
	finalFilePath.config(state=NORMAL)
	finalFilePath.delete(0,END)
	finalFilePath.insert(0,path.get())
	finalFilePath.config(state=DISABLED, disabledforeground="green")

def browseButtonCallback():
	filename= askopenfilename()
	tmpFilePath.delete(0,END)
	tmpFilePath.insert(0,filename)

def goButtonCallBack(path, root):
	thread.start_new_thread(Main.main, (dataQueue, root))


#Some preparation---------------------------------------------------------------
matplotlib.use("TkAgg")
#-------------------------------------------------------------------------------

#Font constants-----------------------------------------------------------------
font = "Comic Sans MS"
bg = "gray"
#-------------------------------------------------------------------------------

#Defining the GUI and window name and label-------------------------------------
top = Tk()
top.geometry('{}x{}'.format(1000,500))
top.configure(background=bg)
top.title("MAMA")

label = Label(top, text="(M)LS (A)dvanced (M)odule (A)ssigner", bg=bg, font=(font, 16))
label.place(x=10, y=10)
#-------------------------------------------------------------------------------

#Buttons and Entries for the source File----------------------------------------
tmpFilePath = Entry(top, width = 50)
tmpFilePath.focus_set()
tmpFilePath.place(x=10, y=90)
tmpFilePath.insert(0,"e.g. /home/filename.csv")

finalFilePath = Entry(top, width = 50)
finalFilePath.place(x=10, y=180)
finalFilePath.insert(0,tmpFilePath.get())
finalFilePath.config(state=DISABLED, disabledforeground="green")

BrowseButton = Button(top, text = "Browse", width=10, command=lambda: browseButtonCallback(), activebackground="blue")
BrowseButton.place(x=10, y=130)

ChooseButton = Button(top, text = "Choose", width=10, command=lambda: chooseButtonCallback(tmpFilePath), activebackground="blue")
ChooseButton.place(x=140, y=130)
#-------------------------------------------------------------------------------

#GO button and output-----------------------------------------------------------
GoButton = Button(top, text = "Start Optimization", width = 15, command = lambda: goButtonCallBack(finalFilePath.get(), top), activebackground="green")
GoButton.place(x=270, y=130)

#Text Widget for output from console (gets stored in queue)---------------------
dataQueue = Queue.Queue()
console = Text(top, width=57, height=17)
console.place(x=10, y=220)
statusConsole(console)
#-------------------------------------------------------------------------------

#Create figure for visual output------------------------------------------------
f = Figure(figsize=(6,5), dpi=100)
f.set_facecolor(bg)
a = f.add_subplot(221)#, axisbg=bg)
b = f.add_subplot(223)
c = f.add_subplot(122)


canvas = FigureCanvasTkAgg(f, master=top)
canvas.get_tk_widget().place(x=420, y=0)#side=BOTTOM, fill=BOTH, expand=True)
canvas.show()


top.mainloop()
