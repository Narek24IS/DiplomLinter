from dataclasses import dataclass
from pathlib import Path


@dataclass
class LinterResult:
    """Результат выполнения линтера"""
    success: bool
    output: str


class Linter:
    """Базовый класс для всех линтеров"""
    def __init__(self, linter_name: str):
        self.linter_name = linter_name
        self.linter_path = Path(__file__).parent.parent / 'bin' / self.linter_name
        if not self.linter_path.exists():
            raise RuntimeError("Бинарник линтера не найден в локальных зависимостях")
        self.linter_path = str(self.linter_path.resolve())

    def run(self, path: Path, fix: bool = False) -> LinterResult:
        """
        Запускает линтер

        Args:
            path: Путь к директории с кодом
            fix: Флаг автоматического исправления

        Returns:
            LinterResult: Результат работы линтера
        """
        raise NotImplementedError("Метод должен быть реализован в подклассе")