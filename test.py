import asyncio
import time

from linter_api_client import ApiClient, Configuration, ApiException
from linter_api_client.api import (
    UsersApi,
    ProjectsApi,
    ScansApi,
    LinterResultsApi
)
from linter_api_client.models import (
    UserCreate,
    ProjectCreate,
    ScanCreate
)

def full_flow():
    # 1. Настройка клиента
    config = Configuration(host="http://localhost:8000")
    token = "test_token_123"
    project_name = "Paginator Bot"
    with ApiClient(config) as api_client:
        users_api = UsersApi(api_client)
        projects_api = ProjectsApi(api_client)
        scans_api = ScansApi(api_client)
        results_api = LinterResultsApi(api_client)

        # 2. Создаем пользователя
        print("⏳ Создаем пользователя...")
        try:
            user = users_api.create_user(
                user_create=UserCreate(
                    username="test_user",
                    token=token
                )
            )
            print(f"✅ Пользователь создан: {user.id} {user.username}")
        except ApiException as e:
            user = users_api.get_user_by_token(token)
            print(f"✅ Пользователь получен: {user.id} {user.username}")

        try:
            # 3. Создаем проект
            print("\n⏳ Создаем проект...")
            project = projects_api.create_project(
                project_create=ProjectCreate(
                    name=project_name,
                    repository_url="https://github.com/Narek24IS/PaginatorBot.git",
                    token="test_token_123"
                )
            )
            print(f"✅ Проект создан: {project.id} {project.name}")
        except Exception as e:
            try:
                project = projects_api.get_project_by_name(project_name)
                print(f"✅ Проект создан: {project.id} {project.name}")
            except Exception as e:
                print(e.body)
                raise e

        # 4. Запускаем сканирование
        print("\n⏳ Запускаем сканирование...")
        scan = scans_api.start_scan(
            project_id=project.id,
            branch="master",
        )
        print(f"✅ Сканирование запущено: {scan.id}")

        # 5. Ждем завершения сканирования (опционально)
        print("\n⏳ Ожидаем завершения сканирования...")
        while True:
            current_scan = scans_api.get_scan(scan.id)
            if current_scan.status == "completed":
                break
            elif current_scan.status == "failed":
                print("❌ Сканирование завершилось с ошибкой")
                return
            time.sleep(2)
        print("✅ Сканирование завершено")

        # 6. Получаем результаты
        print("\n⏳ Получаем результаты сканирования...")
        results = results_api.get_scan_results(scan.id)
        print(f"✅ Получено {len(results)} результатов:")
        for result in results:
            print(f"  - {result.linter_name}: {'✅' if result.is_success else '❌'}")

        # 7. Получаем аналитику
        print("\n⏳ Получаем аналитику...")
        stats = results_api.get_scan_stats(scan.id)
        print("📊 Статистика по линтерам:")
        for stat in stats:
            print(
                f"  - {stat.linter_name}: "
                f"Всего запусков {stat.total_runs}, "
                f"Успешно {stat.success_rate:.0%}, "
            )

        # 8. Получаем информацию о проекте
        print("\n⏳ Получаем полную информацию о проекте...")
        full_project = projects_api.get_project_by_id(project.id)
        print(f"📂 Проект: {full_project.name}")
        print(f"🔗 URL: {full_project.repository_url}")
        print(f"🔄 Всего сканирований: {len(full_project.scans)}")

if __name__ == "__main__":
    full_flow()