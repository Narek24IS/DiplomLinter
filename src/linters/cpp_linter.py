from pathlib import Path
import subprocess
from base import Linter, LinterResult


class CppLinter(Linter):
    def __init__(self):
        super().__init__('clang-tidy')

    def run(self, path: Path, fix: bool = False) -> LinterResult:
        # Используем clang-tidy для анализа
        try:
            if fix:
                # Запуск с автоматическим исправлением
                result = subprocess.run(
                    [self.linter_path, '-fix', '-quiet', str(path)],
                    capture_output=True,
                    text=True
                )
            else:
                # Только проверка
                result = subprocess.run(
                    [self.linter_path, str(path)],
                    capture_output=True,
                    text=True
                )

            # Проверяем вывод на наличие ошибок
            output = result.stdout or result.stderr
            success = "warning generated." not in output.lower()

            return LinterResult(
                success=success,
                output=output
            )

        except FileNotFoundError:
            return LinterResult(
                success=False,
                output=f"{self.linter_name} не установлен. Установите его для проверки C/C++ кода"
            )