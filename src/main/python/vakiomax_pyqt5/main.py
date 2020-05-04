#!/usr/bin/env python


import sys

from PyQt5.QtWidgets import (QDialog, QComboBox, QLabel, QHBoxLayout, QGridLayout, QTextEdit, QPushButton)
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from vakiomax_pyqt5.parselines import coupon_rows_to_wager_request


class VakioMax(QDialog):
    def __init__(self, parent=None):
        super(VakioMax, self).__init__(parent)
        gameComboBox = QComboBox()
        gameComboBox.addItems(['foo', 'bar'])

        game_label = QLabel("&Peli:")
        game_label.setBuddy(gameComboBox)

        top_layout = QHBoxLayout()
        top_layout.addWidget(game_label)
        top_layout.addWidget(gameComboBox)

        text_edit = QTextEdit()
        text_edit.setLineWrapMode(QTextEdit.NoWrap)
        text_edit.setAcceptRichText(False)

        main_layout = QGridLayout()
        main_layout.addLayout(top_layout, 0, 0)
        main_layout.addWidget(text_edit, 1, 0)

        validate_btn = QPushButton("Tarkista rivit")
        validate_btn.setDefault(True)
        validate_btn.clicked.connect(lambda: print(coupon_rows_to_wager_request(text_edit.toPlainText(), 'foo', 'bar')))
        main_layout.addWidget(validate_btn)

        self.setLayout(main_layout)
        self.setWindowTitle("VakioMax 4")


if __name__ == '__main__':
    appctxt = ApplicationContext()
    vakiomax = VakioMax()
    vakiomax.show()
    sys.exit(appctxt.app.exec_())
