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
)

def full_flow():
    # 1. Настройка клиента
    config = Configuration(host="http://localhost:8000")
    token = "test_token_123"
    project_name = "Paginator Bot"
    repo_url = "https://github.com/Narek24IS/PaginatorBot.git"
    project_name = "Cure Bot"
    repo_url = "https://github.com/Narek24IS/CuteBot.git"
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
            print(f"✅ Пользователь создан: {user.user_id} {user.username}")
        except ApiException as e:
            user = users_api.get_user_by_token(token)
            print(f"✅ Пользователь получен: {user.user_id} {user.username}")
        token = "Bearer " + token
        try:
            # 3. Создаем проект
            print("\n⏳ Создаем проект...")
            project = projects_api.create_project(
                project_create=ProjectCreate(
                    name=project_name,
                    repository_url=repo_url,
                    token="test_token_123"
                )
            )
            print(f"✅ Проект создан: {project.project_id} {project.name}")
        except Exception as e:
            try:
                project = projects_api.get_project_by_name(project_name, token)
                print(f"✅ Проект создан: {project.project_id} {project.name}")
            except Exception as e:
                print(e)
                raise e

        # 4. Запускаем сканирование
        print("\n⏳ Запускаем сканирование...")
        scan = scans_api.start_scan(
            project_id=project.project_id,
            branch="master",
            authorization=token
        )
        print(f"✅ Сканирование запущено: {scan.scan_id}")

        # 5. Ждем завершения сканирования (опционально)
        print("\n⏳ Ожидаем завершения сканирования...")
        while True:
            current_scan = scans_api.get_scan(scan.scan_id, authorization=token)
            if current_scan.status == "completed":
                break
            elif current_scan.status == "failed":
                print("❌ Сканирование завершилось с ошибкой")
                return
            time.sleep(2)
        print("✅ Сканирование завершено")

        # 6. Получаем результаты
        print("\n⏳ Получаем результаты сканирования...")
        results = results_api.get_scan_results(scan.scan_id, authorization=token)
        print(f"✅ Получено {len(results)} результатов:")
        for result in results:
            print(f"  - {result.linter_name}: {'✅' if result.is_success else '❌'}")

        # 7. Получаем аналитику
        print("\n⏳ Получаем аналитику...")
        stats = results_api.get_scan_stats(scan.scan_id, authorization=token)
        print("📊 Статистика по линтерам:")
        for stat in stats:
            print(
                f"  - {stat.linter_name}: "
                f"Всего запусков {stat.total_runs}, "
                f"Успешно {stat.success_rate:.0%}, "
            )

        # 8. Получаем информацию о проекте
        print("\n⏳ Получаем полную информацию о проекте...")
        full_project = projects_api.get_project_by_id(project.project_id, authorization=token)
        print(f"📂 Проект: {full_project.name}")
        print(f"🔗 URL: {full_project.repository_url}")
        print(f"🔄 Всего сканирований: {len(full_project.scans)}")

if __name__ == "__main__":
    full_flow()