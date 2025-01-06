import logging
import os
import sys
import zipfile
from datetime import datetime
from logging import Logger
from logging import LogRecord
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler

from app.config.settings import settings

LOG_FORMAT = '%(asctime)s.%(msecs)03d|%(levelname)s|%(thread)5s|%(name)-25.25s|%(message)s'

class StreamHandlerFilter(logging.Filter):
    """Filters loggers by name for console output."""
    loggers_to_filter = [
        'paramiko.transport',
        'urllib3.connectionpool',
    ]

    def filter(self, record: LogRecord) -> bool:
        """Определяет должен ли быть залогирован record.

        :param logging.LogRecord record: Запись для логирования.

        :return: True если record должен быть залогирован, иначе False.
        :rtype: bool
        """
        return record.name not in self.loggers_to_filter


def _get_uvicorn_loggers() -> tuple[Logger, Logger]:
    return logging.getLogger('uvicorn.error'), logging.getLogger('uvicorn.access')

def archive_log(log_path):
    zip_path = f"{log_path}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(log_path, os.path.basename(log_path))
    os.remove(log_path)

class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def doRollover(self):
        super().doRollover()
        if not self.delay:
            archive_log(self.baseFilename + "." + self.suffix)

class CustomRotatingFileHandler(RotatingFileHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def doRollover(self):
        super().doRollover()
        archive_log(self.baseFilename + ".1")

def config_logging_dev():
    log_settings = settings.log
    log_dir = log_settings.logs_path
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{datetime.now():%Y-%m-%d-%H-%M-%S}.log")

    # Основной логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(log_settings.log_level_upper)

    # Форматтер
    file_formatter = logging.Formatter(LOG_FORMAT)

    # Time-based rotating file handler
    time_handler = CustomTimedRotatingFileHandler(
        filename=log_file, when="midnight", interval=1, backupCount=log_settings.max_log_files
    )
    time_handler.setLevel(log_settings.log_level_upper)
    time_handler.setFormatter(file_formatter)
    time_handler.addFilter(StreamHandlerFilter())

    # Size-based rotating file handler
    size_handler = CustomRotatingFileHandler(
        filename=log_file, maxBytes=log_settings.max_size * 1024 * 1024, backupCount=log_settings.max_log_files
    )
    size_handler.setLevel(log_settings.log_level_upper)
    size_handler.setFormatter(file_formatter)
    size_handler.addFilter(StreamHandlerFilter())

    # Console handler для вывода в stdout
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_settings.log_level_upper)
    console_handler.setFormatter(file_formatter)

    # Добавление хэндлеров к логгеру
    root_logger.addHandler(time_handler)
    root_logger.addHandler(size_handler)
    root_logger.addHandler(console_handler)

    # Настройка uvicorn логгеров
    for uvicorn_logger in _get_uvicorn_loggers():
        uvicorn_logger.setLevel(logging.INFO)
        uvicorn_logger.propagate = False
        if not any(isinstance(h, logging.StreamHandler) for h in uvicorn_logger.handlers):
            uvicorn_logger.addHandler(console_handler)

    # Настройка логгера для sqlalchemy
    sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
    sqlalchemy_logger.propagate = False


def config_logging_prod():
    # Создание логгеров для stdout и stderr
    class StreamToStdoutHandler(logging.StreamHandler):
        def __init__(self):
            super().__init__(sys.stdout)

    class StreamToStderrHandler(logging.StreamHandler):
        def __init__(self):
            super().__init__(sys.stderr)

    # Настройка уровня логирования для каждого обработчика
    stdout_handler = StreamToStdoutHandler()
    stdout_handler.setLevel(logging.INFO)  # Логи с уровня INFO и ниже в stdout
    stdout_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    stderr_handler = StreamToStderrHandler()
    stderr_handler.setLevel(logging.WARNING)  # Логи WARNING и выше в stderr
    stderr_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # Настройка базового логгера
    logging.basicConfig(
        level=settings.log.log_level_upper,  # Уровень логирования для приложения
        handlers=[stdout_handler, stderr_handler],
    )