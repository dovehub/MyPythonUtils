import sys
import copy
import pathlib
from typing import Any, Dict, Optional, Union

from loguru import logger as _logger
from loguru._logger import Logger as _Logger


_logger.remove()

_path = Union[str, pathlib.Path, None]
_filename = Union[str, pathlib.Path, None]


class Logger:
    def __init__(self, path: _path = None):
        if path is None:
            basedir = pathlib.Path(__file__).parent.parent
        else:
            if isinstance(path, str):
                basedir = pathlib.Path(path)
            elif isinstance(path, pathlib.Path):
                basedir = path
            else:
                raise TypeError("path类型只能为str或pathlib.Path")
        if not basedir.is_absolute():
            basedir = basedir.absolute()

        self.path = basedir

    def __call__(
        self,
        prefix: str,
        filename: _filename = None,
        format: Optional[str] = None,
        stdout_options: Dict[str, Any] = {},
        file_options: Dict[str, Any] = {},
    ) -> _Logger:
        if filename is None:
            filename = prefix
        filepath = self.path / filename
        parent = filepath.parent
        if not parent.exists():
            parent.mkdir(parents=True)
        filepath = str(filepath)
        if not filepath.endswith(".log"):
            filepath += ".log"
        if format is None:
            format = f"<red>[</red> <green>{{time:YYYY-MM-DD HH:mm:ss.SSS}}</green> | <level>{{level: <8}}</level> | <cyan>{{name}}</cyan>:<cyan>{{function}}</cyan>:<cyan>{{line}}</cyan> | <fg #FFC0CB>{prefix}</fg #FFC0CB> <red>]</red> <level>{{message}}</level>"
        stdout_options.setdefault("format", format)
        file_options.setdefault("format", format)
        file_options.setdefault("level", "WARNING")
        logger = copy.deepcopy(_logger)
        logger.add(sys.stdout, **stdout_options)
        logger.add(filepath, **file_options)
        return logger
