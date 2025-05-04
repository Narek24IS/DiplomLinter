import inspect
from pathlib import Path
from typing import Optional, Dict, Any

from logger.context_vars import call_context


class ExtraFieldsProcessor:
    """Процессор для переноса всех доп полей во вложенное поле extra_fields."""

    BASE_FIELDS = ["event", "level", "timestamp", "reference", "exc_info", "sec_info"]

    def __call__(self, _, __, event_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обрабатывает словарь с данными лога, перенося доп поля в одно вложенное поле.

        :param _: Неиспользуемый аргумент (логгер)
        :param __: Неиспользуемый аргумент (метод)
        :param event_dict: Словарь с данными лога
        :return: Модифицированный словарь с данными лога
        """
        extra_fields = {}
        for key in list(event_dict.keys()):
            if key in self.BASE_FIELDS or key.startswith("_"):
                continue
            extra_fields[key] = event_dict.pop(key)

        if extra_fields:
            event_dict["extra_fields"] = extra_fields

        return event_dict

class SecureDataProcessor:
    """Процессор для защиты конфиденциальных данных в логах."""

    SENSITIVE_KEYS = {"password", "token", "secret"}

    def __call__(self, _, __, event_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обрабатывает словарь с данными лога, удаляя конфиденциальные поля.

        :param _: Неиспользуемый аргумент (логгер)
        :param __: Неиспользуемый аргумент (метод)
        :param event_dict: Словарь с данными лога
        :return: Модифицированный словарь с данными лога
        """
        sec_info = {}
        for key in list(event_dict.keys()):
            if key in self.SENSITIVE_KEYS:
                sec_info[key] = event_dict.pop(key)

        if sec_info:
            event_dict["sec_info"] = sec_info

        return event_dict


def _get_project_root() -> Path:
    """
    Определяет корневую директорию проекта.

    Ищет маркеры (.git или README.md) в родительских директориях.
    :return: Path объект корневой директории проекта
    """
    path = Path(__file__).absolute()
    while not any((path / marker).exists() for marker in (".git", "README.md")):
        if path == path.parent:
            return path
        path = path.parent
    return path


class ReferenceProcessor:
    """Процессор для добавления ссылок на место вызова лога."""

    PROJECT_ROOT = _get_project_root()

    def __call__(self, _, __, event_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Добавляет в лог ссылку на место вызова в формате 'относительный_путь:номер_строки'.

        :param _: Неиспользуемый аргумент (логгер)
        :param __: Неиспользуемый аргумент (метод)
        :param event_dict: Словарь с данными лога
        :return: Модифицированный словарь с данными лога
        """
        params: Optional[Dict[str, Any]] = call_context.get()
        if params and params.get('pathname'):
            full_pathname = params.get('pathname')
            lineno = params.get('lineno')
        else:
            # Fallback для синхронных вызовов
            frame = self._get_caller_frame()
            full_pathname = frame.filename
            lineno = frame.lineno

        try:
            relative_pathname = Path(full_pathname).relative_to(self.PROJECT_ROOT)
        except Exception:
            relative_pathname = full_pathname
        event_dict["reference"] = f"{relative_pathname}:{lineno}"
        return event_dict

    @staticmethod
    def _get_caller_frame() -> inspect.FrameInfo:
        """
        Находит первый релевантный фрейм вызова, игнорируя системные модули.

        :return: Объект фрейма вызова
        """
        ignores = ["structlog", "logging", "stdlib", "site-packages", "python3.", "logger", "threading"]
        frames = inspect.stack()
        for frame in frames:
            frame_filepath = frame.frame.f_globals.get('__file__', '')
            if not any(ignore in frame_filepath for ignore in ignores):
                return frame
        return frames[-1]