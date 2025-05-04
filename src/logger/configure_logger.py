import logging
import os
from typing import List, Sequence, Optional, Union

import structlog
from structlog import stdlib, processors
from structlog.processors import CallsiteParameter
from structlog.tracebacks import ExceptionDictTransformer
from structlog.typing import Processor

from logger.processors import ReferenceProcessor, SecureDataProcessor, ExtraFieldsProcessor
from logger.wrapper import CustomAsyncBoundLogger

_nameToLevel = {
    'CRITICAL': logging.CRITICAL,
    'FATAL': logging.FATAL,
    'ERROR': logging.ERROR,
    'WARN': logging.WARNING,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET,
}


def _checkLevel(level):
    if isinstance(level, int):
        rv = level
    elif str(level) == level:
        if level not in _nameToLevel:
            raise ValueError("Unknown level: %r" % level)
        rv = _nameToLevel[level]
    else:
        raise TypeError("Level not an integer or a valid string: %r"
                        % (level,))
    return rv


def __get_environment() -> str:
    """
    Определяет текущее окружение на основе переменных среды.
    Возвращает 'production' по умолчанию, если ни одна переменная не задана

    Проверяет переменные среды в следующем порядке:
    1. APP_ENVIRONMENT
    2. ENVIRONMENT
    3. ENV
    """
    for env_key in ("APP_ENVIRONMENT", "ENVIRONMENT", "ENV"):
        if os.getenv(env_key):
            return os.getenv(env_key)

    return "production"


ENVIRONMENT = __get_environment()


def get_logger(name: str = "") -> logging.Logger:
    """
    Возвращает стандартный логгер Python.

    :param name: Имя логгера. Если не указано, возвращает корневой логгер.
    """
    return logging.getLogger(name)


def get_async_logger(name: str = "") -> CustomAsyncBoundLogger:
    """
    Возвращает асинхронный логгер structlog с кастомной обёрткой.

    :param name: Имя логгера. Если не указано, возвращает корневой логгер.
    """
    return structlog.get_logger(name)


def configure_logger(enable_json_logs: Optional[bool] = None, debug: Optional[bool] = None,
                     show_locals: Optional[bool] = None, access_logs: Optional[bool] = None,
                     log_level: Optional[Union[int, str]] = None) -> None:
    """
    Настраивает систему логирования для приложения.

    Конфигурация зависит от окружения:
    - В локальном окружении (ENVIRONMENT=local) использует цветной вывод в консоль
    - В других окружениях использует JSON-форматирование логов

    :param enable_json_logs: Принудительно включить JSON-логи
    :param debug: Включить режим отладки (более подробные логи)
    :param access_logs: Показывать локальные переменные в стектрейсах
    :param show_locals: Включить access логи
    :param log_level: Уровень логирования. Если не указан - определяется по параметру DEBUG
    """
    enable_json_logs = enable_json_logs if enable_json_logs is not None else ENVIRONMENT != "local"
    debug = debug if debug is not None else os.getenv("DEBUG", "false").lower() in ("true", "1")
    show_locals = show_locals if show_locals is not None else os.getenv("SHOW_LOCALS", "false").lower() in ("true", "1")
    access_logs = access_logs if access_logs is not None else os.getenv("ACCESS_LOGS", "false").lower() in ("true", "1")
    log_level = log_level if log_level is not None else (logging.DEBUG if debug else logging.INFO)
    log_level = _checkLevel(log_level)

    # Базовые процессоры для всех логгеров
    shared_processors: List[Processor] = [
        stdlib.filter_by_level,  # Фильтрация по уровню логирования
        stdlib.add_log_level,  # Добавление уровня логирования
        processors.TimeStamper(fmt="iso", utc=True),  # Добавление временной метки в UTC
        ReferenceProcessor(),  # Кастомный процессор для ссылок
        SecureDataProcessor(),  # Кастомный процессор для защиты данных
        ExtraFieldsProcessor(),  # Кастомный процессор для доп полей
    ]

    # Дополнительные процессоры для режима отладки
    if debug:
        shared_processors.insert(2, stdlib.add_logger_name)  # Добавляем имя логгера
        shared_processors.insert(2,
                                 processors.CallsiteParameterAdder(
                                     [
                                         CallsiteParameter.THREAD,
                                         CallsiteParameter.THREAD_NAME,
                                         CallsiteParameter.PROCESS,
                                         CallsiteParameter.PROCESS_NAME,
                                     ]
                                 )
                                 )

    # Выбор рендерера в зависимости от формата логов
    if enable_json_logs:
        shared_processors.append(processors.ExceptionRenderer(
            ExceptionDictTransformer(show_locals=show_locals)))  # JSON-формат стектрейсов
        logs_render: Processor = processors.JSONRenderer(ensure_ascii=False)  # Рендерер для JSON
    else:
        logs_render: Processor = structlog.dev.ConsoleRenderer(colors=True)  # Цветной консольный вывод

    # Конфигурация structlog
    structlog.configure(
        processors=shared_processors + [stdlib.ProcessorFormatter.wrap_for_formatter],
        logger_factory=stdlib.LoggerFactory(),
        wrapper_class=CustomAsyncBoundLogger,  # type: ignore
        cache_logger_on_first_use=True,
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    handler = _get_custom_handler(shared_processors, logs_render)
    # Настройка стандартного logging модуля
    _set_handler_to_logger(root_logger, handler)
    # Настройка стандартного logging модуля
    _configure_uvicorn_by_custom(handler, access_logs, log_level)


def _get_custom_handler(
        shared_processors: Sequence[Processor],
        logs_render: Processor,
) -> logging.Handler:
    """
    Настраивает кастомный хэндлер и возвращает его

    :param shared_processors: Общие процессоры для логирования
    :param logs_render: Процессор для рендеринга логов
    :return: настроенный кастомный хэндлер
    """
    handler = logging.StreamHandler()

    formatter = stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            stdlib.ProcessorFormatter.remove_processors_meta,
            logs_render,
        ],
        logger=logging.getLogger(),
    )

    handler.setFormatter(formatter)
    handler.set_name("logger")

    return handler


def _set_handler_to_logger(
        logger: logging.Logger,
        handler: Optional[logging.Handler] = None
) -> None:
    """
    Настраивает стандартный модуль logging для работы с structlog.

    :param logger: логгер, у которого нужно заменить хэндлер
    :param handler: хэндлер, который нужно установить
    """
    # Удаляем старые обработчики с таким же именем
    for h in logger.handlers:
        logger.removeHandler(h)

    # Добавляем новый, если есть
    if handler:
        logger.addHandler(handler)


def _configure_uvicorn_by_custom(
        handler: logging.Handler,
        access_logs: bool = False,
        log_level: Union[int, str] = logging.INFO,
) -> None:
    """
    Настраивает стандартный логер для uvicorn.

    :param access_logs: Флаг для access логов
    """
    # Достаёт uvicorn-логер
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(log_level)

    _set_handler_to_logger(uvicorn_logger, handler)

    # Достаёт uvicorn-access-логер
    access_logger = logging.getLogger("uvicorn.access")
    # Выключаем стандартные access-логи и
    # включаем access-логи в нашем формате, если требуется
    _set_handler_to_logger(access_logger,
                           handler if access_logs else None)
