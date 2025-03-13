import logging
import subprocess
from pathlib import Path
from typing import Optional

from src.linters.base import Linter, LinterResult


class PythonLinter(Linter):
    """Линтер для Python кода"""
    def __init__(self):
        super().__init__("python", "ruff")

    def run(self, path: Path, fix: bool = False, output_file: Optional[str]=None,
            output_format:str = 'grouped') -> LinterResult:
        """
          --fix - Apply fixes to resolve lint violations
          --output-file - Specify file to write the linter output to (default: stdout) [env: RUFF_OUTPUT_FILE=]
          --output-format - Output serialization format for violations.
                Possible values: concise, full, json, json-lines, junit,
                grouped, github, gitlab, pylint, rdjson, azure, sarif.
        """
        flags = []

        if fix:
            flags.append("--unsafe-fixes")
        else:
            flags.append("--no-unsafe-fixes")


        if output_format:
            flags.extend((f"--output-format", output_format))

        if output_file:
            flags.extend((f"--output-file", output_file))

        res_cmd = [self.linter_path, "check", *flags, str(path)]
        logging.info(f"Запускается следующая команда: {' '.join(res_cmd)}")
        result = subprocess.run(
            res_cmd,
            capture_output=True,
            text=True
        )

        return LinterResult(
            success=result.returncode == 0,
            output=result.stdout or result.stderr
        )
