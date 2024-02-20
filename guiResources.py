from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(470, 240)

        layout = QtWidgets.QGridLayout(Form)  # Create a new layout

        self.plainTextEdit = QtWidgets.QPlainTextEdit(parent=Form)
        layout.addWidget(self.plainTextEdit, 0, 0, 13, 2)  # Add widget to layout
                # Set the stretch factors
        layout.setRowStretch(0, 1)
        layout.setColumnStretch(0, 1)

        # Create a QPixmap, QPainter and QBrush to draw a circle
        pixmap = QtGui.QPixmap(20, 20)
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(pixmap)
        brush = QtGui.QBrush(QtCore.Qt.GlobalColor.gray)
        painter.setBrush(brush)
        painter.drawEllipse(0, 3, 15, 15)
        painter.end()

        # Add new QCheckBoxes
        self.radioButtonGptZero = QtWidgets.QCheckBox(parent=Form)
        layout.addWidget(self.radioButtonGptZero, 0, 4)  # Add widget to layout

        self.indicatorGptZero = QtWidgets.QLabel(parent=Form)
        self.indicatorGptZero.setPixmap(pixmap)
        layout.addWidget(self.indicatorGptZero, 0, 3)

        self.radioButtonOpenAi = QtWidgets.QCheckBox(parent=Form)
        layout.addWidget(self.radioButtonOpenAi, 1, 4)  # Add widget to layout

        self.indicatorOpenAi = QtWidgets.QLabel(parent=Form)
        self.indicatorOpenAi.setPixmap(pixmap)
        layout.addWidget(self.indicatorOpenAi, 1, 3)

        self.radioButtonWriter = QtWidgets.QCheckBox(parent=Form)
        layout.addWidget(self.radioButtonWriter, 2, 4)  # Add widget to layout

        self.indicatorWriter = QtWidgets.QLabel(parent=Form)
        self.indicatorWriter.setPixmap(pixmap)
        layout.addWidget(self.indicatorWriter, 2, 3)

        self.radioButtonCrossplag = QtWidgets.QCheckBox(parent=Form)
        layout.addWidget(self.radioButtonCrossplag, 3, 4)  # Add widget to layout

        self.indicatorCrossplag = QtWidgets.QLabel(parent=Form)
        self.indicatorCrossplag.setPixmap(pixmap)
        layout.addWidget(self.indicatorCrossplag, 3, 3)

        self.radioButtonCopyleaks = QtWidgets.QCheckBox(parent=Form)
        layout.addWidget(self.radioButtonCopyleaks, 4, 4)  # Add widget to layout

        self.indicatorCopyleaks = QtWidgets.QLabel(parent=Form)
        self.indicatorCopyleaks.setPixmap(pixmap)
        layout.addWidget(self.indicatorCopyleaks, 4, 3)

        self.radioButtonSapling = QtWidgets.QCheckBox(parent=Form)
        layout.addWidget(self.radioButtonSapling, 5, 4)  # Add widget to layout

        self.indicatorSapling = QtWidgets.QLabel(parent=Form)
        self.indicatorSapling.setPixmap(pixmap)
        layout.addWidget(self.indicatorSapling, 5, 3)

        self.radioButtonContentAtScale = QtWidgets.QCheckBox(parent=Form)
        layout.addWidget(self.radioButtonContentAtScale, 6, 4)  # Add widget to layout

        self.indicatorContentAtScale = QtWidgets.QLabel(parent=Form)
        self.indicatorContentAtScale.setPixmap(pixmap)
        layout.addWidget(self.indicatorContentAtScale, 6, 3)

        self.radioButtonZeroGpt = QtWidgets.QCheckBox(parent=Form)
        layout.addWidget(self.radioButtonZeroGpt, 7, 4)  # Add widget to layout

        self.indicatorZeroGpt = QtWidgets.QLabel(parent=Form)
        self.indicatorZeroGpt.setPixmap(pixmap)
        layout.addWidget(self.indicatorZeroGpt, 7, 3)

        self.radioButtonGrammica = QtWidgets.QCheckBox(parent=Form)
        layout.addWidget(self.radioButtonGrammica, 8, 4)  # Add widget to layout

        self.indicatorGrammica = QtWidgets.QLabel(parent=Form)
        self.indicatorGrammica.setPixmap(pixmap)
        layout.addWidget(self.indicatorGrammica, 8, 3)

        self.radioButtonWritefull = QtWidgets.QCheckBox(parent=Form)
        layout.addWidget(self.radioButtonWritefull, 9, 4)  # Add widget to layout

        self.indicatorWritefull = QtWidgets.QLabel(parent=Form)
        self.indicatorWritefull.setPixmap(pixmap)
        layout.addWidget(self.indicatorWritefull, 9, 3)

        self.radioButtonHive = QtWidgets.QCheckBox(parent=Form)
        layout.addWidget(self.radioButtonHive, 10, 4)  # Add widget to layout

        self.indicatorHive = QtWidgets.QLabel(parent=Form)
        self.indicatorHive.setPixmap(pixmap)
        layout.addWidget(self.indicatorHive, 10, 3)

        self.radioButtonScribbr = QtWidgets.QCheckBox(parent=Form)
        layout.addWidget(self.radioButtonScribbr, 11, 4)  # Add widget to layout

        self.indicatorScribbr = QtWidgets.QLabel(parent=Form)
        self.indicatorScribbr.setPixmap(pixmap)
        layout.addWidget(self.indicatorScribbr, 11, 3)

        self.radioButtonTypeset = QtWidgets.QCheckBox(parent=Form)
        layout.addWidget(self.radioButtonTypeset, 12, 4)  # Add widget to layout

        self.indicatorTypeset = QtWidgets.QLabel(parent=Form)
        self.indicatorTypeset.setPixmap(pixmap)
        layout.addWidget(self.indicatorTypeset, 12, 3)

        self.pushButtonCheck = QtWidgets.QPushButton(parent=Form)
        layout.addWidget(self.pushButtonCheck, 13, 4)  # Add widget to layout

        self.pushButtonFile = QtWidgets.QPushButton(parent=Form)
        layout.addWidget(self.pushButtonFile, 13, 0)  # Add widget to layout
        

        self.pushButtonFolder = QtWidgets.QPushButton(parent=Form)
        layout.addWidget(self.pushButtonFolder, 13, 1)  # Add widget to layout

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        for x in [self.radioButtonGptZero, self.radioButtonOpenAi, self.radioButtonWriter, self.radioButtonCrossplag, self.radioButtonCopyleaks, self.radioButtonSapling, self.radioButtonContentAtScale, self.radioButtonZeroGpt]:
            x.stateChanged.connect(self.updateUndetectableGroup)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("AI Text Detector", "AI Text Detector"))
        self.radioButtonGptZero.setText(_translate("Form", "GPTZERO"))
        self.radioButtonOpenAi.setText(_translate("Form", "OPENAI"))
        self.radioButtonWriter.setText(_translate("Form", "WRITER"))
        self.radioButtonCrossplag.setText(_translate("Form", "CROSSPLAG"))
        self.radioButtonCopyleaks.setText(_translate("Form", "COPYLEAKS"))
        self.radioButtonSapling.setText(_translate("Form", "SAPLING"))
        self.radioButtonContentAtScale.setText(_translate("Form", "CONTENTATSCALE"))
        self.radioButtonZeroGpt.setText(_translate("Form", "ZEROGPT"))
        self.radioButtonGrammica.setText(_translate("Form", "Grammica"))
        self.radioButtonWritefull.setText(_translate("Form", "Writefull"))
        self.radioButtonHive.setText(_translate("Form", "Hive"))
        self.radioButtonScribbr.setText(_translate("Form", "Scribbr"))
        self.radioButtonTypeset.setText(_translate("Form", "Typeset"))
        self.pushButtonCheck.setText(_translate("Form", "Check"))
        self.pushButtonFile.setText(_translate("Form", "Chose a file instead"))
        self.pushButtonFolder.setText(_translate("Form", "Chose a folder instead"))
    
    def set_indicator_color(self, indicator, result):
        # Create a QPixmap, QPainter and QBrush to draw a circle with the new color
        if result == "Human":
            color = "green"
        elif result == "AI":
            color = "red"
        else:
            color = "yellow"
        pixmap = QtGui.QPixmap(20, 20)
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(pixmap)
        brush = QtGui.QBrush(QtGui.QColor(color))
        painter.setBrush(brush)
        painter.drawEllipse(0, 3, 15, 15)
        painter.end()

        # Set the new QPixmap to the QLabel
        indicator.setPixmap(pixmap)
        # Add similar lines for all other indicators
        # Add similar lines for all other indicators

    def updateUndetectableGroup(self, state):
        if state == 0:
            for x in [self.radioButtonGptZero, self.radioButtonOpenAi, self.radioButtonWriter, self.radioButtonCrossplag, self.radioButtonCopyleaks, self.radioButtonSapling, self.radioButtonContentAtScale, self.radioButtonZeroGpt]:
                x.setChecked(False)
        elif state == 2:
            for x in [self.radioButtonGptZero, self.radioButtonOpenAi, self.radioButtonWriter, self.radioButtonCrossplag, self.radioButtonCopyleaks, self.radioButtonSapling, self.radioButtonContentAtScale, self.radioButtonZeroGpt]:
                x.setChecked(True)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())