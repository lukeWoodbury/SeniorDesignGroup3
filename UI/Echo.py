__doc__ = info = '''
'''

from Tkinter import *
from tkFileDialog import *
from PIL import Image


#Open directory
def openfile():

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
	root.maxsize(width=1000, height=650)
	root.resizable(0,0)
	def hello():
		print "hello!"
	def loadDir():
		directory = tkFileDialog.askopenfilename(parent=root)


#*****************************************************************MenuBar****************************************************************
	menubar = Menu(root)



	# create a pulldown menu, and add it to the menu bar
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="Open", command=openfile)
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
	Label(tab1, text="Number of epochs").pack() 
	txt = Text(tab1).pack()
	Button(tab1, text="save changes", command=(lambda: bar.delete("Train"))).pack()

#*****************************************************************TAB2****************************************************************
	tab2 = Tab(root, "Predict")

	txt = Text(tab2, width=666, height=666)
	txt.focus()
	txt.pack(side=LEFT, fill=X, expand=YES)

#*****************************************************************TAB3****************************************************************
	tab3 = Tab(root, "Analze")
	txt = Text(tab3, width=666, height=666)
	txt.focus()
	txt.pack(side=LEFT, fill=X, expand=YES)

#*****************************************************************TAB4****************************************************************
	tab4 = Tab(root, "Info")
	
	
	listbox = Listbox(tab4)
	listbox.pack(side=LEFT, fill =Y)

	listbox.insert(END, "a list entry")
	#logic for selecting and switching graphs
	listbox.bind("<<ListboxSelect>>", onselect)
	img2 = PhotoImage(file='age_acc.png')
	
	imglabel = Label(tab4, image = img2).pack(side=LEFT)


	for item in ["age_loss", "two", "three", "four"]:
		listbox.insert(END, item)



	bar.add(tab1)                   # add the tabs to the tab bar
	bar.add(tab2)
	bar.add(tab3)
	bar.add(tab4)

	bar.config(bd=2, relief=RIDGE)			# add some border
	
	bar.show()
	
	root.mainloop()

