#!/usr/bin/env python


import sys

from PyQt5.QtWidgets import (QDialog, QComboBox, QLabel, QHBoxLayout, QTextEdit, QPushButton, QLineEdit,
                             QWidget, QVBoxLayout, QMessageBox)
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from vakiomax_pyqt5.connections import login, refresh_games, LoginException
from vakiomax_pyqt5.parselines import coupon_rows_to_wager_request, draws_to_options, GameOption


class VakioMax(QDialog):

    def __init__(self, parent=None):
        self.session = None
        super(VakioMax, self).__init__(parent)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self._login_layout())
        main_layout.addWidget(self._game_layout())
        self._connect_events()

        self.setLayout(main_layout)
        self.setWindowTitle("VakioMax 4")

    def _login_layout(self):
        login_container = QWidget()
        login_layout = QHBoxLayout(login_container)
        username = QLineEdit()
        u_label = QLabel("&Käyttäjätunnus:")
        u_label.setBuddy(username)

        password = QLineEdit()
        password.setEchoMode(QLineEdit.Password)
        p_label = QLabel("Salasana:")
        p_label.setBuddy(password)

        login_layout.addWidget(u_label)
        login_layout.addWidget(username)
        login_layout.addWidget(p_label)
        login_layout.addWidget(password)
        login_btn = QPushButton('Login')
        login_btn.setDefault(True)
        login_layout.addWidget(login_btn)

        self.login_container = login_container
        self.login_btn = login_btn
        self.username = username
        self.password = password
        return login_container

    def _game_layout(self):
        game_layout_container = QWidget()
        game_layout_container.setDisabled(True)
        game_layout = QVBoxLayout(game_layout_container)

        game_combo_box = QComboBox()

        game_label = QLabel("&Peli:")
        game_label.setBuddy(game_combo_box)
        game_selection_layout = QHBoxLayout()
        game_selection_layout.addWidget(game_label)
        game_selection_layout.addWidget(game_combo_box)

        game_send_layout_container = QWidget()
        game_send_layout = QVBoxLayout(game_send_layout_container)
        text_edit = QTextEdit()
        text_edit.setLineWrapMode(QTextEdit.NoWrap)
        text_edit.setAcceptRichText(False)
        self.text_edit = text_edit
        game_send_layout.addWidget(text_edit)
        self.game_send_layout_container = game_send_layout_container

        validate_btn = QPushButton("Tarkista rivit")
        validate_btn.setDefault(True)
        self.validate_btn = validate_btn
        game_send_layout.addWidget(validate_btn)
        game_layout.addLayout(game_selection_layout)
        game_layout.addWidget(game_send_layout_container)

        self.game_combo_box = game_combo_box
        self.game_layout_container = game_layout_container
        return game_layout_container

    def _connect_events(self):
        self.login_btn.clicked.connect(self.do_login)
        self.validate_btn.clicked.connect(self.do_check_rows)
        self.game_combo_box.currentIndexChanged.connect(self.enable_text_when_value_selected)

    def enable_text_when_value_selected(self):
        data = self.game_combo_box.currentData()
        self.game_send_layout_container.setDisabled(False if data else True)

    def do_login(self):
        u = self.username.text()
        p = self.password.text()
        print(f'would login with "{u}" "{p}"')
        try:
            self.session = login(u, p)
            self.login_container.hide()
            self.do_refresh_games()
            self.game_layout_container.setDisabled(False)
            self.game_combo_box.setFocus()
            self.game_layout_container.show()
        except LoginException as e:
            QMessageBox.warning(self, "Kirjautumisvirhe", f"Kirjautuminen epäonnistui:\n{e.msg} {e.status_code}",
                                QMessageBox.Ok)

        pass

    def do_refresh_games(self):
        options = draws_to_options(refresh_games(self.session))
        self.game_combo_box.clear()
        self.game_combo_box.addItem('')
        for option in options:
            self.game_combo_box.addItem(option.name, option)

    def do_check_rows(self):
        selected_option: GameOption = self.game_combo_box.currentData()
        print(selected_option)
        print(coupon_rows_to_wager_request(self.text_edit.toPlainText(), 'foo', 'bar'))


if __name__ == '__main__':
    appctxt = ApplicationContext()
    vakiomax = VakioMax()
    vakiomax.show()
    sys.exit(appctxt.app.exec_())
