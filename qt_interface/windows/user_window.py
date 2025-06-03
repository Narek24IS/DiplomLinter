import os
import sys
from time import sleep

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication

from linter_api_client import ProjectsApi, LinterResultsApi
from qt_interface.db.pgsql_connection import select, update, insert
from qt_interface.interface.user_window_ui import Ui_UserWindow
from qt_interface.settings import settings
from qt_interface.windows.table_window import TableWindow, JoinClause
from linter_api_client.api.scans_api import ScansApi


class UserWindow(QMainWindow, Ui_UserWindow):
    def __init__(self, user_id: int, parent: QMainWindow = None):
        super().__init__(parent)
        self.setupUi(self)
        self.user_id = user_id
        self.set_icon()
        self.set_avatar()
        self.set_labels()

        self.table_button_1.clicked.connect(self.open_projects_window)
        self.table_button_2.clicked.connect(self.open_scans_window)
        self.table_button_3.clicked.connect(self.open_results_window)
        self.table_button_4.clicked.connect(self.open_analysis_window)

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

    def set_labels(self):
        user_info = select(
            f"SELECT username, token FROM users WHERE user_id = {self.user_id}"
        )[0]
        self.token = f"Bearer {user_info['token']}"
        username = user_info.get("username", "Undefined")
        self.name_label.setText(username)
        self.role_label.setText("User")

    def go_back(self):
        self.parent().show()
        self.close()

    def open_projects_window(self):
        def start_scan(window: TableWindow, row_num: int, pk_value: str):
            """Сканировать"""
            project_id = pk_value
            client = ScansApi()
            client.api_client.configuration.host = f"{settings.server_host}:{settings.server_port}"
            client.start_scan(project_id=project_id, branch="main", authorization=self.token)
            QMessageBox.information(window, "Сканирование запущено", "Для проверки статуса сканирования перейдите в окно 'Мои сканирования'")



        self.window = TableWindow(main_table="projects", parent=self,
                                  columns=["project_id", "repository_url", "name", "created_at"],
                                  where_expression=f"projects.owner_id = {self.user_id}",
                                  button_func=start_scan,
                                  user_id=self.user_id, can_edit=True,
                                  can_add=True, can_delete=True)
        self.window.show()

    def open_scans_window(self):
        self.window = TableWindow(main_table="scans", parent=self,
                                  columns=["scan_id", "status", "started_at", "finished_at",
                                           "branch", "total_errors"],
                                  where_expression=f"projects.owner_id = {self.user_id}",
                                  joins=[
                                      JoinClause(
                                          tablename="projects",
                                          pk="project_id",
                                          join_query="LEFT JOIN projects ON projects.project_id = scans.project_id",
                                          columns=["repository_url", "name"]
                                      )
                                  ],
                                  user_id=self.user_id, can_edit=False, can_add=False, can_delete=True)
        self.window.show()

    def open_results_window(self):
        self.window = TableWindow(main_table="linter_results", parent=self,
                                  where_expression=f"projects.owner_id = {self.user_id}",
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
                                      )
                                  ],
                                  user_id=self.user_id, can_edit=False, can_add=False, can_delete=False)
        self.window.show()

    def open_analysis_window(self):
        def show_analysis_dialog(window: TableWindow, row_num: int, pk_value: str):
            """Аналитика"""
            scan_id = pk_value
            project_id = window.table.item(row_num, 3).text()
            results_api = ScansApi()
            results_api.api_client.configuration.host = f"{settings.server_host}:{settings.server_port}"
            projects_api = ProjectsApi()
            projects_api.api_client.configuration.host = f"{settings.server_host}:{settings.server_port}"
            stats_api = LinterResultsApi()
            stats_api.api_client.configuration.host = f"{settings.server_host}:{settings.server_port}"
            results = results_api.get_scan(scan_id, authorization=self.token)
            text = f"✅ Получено {len(results.linter_results)} результатов:"
            for result in results.linter_results:
                text += f"\n  - {result.linter_name}: {'✅' if result.is_success else '❌'}"

            # 7. Получаем аналитику
            text += "\n\n⏳ Получаем аналитику..."
            stats = stats_api.get_scan_stats(scan_id, authorization=self.token)
            text += "\n📊 Статистика по линтерам:"
            for stat in stats:
                text += (f"\n  - {stat.linter_name}: "
                    f"Всего запусков {stat.total_runs}, "
                    f"Успешно {stat.success_rate:.0%}, "
                )

            # 8. Получаем информацию о проекте
            text += "\n\n⏳ Получаем полную информацию о проекте..."
            full_project = projects_api.get_project_by_id(int(project_id), authorization=self.token)
            text += f"\n📂 Проект: {full_project.name}"
            text += f"\n🔗 URL: {full_project.repository_url}"
            text += f"\n🔄 Всего сканирований: {len(full_project.scans)}"

            QMessageBox.information(window, "Аналитика", text)

        self.window = TableWindow(main_table="scans", parent=self,
                                  where_expression=f"projects.owner_id = {self.user_id}",
                                  joins=[
                                      JoinClause(
                                          tablename="projects",
                                          pk="project_id",
                                          join_query="LEFT JOIN projects ON projects.project_id = scans.project_id",
                                          columns=["repository_url", "name"]
                                      )
                                  ],
                                  button_func=show_analysis_dialog,
                                  user_id=self.user_id, can_edit=False,
                                  can_add=False, can_delete=True)
        self.window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserWindow(1)
    window.show()
    sys.exit(app.exec())