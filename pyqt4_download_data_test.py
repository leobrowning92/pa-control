"""
ZetCode PyQt4 tutorial

In this example, we receive data from
a QtGui.QInputDialog dialog.

author: Jan Bodnar
website: zetcode.com
last edited: October 2011
"""

import sys
from PyQt4 import QtGui

class Main(QtGui.QMainWindow):
    """Handles the main window which includes toolbars, menues and the
    central widget which has all the buttons and such"""
    def __init__(self):
        super(Main, self).__init__()

        self.initUI()


    def initUI(self):

        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        self.sb =self.statusBar()
        self.sb.showMessage('Ready')

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.widgets=widgets()
        self.setCentralWidget(self.widgets)

        self.setGeometry(300, 300, 500, 100)
        self.setWindowTitle('Main')
        self.show()
    def setStatusBar(self,string):
        self.sb.showMessage(string)

class widgets(QtGui.QWidget):
    """has all the widgets needed in a grid"""

    def __init__(self):
        super(widgets, self).__init__()

        self.initUI()

    def initUI(self):


        grid =QtGui.QGridLayout()
        self.setLayout(grid)

        self.btn = QtGui.QPushButton('path', self)
        grid.addWidget(self.btn,0,0)
        self.btn.clicked.connect(self.fileDialog)

        self.le = QtGui.QLineEdit(self)
        grid.addWidget(self.le,0,1)

    def fileDialog(self):

        path= QtGui.QFileDialog.getExistingDirectory(self, 'Open file',
                '/home')
        ex.setStatusBar("Save directory : "+path)
        print(path)


    def showDialog(self):

        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog',
            'Enter your name:')

        if ok:
            self.le.setText(str(text)) #sets text in line edit
        print(self.le.text()) ##prints the text in a line edit



app = QtGui.QApplication(sys.argv)
ex = Main()
sys.exit(app.exec_())



