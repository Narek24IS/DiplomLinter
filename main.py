import argparse
import os
import sys
from pathlib import Path
from src.linters.python.python_linter import PythonLinter
from src.linters.cpp.cpp_linter import CppLinter
from src.linters.go.golang_linter import GolangLinter
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
    parser = argparse.ArgumentParser(description='Универсальный линтер для проверки кода')
    parser.add_argument('language', type=str, choices=['python', 'cpp', 'c', 'go'],
                        help='Язык программирования (python, cpp, c, go)')
    parser.add_argument('path', type=str,
                        help='Путь к проверяемой директории')
    parser.add_argument('--fix', action='store_true',
                        help='Автоматически исправлять найденные проблемы')
    parser.add_argument('--output', "-o", default=None,
                        help='Сохранить результат в указанный файл: -o <output.txt>')
    return parser.parse_args()


def main():
    """Основная функция программы"""
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    args = parse_args()

    if not os.path.exists(args.path):
        logging.info(f"Ошибка: путь {args.path} не существует")
        sys.exit(1)

    try:
        linter = LinterFactory.get_linter(args.language)
        logging.info(f"Запуск линтера для {args.language}...")

        # Запуск проверки
        result = linter.run(Path(args.path), args.fix, args.output)

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
        logging.error(f"Ошибка: {str(e)}", exc_info=e)
        sys.exit(1)


if __name__ == "__main__":
    main()