#!/usr/bin/env python
import configparser
import os
import re
import sys
from pathlib import Path

from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import (QApplication, QDialog, QComboBox, QFormLayout, QLabel, QHBoxLayout, QTextEdit, QPushButton, QLineEdit,
                             QWidget, QVBoxLayout, QMessageBox)
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from vakiomax_pyqt5.connections import login, refresh_games, ConnectionException, send_games
from vakiomax_pyqt5.parselines import coupon_rows_to_wager_requests, draws_to_options, GameOption
from vakiomax_pyqt5.passwords import set_password, get_password

class LoginDialog(QDialog):
    def __init__(self, appWindow: QDialog, parent=None):
        super(LoginDialog, self).__init__(parent)

        self.appWindow = appWindow

        login_layout = QVBoxLayout()
        login_layout.addWidget(self._login_layout())
        self._connect_events()
        self._prepare_user_and_pass()

        self.setLayout(login_layout)
        self.setWindowTitle("VakioMax 4")

    def _login_layout(self):
        login_container = QWidget()
        login_layout = QFormLayout(login_container)
        username = QLineEdit()
        login_layout.addRow("&Käyttäjätunnus:", username)

        password = QLineEdit()
        password.setFixedWidth(250)
        password.setEchoMode(QLineEdit.Password)
        login_layout.addRow("Salasana:", password)

        login_btn = QPushButton('Login')
        login_layout.addRow(login_btn)

        self.login_container = login_container
        self.login_btn = login_btn
        self.username = username
        self.password = password
        return login_container

    def _connect_events(self):
        self.login_btn.clicked.connect(self.do_login)

    def do_login(self):
        u = self.username.text()
        p = self.password.text()
        print(f'trying login with {u}')
        set_username(u)
        try:
            self.appWindow.session = login(u, p)
            set_password(u, p)
            self.hide()
            self.appWindow.show()
            self.appWindow.do_refresh_games()
        except ConnectionException as e:
            QMessageBox.warning(self, "Kirjautumisvirhe", f"Kirjautuminen epäonnistui:\n{e.msg} {e.status_code}",
                                QMessageBox.Ok)

    def _prepare_user_and_pass(self):
        username = get_username()
        if username:
            self.username.setText(username)
            password = get_password(username)
            if password:
                self.password.setText(password)


class VakioMax(QDialog):

    def __init__(self, parent=None):
        self.session = None
        super(VakioMax, self).__init__(parent)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self._game_layout())
        self._connect_events()

        self.setLayout(main_layout)
        self.setWindowTitle("VakioMax 4")
        self.send_btn.setEnabled(False)
        self.game_layout_container.setEnabled(True)
        self.game_combo_box.setFocus()
        self.game_layout_container.show()


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
        font: QFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        font.setPointSize(12)
        text_edit.setFont(font)
        text_edit.setLineWrapMode(QTextEdit.NoWrap)
        text_edit.setAcceptRichText(False)
        self.text_edit = text_edit
        game_send_layout.addWidget(text_edit)
        self.game_send_layout_container = game_send_layout_container

        send_btn = QPushButton("Osta rivit")
        send_btn.setDefault(True)
        self.send_btn = send_btn
        game_send_layout.addWidget(send_btn)
        game_layout.addLayout(game_selection_layout)
        game_layout.addWidget(game_send_layout_container)

        self.game_combo_box = game_combo_box
        self.game_layout_container = game_layout_container
        return game_layout_container

    def _connect_events(self):
        self.send_btn.clicked.connect(self.do_send_rows)
        self.game_combo_box.currentIndexChanged.connect(self.enable_text_when_value_selected)
        self.game_combo_box.currentIndexChanged.connect(self.check_row_validity)
        self.text_edit.textChanged.connect(self.check_row_validity)


    def check_row_validity(self):
        current_game_option: GameOption = self.game_combo_box.currentData()
        current_text = self.text_edit.toPlainText()
        if not current_game_option:
            self.send_btn.setEnabled(False)
            return
        parsed_coupon = coupon_rows_to_wager_requests(current_text, current_game_option.list_index,
                                                      current_game_option.base_price)
        is_valid = True if parsed_coupon else False
        boards_ = parsed_coupon['boards']
        for board in boards_:
            is_valid &= len(board['selections']) == current_game_option.rows_count
        self.send_btn.setEnabled(is_valid)

    def enable_text_when_value_selected(self):
        data = self.game_combo_box.currentData()
        self.game_send_layout_container.setEnabled(True if data else False)

    def do_refresh_games(self):
        options = draws_to_options(refresh_games(self.session))
        self.game_combo_box.clear()
        self.game_combo_box.addItem('')
        for option in options:
            self.game_combo_box.addItem(option.name, option)

    def do_send_rows(self):
        selected_option: GameOption = self.game_combo_box.currentData()
        print(selected_option)
        rows_text = self.text_edit.toPlainText()
        split_rows = re.split(r'[\r\n]', rows_text.strip())
        rows_in_chunks = chunks(split_rows, 10)
        coupons = [coupon_rows_to_wager_requests('\n'.join(rows), selected_option.list_index,
                                                 selected_option.base_price) for rows in rows_in_chunks]

        try:
            for coupon in coupons:
                send_games(self.session, coupon)
            QMessageBox.information(self, "Pelit ostettu", f"{len(coupons)} kuponkia ostettu onnistuneesti")
            self.text_edit.clear()
        except ConnectionException as e:
            error_message = f"Pelien lähetys epäonnistui:\n{e.msg} {e.status_code}"
            print(error_message)
            QMessageBox.warning(self, "Lähetysvirhe", error_message,
                                QMessageBox.Ok)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


app_name = 'vakiomax4-pyqt5'
home_path = os.environ['HOME']
app_home = (Path(home_path) / 'Library' / 'Application Support' / app_name)


def get_username():
    config = configparser.ConfigParser()
    config_file = (app_home / 'config.ini')
    if config_file.exists():
        config.read(config_file)
        if 'user' in config:
            return config['user'].get('username')
    return None


def set_username(username):
    config = configparser.ConfigParser()
    app_home.mkdir(parents=True, exist_ok=True)
    config_file = (app_home / 'config.ini')
    if config_file.exists():
        config.read(config_file)
        if 'user' not in config:
            config['user'] = {}
        config['user']['username'] = username
    with config_file.open('w') as open_cfg_file:
        config.write(open_cfg_file)




if __name__ == '__main__':
    appctxt = ApplicationContext()
    app = QApplication.instance()
    app.setStyle('Fusion')

    vakiomax = VakioMax()
    loginDialog = LoginDialog(appWindow = vakiomax)
    loginDialog.show()
    sys.exit(appctxt.app.exec_())
