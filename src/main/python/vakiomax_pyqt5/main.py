#!/usr/bin/env python


import sys

from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import (QDialog, QComboBox, QLabel, QHBoxLayout, QTextEdit, QPushButton, QLineEdit,
                             QWidget, QVBoxLayout, QMessageBox)
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from vakiomax_pyqt5.connections import login, refresh_games, ConnectionException, send_games
from vakiomax_pyqt5.parselines import coupon_rows_to_wager_requests, draws_to_options, GameOption


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
        self.login_btn.clicked.connect(self.do_login)
        self.send_btn.clicked.connect(self.do_send_rows)
        self.game_combo_box.currentIndexChanged.connect(self.enable_text_when_value_selected)
        self.game_combo_box.currentIndexChanged.connect(self.check_row_validity)
        self.text_edit.textChanged.connect(self.check_row_validity)

    def check_row_validity(self):
        current_game_option: GameOption = self.game_combo_box.currentData()
        current_text = self.text_edit.toPlainText().lower()
        if not current_game_option:
            self.send_btn.setEnabled(False)
            return
        parsed_coupons = coupon_rows_to_wager_requests(current_text, current_game_option.id,
                                                       current_game_option.base_price)
        is_valid = True if parsed_coupons else False
        for coupon in parsed_coupons:
            selections_ = coupon['selections']
            for s in selections_:
                is_valid &= len(s['outcomes']) == current_game_option.rows_count
        self.send_btn.setEnabled(is_valid)

    def enable_text_when_value_selected(self):
        data = self.game_combo_box.currentData()
        self.game_send_layout_container.setEnabled(True if data else False)

    def do_login(self):
        u = self.username.text()
        p = self.password.text()
        print(f'would login with "{u}" "{p}"')
        try:
            self.session = login(u, p)
            self.login_container.hide()
            self.do_refresh_games()
            self.game_layout_container.setEnabled(True)
            self.send_btn.setEnabled(False)
            self.game_combo_box.setFocus()
            self.game_layout_container.show()
        except ConnectionException as e:
            QMessageBox.warning(self, "Kirjautumisvirhe", f"Kirjautuminen epäonnistui:\n{e.msg} {e.status_code}",
                                QMessageBox.Ok)

        pass

    def do_refresh_games(self):
        options = draws_to_options(refresh_games(self.session))
        self.game_combo_box.clear()
        self.game_combo_box.addItem('')
        for option in options:
            self.game_combo_box.addItem(option.name, option)

    def do_send_rows(self):
        selected_option: GameOption = self.game_combo_box.currentData()
        print(selected_option)
        coupons = coupon_rows_to_wager_requests(self.text_edit.toPlainText(), selected_option.id,
                                                selected_option.base_price)

        coupons_in_chunks = chunks(coupons, 25)
        try:
            for chunk in coupons_in_chunks:
                send_games(self.session, chunk)
            QMessageBox.information(self, "Pelit ostettu", f"{len(coupons)} peliä ostettu onnistuneesti")
            self.text_edit.clear()
        except ConnectionException as e:
            QMessageBox.warning(self, "Lähetysvirhe", f"Pelien lähetys epäonnistui:\n{e.msg} {e.status_code}",
                                QMessageBox.Ok)



def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


if __name__ == '__main__':
    appctxt = ApplicationContext()
    vakiomax = VakioMax()
    vakiomax.show()
    sys.exit(appctxt.app.exec_())
