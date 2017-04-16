__doc__ = info = '''
'''

from Tkinter import *
from tkFileDialog import *
from PIL import Image


#Open directory
def openFile():

   filename = askopenfile(parent=root)
   f = open(filename)
   f.read()
#Open directory
def openDirectory():

   filename = askdirectory(parent=root)
   f = open(filename)
   f.read()
#switch between graphs
def onselect(evt):
    	# Note here that Tkinter passes an event object to onselect()
		w = evt.widget
		index = int(w.curselection()[0])
		value = w.get(index)
		value2 = (value + ".gif")
		
		img = PhotoImage(file = value2)
		
		#imglabel.configure(image=img)
		#imglabel.image = img
		imglabel = Label(tab3, image = img)
		imglabel.image = img
		imglabel.grid(row=0,column=1)
		print ''+ value2

BASE = RAISED
SELECTED = FLAT




# a base tab class
class Tab(Frame):
	def __init__(self, master, name):
		Frame.__init__(self, master)
		self.tab_name = name

# the bulk of the logic is in the actual tab bar
class TabBar(Frame):
	def __init__(self, master=None, init_name=None):
		Frame.__init__(self, master)
		self.tabs = {}
		self.buttons = {}
		self.current_tab = None
		self.init_name = init_name
	
	def show(self):
		self.pack(side=TOP, expand=NO, fill=X)
		self.switch_tab(self.init_name or self.tabs.keys()[-1])# switch the tab to the first tab
	
	def add(self, tab):
		tab.pack_forget()									# hide the tab on init
		
		self.tabs[tab.tab_name] = tab						# add it to the list of tabs
		b = Button(self, text=tab.tab_name, relief=BASE,	# basic button stuff
			command=(lambda name=tab.tab_name: self.switch_tab(name)))	# set the command to switch tabs
		b.pack(side=LEFT)												# pack the buttont to the left mose of self
		self.buttons[tab.tab_name] = b											# add it to the list of buttons
	
	def delete(self, tabname):
		
		if tabname == self.current_tab:
			self.current_tab = None
			self.tabs[tabname].pack_forget()
			del self.tabs[tabname]
			self.switch_tab(self.tabs.keys()[0])
		
		else: del self.tabs[tabname]
		
		self.buttons[tabname].pack_forget()
		del self.buttons[tabname] 
		
	
	def switch_tab(self, name):
		if self.current_tab:
			self.buttons[self.current_tab].config(relief=BASE)
			self.tabs[self.current_tab].pack_forget()			# hide the current tab
		self.tabs[name].pack(side=BOTTOM)							# add the new tab to the display
		self.current_tab = name									# set the current tab to itself
		
		self.buttons[name].config(relief=SELECTED)					# set it to the selected style
	

#*****************************************************************MainWindow****************************************************************
			
if __name__ == '__main__':
	def write(x): print x

	root = Tk()
	root.title("Tabs")
	root.minsize(width=1000, height=650)
	root.maxsize(width=1500, height=650)
	root.resizable(0,0)
	img2 = PhotoImage(file='age_acc.gif') 	
	def hello():
		print "hello!"
	def loadDir():
		directory = tkFileDialog.askopenfilename(parent=root)


#*****************************************************************MenuBar****************************************************************
	menubar = Menu(root)



	# create a pulldown menu, and add it to the menu bar
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="Open", command=openDirectory)
	filemenu.add_command(label="Save", command=hello)
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=root.quit)
	menubar.add_cascade(label="File", menu=filemenu)

	# create more pulldown menus
	editmenu = Menu(menubar, tearoff=0)
	editmenu.add_command(label="Cut", command=hello)
	editmenu.add_command(label="Copy", command=hello)
	editmenu.add_command(label="Paste", command=hello)
	menubar.add_cascade(label="Edit", menu=editmenu)

	helpmenu = Menu(menubar, tearoff=0)
	helpmenu.add_command(label="About", command=hello)
	menubar.add_cascade(label="Help", menu=helpmenu)

	# display the menu
	root.config(menu=menubar)
	
	bar = TabBar(root, "Info")
	
#*****************************************************************TAB1****************************************************************
	tab1 = Tab(root, "Train")				# notice how this one's master is the root instead of the bar
	var= IntVar()
	weights = Checkbutton(tab1, text='Use Weights', variable=var).grid(row=0)
	Label(tab1, text="Number of epochs").grid(row=1)
	txt = Text(tab1, width = 10, height = 5).grid(row=1, column=1)
	Label(tab1, text="learning rate").grid(row=2)
	txt = Text(tab1, width = 10, height = 5).grid(row=2, column=1)
	Label(tab1, text="loss weights").grid(row=3)
	txt = Text(tab1, width = 10, height = 5).grid(row=3, column=1)
	Label(tab1, text="optimizer").grid(row=4)
	lst1 = ['1','2','3']
	var1 = StringVar()
	drop = OptionMenu(tab1, var1, *lst1).grid(row=4, column=1)
	txt = Text(tab1, width = 10, height = 5).grid(row=2, column=1)
	Label(tab1, text="batch size").grid(row=5)
	Button(tab1, text="save changes", command=hello).grid(row=6)

#*****************************************************************TAB2****************************************************************
	tab2 = Tab(root, "Predict")

	Label(tab1, text="File for Prediction").grid(row=1)
	txt = Text(tab2, width = 10, height = 5).grid(row=1, column=1)
	Button(tab2, text="Choose file", command=openFile).grid(row=1,column=2)
	Button(tab2, text="predict", command=hello).grid(row=10,column=2)

#*****************************************************************TAB3****************************************************************
	tab3 = Tab(root, "Analze")
	listbox = Listbox(tab3)
	listbox.grid(row=0, column = 0)

	listbox.insert(END, "age_acc")
	#logic for selecting and switching graphs
	listbox.bind("<<ListboxSelect>>", onselect)
	
	
	imglabel = Label(tab3, image = img2).grid(row=0,column = 1)


	for item in ["age_loss", "gender_acc", "gender_loss"]:
		listbox.insert(END, item)

#*****************************************************************TAB4****************************************************************
	tab4 = Tab(root, "Info")
	
	




	bar.add(tab1)                   # add the tabs to the tab bar
	bar.add(tab2)
	bar.add(tab3)
	bar.add(tab4)

	bar.config(bd=2, relief=RIDGE)			# add some border
	
	bar.show()
	
	root.mainloop()

