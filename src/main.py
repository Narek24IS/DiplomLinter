import argparse
import os
import sys
from pathlib import Path
from linters.python_linter import PythonLinter
from linters.cpp_linter import CppLinter
from linters.golang_linter import GolangLinter
import logging


class LinterFactory:
    """Фабрика для создания объектов-линтеров"""

    LINTERS = {
        'python': PythonLinter,
        'cpp': CppLinter,
        'c': CppLinter,
        'go': GolangLinter
    }

    @classmethod
    def get_linter(cls, language: str):
        """Возвращает экземпляр линтера для указанного языка"""
        linter_class = cls.LINTERS.get(language.lower())
        if not linter_class:
            raise ValueError(f"Unsupported language: {language}")
        return linter_class()


def parse_args():
    """Разбор аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description='Универсальный линтер для проверки кода')
    parser.add_argument('language', type=str,
                        help='Язык программирования (python, cpp, c, go)')
    parser.add_argument('path', type=str,
                        help='Путь к проверяемой директории')
    parser.add_argument('--fix', action='store_true',
                        help='Автоматически исправлять найденные проблемы')
    return parser.parse_args()


def main():
    """Основная функция программы"""
    args = parse_args()

    if not os.path.exists(args.path):
        logging.info(f"Ошибка: путь {args.path} не существует")
        sys.exit(1)

    try:
        linter = LinterFactory.get_linter(args.language)
        logging.info(f"Запуск линтера для {args.language}...")

        # Запуск проверки
        result = linter.run(Path(args.path), fix=args.fix)

        # Вывод результатов
        if result.success:
            logging.info("Проверка завершена успешно!")
            if args.fix:
                logging.info("Все автоматические исправления применены")
            else:
                logging.info("Проблем не найдено")
        else:
            logging.info("Обнаружены проблемы:")
            logging.info(result.output)
            sys.exit(1)

    except Exception as e:
        logging.info(f"Ошибка: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()