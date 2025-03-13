from pathlib import Path
import subprocess
from base import Linter, LinterResult


class GolangLinter(Linter):
    """Линтер для Go кода"""
    def __init__(self):
        super().__init__('golangci-lint')

    def run(self, path: Path, fix: bool = False) -> LinterResult:
        try:
            if fix:
                # Запуск golangci-lint с исправлениями
                result = subprocess.run(
                    [self.linter_path, 'run', '--fix', str(path)],
                    capture_output=True,
                    text=True
                )
            else:
                # Только проверка
                result = subprocess.run(
                    [self.linter_path, 'run', str(path)],
                    capture_output=True,
                    text=True
                )

            return LinterResult(
                success=result.returncode == 0,
                output=result.stdout or result.stderr
            )

        except FileNotFoundError:
            return LinterResult(
                success=False,
                output=f"{self.linter_name} не установлен. Установите его для проверки Go кода"
            )