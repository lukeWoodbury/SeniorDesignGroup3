from Tkinter import *
from ttk import *


class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
        
    def initUI(self):
      
        self.parent.title("Ekko")
        self.style = Style()
        self.style.theme_use("default")

        self.pack(fill=BOTH, expand=1)

        frame0 =Frame(self)
        frame0.pack(fill=X)
        testButton = Button(frame0, text="test",
            command=self.quit)
        testButton.pack(side=LEFT, padx=5, pady=5)

        
        self.pack(fill=BOTH, expand=True)
        
        frame1 = Frame(self)
        frame1.pack(fill=X)
        
        lbl1 = Label(frame1, text="Birth Place", width=18)
        lbl1.pack(side=LEFT, padx=5, pady=5)           
       
        entry1 = Entry(frame1)
        entry1.pack(fill=X, padx=5, expand=True)
        
        frame2 = Frame(self)
        frame2.pack(fill=X)
        
        lbl2 = Label(frame2, text="Native Lagnuage", width=18)
        lbl2.pack(side=LEFT, padx=5, pady=5)        

        entry2 = Entry(frame2)
        entry2.pack(fill=X, padx=5, expand=True)
        
        frame3 = Frame(self)
        frame3.pack(fill=BOTH, expand=True)
        
        lbl3 = Label(frame3, text="age", width=18)
        lbl3.pack(side=LEFT, anchor=N, padx=5, pady=5)
        
        entry3 = Entry(frame3)
        entry3.pack(fill=X, padx=5, expand=True)        
   
        frame4 = Frame(self)
        frame4.pack(fill=X)
        
        lbl4 = Label(frame4, text="Sex", width=18)
        lbl4.pack(side=LEFT, padx=5, pady=5)           
       
        entry4 = Entry(frame4)
        entry4.pack(fill=X, padx=5, expand=True)
        
        frame5 = Frame(self)
        frame5.pack(fill=X)
        
        lbl5 = Label(frame5, text="age of onset", width=18)
        lbl5.pack(side=LEFT, padx=5, pady=5)        

        entry5 = Entry(frame5)
        entry5.pack(fill=X, padx=5, expand=True)
        
        frame6 = Frame(self)
        frame6.pack(fill=X)
        
        lbl6 = Label(frame6, text="learning method", width=18)
        lbl6.pack(side=LEFT, padx=5, pady=5)           
       
        entry6 = Entry(frame6)
        entry6.pack(fill=X, padx=5, expand=True)
        
        frame7 = Frame(self)
        frame7.pack(fill=X)
        
        lbl7 = Label(frame7, text="English Residence", width=18)
        lbl7.pack(side=LEFT, padx=5, pady=5)        

        entry7 = Entry(frame7)
        entry7.pack(fill=X, padx=5, expand=True)

        frame8 = Frame(self)
        frame8.pack(fill=BOTH, expand=True)
        
        lbl8 = Label(frame8, text="Length of Residence", width=18)
        lbl8.pack(side=LEFT, anchor=N, padx=5, pady=5)        

        txt = Text(frame8)
        txt.pack(fill=BOTH, pady=5, padx=5, expand=True)    



def main():
  
    root = Tk()

    root.geometry("450x260+300+300")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  

