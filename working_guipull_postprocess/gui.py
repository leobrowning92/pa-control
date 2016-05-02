"""
Tkinter app for running the pa download, cleandata and PAplot scripts
from a simple GUI
"""

from Tkinter import Tk, Text, BOTH, W, N, E, S, RAISED, StringVar, Menu, Radiobutton, IntVar
from ttk import Frame, Button, Label, Style, Entry
import tkFileDialog

import nameIterator
import download_pa
# import cleandata


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

        self.path = StringVar()
        self.fname = StringVar()

        self.lbl1 = Label(self, text="Dummy label at the top of the widget",
                          justify="center")
        self.lbl1.grid(column=1, sticky=W, pady=4, padx=5)

        self.lbl2 = Label(self, text='path/to/save/to/file',
                          justify="center", font="arial 11 italic")
        self.lbl2.grid(column=1, row=3, columnspan=2,
                       sticky=N + E + W, pady=4, padx=5)

        self.lbl3 = Label(self, text="Save Path : ",
                          justify="right")
        self.lbl3.grid(column=0, row=3, sticky=N + E, pady=4, padx=5)

        self.entry1 = Entry(self, textvariable=self.path)
        self.entry1.grid(row=1, column=1, columnspan=2,
                         padx=5, sticky=E + W)

        self.entry2 = Entry(self, textvariable=self.fname)
        self.entry2.grid(row=2, column=1, columnspan=2,
                         padx=5, sticky=E + W)

        self.abtn = Button(self, text="Directory", command=self.askdirectory)
        self.abtn.grid(row=1, column=0)

        self.cbtn = Button(self, text="Filename", command=self.askfile)
        self.cbtn.grid(row=2, column=0)

        self.hbtn = Button(self, text="Exit", command=self.quit)
        self.hbtn.grid(row=5, column=0, padx=5)

        self.obtn = Button(self, text="Update", command=self.runClick)
        self.obtn.grid(row=3, column=3, sticky=N)

        self.obtn = Button(self, text="New Chip", command=self.newChip)
        self.obtn.grid(row=1, column=3, sticky=N)

        self.obtn = Button(self, text="New Device", command=self.newDevice)
        self.obtn.grid(row=2, column=3, sticky=N)

        # this button runs pulldata with parameter set by
        # self.v, which stores the value of self.radbtn
        self.hbtn = Button(self, text="Pull Data", command=self.pulldata)
        self.hbtn.grid(row=5, column=3, padx=5)

        self.v = IntVar()
        self.radbtn = Radiobutton(
            self, text='Diode (VF, IF)', variable=self.v, value=1)
        self.radbtn.grid(row=5, column=1, padx=5, sticky=N + E)

        self.radbtn = Radiobutton(
            self, text='FET (VG, VDS, ID, IG)', variable=self.v, value=2)
        self.radbtn.grid(row=5, column=2, padx=5, sticky=N + E)

    def newChip(self):
        if self.entry2.get() == '':
            self.askfile()

        else:
            try:
                newname = nameIterator.iterateChip(self.entry2.get())
            except:
                self.lbl2.config(text="ERROR filename not compatible")

            self.entry2.delete(0, 'end')
            self.entry2.insert(0, newname)

    def newDevice(self):
        if self.entry2.get() == '':
            self.askfile()
        else:
            try:
                newname = nameIterator.iterateDevice(self.entry2.get())
            except:
                self.lbl2.config(text="ERROR filename not compatible")
            self.entry2.delete(0, 'end')
            self.entry2.insert(0, newname)

    def runClick(self):
        self.lbl2.config(text=(self.entry1.get() + '/' + self.entry2.get()))

    def askdirectory(self):
        """Returns a selected directoryname."""
        self.entry1.delete(0, 'end')
        self.entry1.insert(0, tkFileDialog.askdirectory())

    def askfile(self):
        fullpath = tkFileDialog.askopenfilename()
        if "/" in fullpath:
            i = fullpath.rfind("/")
        if "\\" in fullpath:
            i = fullpath.rfind("\\")
        self.entry2.delete(0, 'end')
        self.entry2.insert(0, fullpath[i + 1:])

    def pulldata(self):
        if self.v.get() == 1:
            download_pa.download_data(path=self.entry1.get(
            ), filename=self.entry2.get(), values=['VF', 'IF'])
        elif self.v.get() == 2:
            download_pa.download_data(path=self.entry1.get(
            ), filename=self.entry2.get(), values=['VG', 'VDS', 'ID', 'IG'])
        print("\a") #adds a beep when data is finished pulling


def main():
    root = Tk()
    root.geometry("800x200+300+300")
    app = PAGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
