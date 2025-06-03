import os

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QLineEdit

from qt_interface.db.pgsql_connection import select
from qt_interface.interface.auth_window_ui import Ui_AuthWindow
from qt_interface.settings import settings
from qt_interface.windows.user_window import UserWindow
from qt_interface.windows.admin_window import AdminWindow


class AuthWindow(QMainWindow, Ui_AuthWindow):
    """
    Окно авторизации пользователя.
    """

    def __init__(self, parent: QMainWindow = None):
        super().__init__(parent)
        self.setupUi(self)
        self.username = ""
        self.set_icon()

        self.pass_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.log_but.clicked.connect(self.authenticate_user)

    def set_icon(self):
        try:
            pixmap = QPixmap(
                os.path.join(
                    settings.project_root, "images", "logo.jpg"
                )
            )
            if not pixmap.isNull():
                self.icon_label.setPixmap(pixmap)
                self.icon_label.setScaledContents(True)
        except Exception as e:
            print(f"Ошибка загрузки иконки: {e}")

    def authenticate_user(self):
        login = self.log_edit.text().strip()
        password = self.pass_edit.text().strip()

        if login == settings.root_login or password == settings.root_password:
            self.user_id = 0
            self.open_admin_window()
            return

        try:
            row = select("SELECT user_id FROM users WHERE username = %s AND token = %s", (login, password))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка при поиске пользователя", str(e))
            return
        if row:
            self.log_edit.clear()
            self.pass_edit.clear()
            row = row[0]
            self.user_id = row["user_id"]
            self.open_user_window()
        else:
            QMessageBox.critical(self, "Ошибка", "Неверный логин или пароль.")

    def open_user_window(self):
        self.window = UserWindow(self.user_id, self)
        self.window.show()
        self.hide()

    def open_admin_window(self):
        self.window = AdminWindow(self.user_id, self)
        self.window.show()
        self.hide()
