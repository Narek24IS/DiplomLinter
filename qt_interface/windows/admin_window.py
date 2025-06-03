import os
import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication

from qt_interface.db.pgsql_connection import select, update, insert
from qt_interface.interface.admin_window_ui import Ui_AdminWindow
from qt_interface.settings import settings
from qt_interface.windows.table_window import TableWindow, JoinClause


class AdminWindow(QMainWindow, Ui_AdminWindow):
    def __init__(self, user_id: int, parent: QMainWindow = None):
        super().__init__(parent)
        self.setupUi(self)
        self.user_id = user_id
        self.set_icon()
        self.set_avatar()

        self.back_btn.clicked.connect(self.go_back)
        self.table_button_1.clicked.connect(self.open_users_window)
        self.table_button_2.clicked.connect(self.open_projects_window)
        self.table_button_3.clicked.connect(self.open_scans_window)
        self.table_button_4.clicked.connect(self.open_results_window)

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

    def set_avatar(self):
        try:
            pixmap = QPixmap(
                os.path.join(
                    settings.project_root, "images", "avatar.jpg"
                )
            )
            if not pixmap.isNull():
                self.avatar_label.setPixmap(pixmap)
                self.avatar_label.setScaledContents(True)
        except Exception as e:
            print(f"Ошибка загрузки аватарки: {e}")

    def go_back(self):
        self.parent().show()
        self.close()

    def open_users_window(self):
        self.window = TableWindow(main_table="users", parent=self, user_id=self.user_id, can_edit=True, can_add=True, can_delete=True)
        self.window.show()

    def open_projects_window(self):
        self.window = TableWindow(main_table="projects", parent=self,
                                  joins=[                                      JoinClause(
                                      tablename="users",
                                      pk="user_id",
                                      join_query="LEFT JOIN users ON users.user_id = projects.owner_id",
                                      columns=["username", "created_at"]
                                  ),],
                                  user_id=self.user_id, can_edit=True,
                                  can_add=True, can_delete=True)
        self.window.show()

    def open_scans_window(self):
        self.window = TableWindow(main_table="scans", parent=self,
                                  joins=[
                                      JoinClause(
                                          tablename="projects",
                                          pk="project_id",
                                          join_query="LEFT JOIN projects ON projects.project_id = scans.project_id",
                                          columns=["repository_url", "name"]
                                      ),
                                      JoinClause(
                                          tablename="users",
                                          pk="user_id",
                                          join_query="LEFT JOIN users ON users.user_id = projects.owner_id",
                                          columns=["username", "created_at"]
                                      ),
                                  ],
                                  user_id=self.user_id, can_edit=True,
                                  can_add=True, can_delete=True)
        self.window.show()

    def open_results_window(self):
        self.window = TableWindow(main_table="linter_results", parent=self,
                                  joins=[
                                      JoinClause(
                                          tablename="scans",
                                          pk="scan_id",
                                          join_query="LEFT JOIN scans ON scans.scan_id = linter_results.scan_id",
                                          columns=["branch", "status", "started_at", "finished_at", "total_errors"]
                                      ),
                                      JoinClause(
                                          tablename="projects",
                                          pk="project_id",
                                          join_query="LEFT JOIN projects ON projects.project_id = scans.project_id",
                                          columns=["repository_url", "name"]
                                      ),
                                      JoinClause(
                                          tablename="users",
                                          pk="user_id",
                                          join_query="LEFT JOIN users ON users.user_id = projects.owner_id",
                                          columns=["username", "created_at"]
                                      ),
                                  ],
                                  user_id=self.user_id, can_edit=True,
                                  can_add=True, can_delete=True)
        self.window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminWindow(1)
    window.show()
    sys.exit(app.exec())