from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QFileDialog
from guiResources import Ui_Form
import sys
from start import Start
from setup import Options
import os
import glob
import ast

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_Form()
        self.central_widget = QtWidgets.QWidget()
        self.ui.setupUi(self.central_widget)
        self.setCentralWidget(self.central_widget)
        self.ui.pushButtonFile.clicked.connect(self.open_file_dialog)
        self.ui.pushButtonFolder.clicked.connect(self.open_folder_dialog)
        self.ui.pushButtonCheck.clicked.connect(self.check_file)
        options = Options()
        options.loadCachedOptions()
        self.ui.radioButtonGptZero.setChecked(options.toggleUndetectableAI)
        self.ui.radioButtonGrammica.setChecked(options.toggleGrammica)
        self.ui.radioButtonWritefull.setChecked(options.toggleWritefull)
        self.ui.radioButtonHive.setChecked(options.toggleHive)
        self.ui.radioButtonScribbr.setChecked(options.toggleScribbr)
        self.ui.radioButtonTypeset.setChecked(options.toggleTypeset)
    
    def open_file_dialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*);;PDF Files (*.pdf);;Text Files (*.txt)")
        if fileName:
            fileNameEx = fileName
            self.files_to_check = [fileNameEx]
            self.ui.plainTextEdit.setPlainText(str(self.files_to_check))
    
    def open_folder_dialog(self):
        folderName = QFileDialog.getExistingDirectory(self, "QFileDialog.getExistingDirectory()", "", QFileDialog.Option.ShowDirsOnly)
        if folderName:
            self.folders_to_check = glob.glob(rf"{folderName}/*.[tp][xd][ft]")
            self.ui.plainTextEdit.setPlainText(str(self.folders_to_check))

    def check_file(self):
        text = self.ui.plainTextEdit.toPlainText()
        try:
            paths = ast.literal_eval(text)  # parse string into list

            valid_paths = [path for path in paths if os.path.exists(path)]

            if valid_paths:
                checkingFiles = valid_paths
            else:
                with open("temp.txt", "w") as temp_file:
                    temp_file.write(text)
                checkingFiles = ["temp.txt"]
        except:
            with open("temp.txt", "w") as temp_file:
                temp_file.write(text)
            checkingFiles = ["temp.txt"]

        self.buttonStates = []
        for x in [self.ui.radioButtonGptZero, self.ui.radioButtonGrammica, self.ui.radioButtonWritefull, self.ui.radioButtonHive, self.ui.radioButtonScribbr, self.ui.radioButtonTypeset]:
            self.buttonStates.append(x.isChecked())
        start = Start(self)
        start.begin(checkingFiles)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())