import subprocess
from pathlib import Path

from base import Linter, LinterResult


class PythonLinter(Linter):
    """Линтер для Python кода"""

    def run(self, path: Path, fix: bool = False) -> LinterResult:
        # Сначала проверяем
        result = subprocess.run(
            ['flake8', str(path)],
            capture_output=True,
            text=True
        )

        if fix and result.returncode != 0:
            # Запускаем autopep8 для исправлений
            subprocess.run(
                ['autopep8', '--in-place', '--recursive', str(path)],
                check=True
            )
            # Повторная проверка после исправлений
            result = subprocess.run(
                ['flake8', str(path)],
                capture_output=True,
                text=True
            )

        return LinterResult(
            success=result.returncode == 0,
            output=result.stdout or result.stderr
        )
