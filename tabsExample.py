__doc__ = info = '''
'''

from Tkinter import *

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
		self.pack(side=TOP, expand=YES, fill=X)
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
			
if __name__ == '__main__':
	def write(x): print x
		
	root = Tk()
	root.title("Tabs")
	
	bar = TabBar(root, "Info")
	
	tab1 = Tab(root, "Train")				# notice how this one's master is the root instead of the bar
	txt = Text(tab1, width=50, height=20)
	txt.focus()
	txt.pack(side=LEFT, fill=X, expand=YES)
	
	
	tab2 = Tab(root, "Predict")
	txt = Text(tab2, width=50, height=20)
	txt.focus()
	txt.pack(side=LEFT, fill=X, expand=YES)

	tab3 = Tab(root, "Analze")
	txt = Text(tab3, width=50, height=20)
	txt.focus()
	txt.pack(side=LEFT, fill=X, expand=YES)

	tab4 = Tab(root, "Info")
	txt = Text(tab4, width=50, height=20)
	txt.focus()
	txt.pack(side=LEFT, fill=X, expand=YES)

	bar.add(tab1)                   # add the tabs to the tab bar
	bar.add(tab2)
	bar.add(tab3)
	bar.add(tab4)

	#bar.config(bd=2, relief=RIDGE)			# add some border
	
	bar.show()
	
	root.mainloop()
