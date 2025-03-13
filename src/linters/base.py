from dataclasses import dataclass
from pathlib import Path


@dataclass
class LinterResult:
    """Результат выполнения линтера"""
    success: bool
    output: str


class Linter:
    """Базовый класс для всех линтеров"""
    def __init__(self, language:str, linter_name: str):
        self.language = language
        self.linter_name = linter_name
        self.cur_dir = Path(__file__).parent / self.language
        self.linter_path = self.cur_dir / self.linter_name
        if not self.linter_path.exists():
            raise RuntimeError(f"Бинарник линтера не найден в локальных зависимостях по пути {self.linter_path}")
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