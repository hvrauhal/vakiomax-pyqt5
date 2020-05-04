#!/usr/bin/env python


import sys

from PyQt5.QtWidgets import (QDialog, QComboBox, QLabel, QHBoxLayout, QGridLayout, QTextEdit)
from fbs_runtime.application_context.PyQt5 import ApplicationContext


class VakioMax(QDialog):
    def __init__(self, parent=None):
        super(VakioMax, self).__init__(parent)
        gameComboBox = QComboBox()
        gameComboBox.addItems(['foo', 'bar'])

        gameLabel = QLabel("&Peli:")
        gameLabel.setBuddy(gameComboBox)

        topLayout = QHBoxLayout()
        topLayout.addWidget(gameLabel)
        topLayout.addWidget(gameComboBox)

        textEdit = QTextEdit()

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0)
        mainLayout.addWidget(textEdit, 1, 0)

        self.setLayout(mainLayout)
        self.setWindowTitle("VakioMax 4")


if __name__ == '__main__':
    appctxt = ApplicationContext()
    vakiomax = VakioMax()
    vakiomax.show()
    sys.exit(appctxt.app.exec_())
