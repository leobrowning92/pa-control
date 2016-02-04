"""
Tkinter app for running the pa download, cleandata and PAplot scripts
from a simple GUI
"""

from Tkinter import Tk, Text, BOTH, W, N, E, S, RAISED, StringVar, Menu
from ttk import Frame, Button, Label, Style, Entry
import tkFileDialog


class PAGUI(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Parameter Analyzer Control")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        self.path=StringVar()
        self.fname=StringVar()



        self.lbl1 = Label(self, text="Dummy label at the top of the widget",
                     justify="center")
        self.lbl1.grid(column=1, sticky=W, pady=4, padx=5)

        self.lbl2 = Label(self, text='path/to/save/to/file',
                     justify="center", font="arial 11 italic")
        self.lbl2.grid(column=1, row=3, columnspan=2,
                  sticky=N + E + W, pady=4, padx=5)

        self.lbl3 = Label(self, text="Save Path : ",
                     justify="right")
        self.lbl3.grid(column=0,row=3, sticky=N+E, pady=4, padx=5)

        self.entry1 = Entry(self,textvariable=self.path)
        self.entry1.grid(row=1, column=1, columnspan=2,
                    padx=5, sticky=E + W)

        self.entry2 = Entry(self,textvariable=self.fname)
        self.entry2.grid(row=2, column=1, columnspan=2,
                    padx=5, sticky=E + W)

        abtn = Button(self, text="Directory",command=self.askdirectory)
        abtn.grid(row=1, column=0)

        cbtn = Button(self, text="Filename",command=self.askfile)
        cbtn.grid(row=2, column=0)

        hbtn = Button(self, text="Exit",command=self.quit)
        hbtn.grid(row=5, column=0, padx=5)

        obtn = Button(self, text="Update",command= self.runClick)
        obtn.grid(row=3, column=3,sticky= N)

    def runClick(self):
        self.lbl2.config(text=(self.entry1.get()+'/'+self.entry2.get()))

    def askdirectory(self):
        """Returns a selected directoryname."""
        self.entry1.insert(0,tkFileDialog.askdirectory())
    def askfile(self):
        self.entry2.insert(0,tkFileDialog.askopenfilename())
def main():
    root = Tk()
    root.geometry("800x200+300+300")
    app = PAGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
