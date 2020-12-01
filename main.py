from pyquery import PyQuery
from PyQt5 import QtWidgets, uic,QtGui,QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QFontDialog,QFileDialog
import os,sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('interface.ui', self)
        self.file_path = ""
        self.filename = ""
        self.text_changed_counter = 0
        self.Menu_connect()
        self.show()

    def Menu_connect(self):
        self.actionChange_font.triggered.connect(self.Open_Font_Dialog)
        self.actionOPen.triggered.connect(self.Open_File_Dialog)
        self.actionSave_as.triggered.connect(self.Save_File_Dialog)
        self.actionSave.triggered.connect(self.Save_File)
        self.actionNew.triggered.connect(self.New_File)
        self.actionExit.triggered.connect(self.close)
        self.actionStatus_bar.triggered.connect(self.Show_Hide_Sbar)
        self.actionZoom.triggered.connect(self.textEdit.zoomIn)
        self.actionZoom_0.triggered.connect(self.textEdit.zoomOut)

        self.textEdit.cursorPositionChanged.connect(self.Status_Bar_Handler)
        self.textEdit.textChanged.connect(self.Text_Changed)

    def wheelEvent(self,event):
        if event.angleDelta().y() > 0:
            self.textEdit.zoomIn()
        else:
            self.textEdit.zoomOut()

    def Text_Changed(self):
        if self.filename != "":
            self.setWindowTitle(self.filename+"*")
        else:
            self.setWindowTitle("New File*")
        self.text_changed_counter += 1
            
    def Status_Bar_Handler(self):
        try:
            cursor = self.textEdit.textCursor()
            y = cursor.blockNumber() + 1
            x = cursor.columnNumber() + 1
            if self.filename != "":                
                self.statusbar.showMessage("{filename1} | {cur1}:{cur2}x{cur3} |".format(filename1=self.file_path,
                                                                                         cur1="Cursor",
                                                                                         cur2=y,
                                                                                         cur3=x))
                self.setWindowTitle(self.filename)
            else:
                self.statusbar.showMessage("{filename1} | {cur1}:{cur2}x{cur3} |".format(filename1="New File",
                                                                                         cur1="Cursor",
                                                                                         cur2=y,
                                                                                         cur3=x))
        except Exception as ex:
            print(ex)

    def Show_Hide_Sbar(self, state):
        if self.statusbar.isVisible():
            self.statusbar.hide()
        else:
            self.statusbar.show()

    def New_File(self):
        if self.text_changed_counter > 0:
            self.Save_File_Dialog()
        self.filename = ""
        self.file_path = ""
        self.setWindowTitle("New File")
        self.textEdit.setText("")
        self.text_changed_counter = 0
        
    def Save_File(self):
        if self.filename != "":
            open(self.file_path,mode="w",encoding="UTF-8").write(self.textEdit.toPlainText())
            self.setWindowTitle(self.filename)
        else:
            self.Save_File_Dialog()
    
    def Save_File_Dialog(self):
        filename, ok = QFileDialog.getSaveFileName(caption="Save File",directory=self.filename)
        if ok:
            open(filename,mode="w",encoding="UTF-8").write(self.textEdit.toPlainText())
            self.file_path = filename
            self.filename = self.file_path[self.file_path.rfind("/")+1:]
            self.setWindowTitle(self.filename)
        
    def Open_Font_Dialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            print(self.textEdit.setFont(font))

    def Open_File_Dialog(self):
        filename, ok = QFileDialog.getOpenFileName(caption="Select File")
        if ok:
            self.file_path = filename
            self.filename = self.file_path[self.file_path.rfind("/")+1:]
            self.textEdit.setText(open(self.file_path,"r",encoding="UTF-8").read())
            self.Status_Bar_Handler()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
