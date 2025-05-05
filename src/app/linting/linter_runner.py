import asyncio
import json
import os
import pathlib
import shlex
import tempfile

from ..consumers.models import ProjectForLint
from ..db import crud
from ..db.connection import SessionLocal
from ..db.models import ScanStatus
from ..db.schemas import LinterResultCreate
from ..dependencies import get_logger
from ..settings import get_settings
from ..tools.urls import convert_url_to_project_name

logger = get_logger("Super Linter")


class ProjectLogger:
    """Контекстный менеджер для логирования с префиксом проекта."""

    def __init__(self, project_name: str):
        self.project_name = project_name

    async def info(self, message: str):
        await logger.info(f"[{self.project_name}] {message}")

    async def warning(self, message: str):
        await logger.warning(f"[{self.project_name}] {message}")

    async def error(self, message: str):
        await logger.error(f"[{self.project_name}] {message}")


async def handle_async_process(
        cmd: str, process: asyncio.subprocess.Process, project_logger: ProjectLogger, verbose: bool = False
):
    """
    Ожидает завершения переданного процесса, выводит её результат
    или кидает ошибку в случае, если команда провалилась

    :param cmd: Команда, которая была запущена в процессе
    :param process: Объект процесса запущенной команды
    :param project_logger: Логер, который будет использоваться при логировании
    :param verbose: Если флаг True - логировать весь вывод команды

    :raise CalledProcessError: Ошибка в случае, если код завершения команды не 0
    """
    await project_logger.info(f"Running command: {cmd}")

    stdout, _ = await process.communicate()
    if verbose:
        # if True:
        output = await trim_command_output(stdout, project_logger)
        await project_logger.info(f"VERBOSE:\n{output}")
    # if process.returncode != 0:
    #     raise subprocess.CalledProcessError(process.returncode or 2, cmd, stdout, None)


async def trim_command_output(output, project_logger: ProjectLogger):
    """
    Форматирует и выводит ошибки выполнения команд.

    :param output: поток вывода команды(stdout или stderr)
    :param project_logger: Логер, который будет использоваться при логировании
    """
    if not output:
        await project_logger.warning("STDOUT is empty.")
        return

    fmt_lines = []
    for line in output.decode().splitlines():
        stripped_line = line.strip().replace("  ", "")
        if stripped_line:
            fmt_lines.append(f"[{project_logger.project_name}] {line}")

    fmt_output = "\n".join(fmt_lines)
    return fmt_output


async def start_local_lint(project: ProjectForLint) -> dict[str:LinterResultCreate]:
    """
    Запускает линтинг проекта через локальную CLI утилиту.

    :param project: Данные проекта для сканирования.

    :raise CalledProcessError: Ошибка в случае, если код завершения команды не 0
    :raise Exception: Если происходит ошибка при выполнении.
    """
    project_name = convert_url_to_project_name(project.repository_url)
    branch = project.branch_name.replace("refs/heads/", "")
    settings = get_settings()
    project_logger = ProjectLogger(project_name)

    try:
        with tempfile.TemporaryDirectory(delete=False) as tmp_dir:
            # Клонируем репозиторий
            clone_cmd = ["git", "clone", "--depth", "1", "--branch", branch, project.repository_url, tmp_dir]
            clone_process = await asyncio.create_subprocess_exec(
                *clone_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )
            await handle_async_process(shlex.join(clone_cmd), clone_process, project_logger, settings.app_debug)
            await project_logger.info("Cloning completed successfully.")

            # Создаем директории для результатов
            output_dir_name = "super-linter-output"
            output_dir = pathlib.Path(tmp_dir) / output_dir_name
            output_dir.mkdir(exist_ok=True)

            # Подготавливаем команду для запуска линтера
            lint_cmd = [
                "bash", "/action/lib/linter.sh"
            ]

            env = {
                **os.environ,
                "RUN_LOCAL": "true",
                "USE_FIND_ALGORITHM": "true",
                "VALIDATE_ALL_CODEBASE": "true",
                "LOG_LEVEL": "DEBUG" if settings.app_debug else "INFO",
                "DEFAULT_WORKSPACE": tmp_dir,
                "FILTER_REGEX_EXCLUDE": ".idea",
                "SAVE_SUPER_LINTER_OUTPUT": "true",
                "SAVE_SUPER_LINTER_SUMMARY": "true",
                "JSON_SUMMARY": "true",
                "SUPER_LINTER_OUTPUT_DIRECTORY_NAME": output_dir_name,
            }

            await project_logger.info(f"Starting linting with command: {shlex.join(lint_cmd)}")

            lint_process = await asyncio.create_subprocess_exec(
                *lint_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                env=env,
                cwd=tmp_dir,
            )
            await handle_async_process(shlex.join(lint_cmd), lint_process, project_logger, settings.app_debug)

            # Обработка результатов
            output_file = output_dir / "super-linter/super-linter-results.json"
            if output_file.exists():
                await project_logger.info(f"Linting output: {output_file.read_text()}")

            results_file = output_dir / "super-linter-result-object.json"
            if results_file.exists():
                results = json.loads(results_file.read_text())
                if results:
                    await project_logger.info(f"Linting results: {json.dumps(results, indent=2)}")
            else:
                results = {}

            summary_file = output_dir / "super-linter-summary.md"
            if summary_file.exists():
                summary = json.loads(summary_file.read_text())
                if summary:
                    await project_logger.info(f"Linting summary:\n{json.dumps(summary, indent=2)}")
            else:
                summary = {}

            linting_result: dict[str:LinterResultCreate] = dict()
            for result in summary:
                linter = result.get("linter", "")
                if linter:
                    linting_result[linter] = LinterResultCreate(
                        linter_name=linter,
                        is_success=result.get("is_success", False),
                    )

            for result in results:
                linter = result.pop("V", [None])[0]
                if linter:
                    obj = linting_result[linter]
                    obj.output = f"STDOUT: {result.pop('Stdout', '')}\nSTDERR: {result.pop('Stderr', '')}"
                    obj.details = result

            await project_logger.info("Linting completed successfully.")

            return linting_result
    except Exception as e:
        await project_logger.error(f"Error during linting: {type(e).__name__} {e}")
        raise


async def run_linting(scan_id: int, repo_url: str, branch: str):
    db = SessionLocal()
    try:
        # Обновляем статус сканирования
        crud.update_scan_status(db, scan_id=scan_id, status=ScanStatus.IN_PROGRESS)

        # Запускаем линтинг (ваша реализация из вопроса)
        lint_results: dict[str:LinterResultCreate] = await start_local_lint(ProjectForLint(
            id=scan_id,
            repository_url=repo_url,
            branch_name=branch,
        ))

        # Сохраняем результаты
        for result in lint_results.values():
            result: LinterResultCreate
            crud.create_linter_result(
                db,
                scan_id=scan_id,
                result=result
            )

        crud.update_scan_status(
            db,
            scan_id=scan_id,
            status=ScanStatus.COMPLETED,
        )

    except Exception as e:
        await logger.error(f"Error during linting scan {scan_id}: {str(e)}")
        crud.update_scan_status(db, scan_id=scan_id, status=ScanStatus.FAILED)
    finally:
        db.close()
