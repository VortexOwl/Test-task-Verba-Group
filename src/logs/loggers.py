# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from logging import basicConfig, getLogger, Formatter, Logger, FileHandler, StreamHandler, INFO, DEBUG, WARNING, ERROR, FATAL

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from src.logs.config import LOG_LEVEL
from src.utilities.utilities import creating_necessary_folders


def create_main_logger(formatter: Formatter, log_level:int) -> Logger:
    logger = getLogger('main')
    logger.propagate = False
    file_handler = FileHandler('logs/logs.log', mode='a', encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    console_handler = StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


def create_sub_logger(name_log: str, formatter: Formatter) -> Logger:
    logger = getLogger(name_log)
    logger.propagate = False
    file_handler = FileHandler(f'logs/logs_{name_log}.log', mode='a', encoding='utf-8')
    file_handler.setLevel(globals()[name_log.upper()])
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def basic_configuration() -> None:
    global logger_main, logger_info, logger_debug, logger_warning, logger_error, logger_fatal
    creating_necessary_folders(path='logs')
    log_level = globals()[LOG_LEVEL.upper()]
    basicConfig(level=log_level)
    formatter = Formatter(fmt="{asctime} | {levelname} | {message}", style="{", datefmt="%Y-%m-%d %H:%M:%S")

    logger_main = create_main_logger(formatter=formatter, log_level=log_level)
    logger_info = create_sub_logger(name_log='info', formatter=formatter)
    logger_debug = create_sub_logger(name_log='debug', formatter=formatter)
    logger_warning = create_sub_logger(name_log='warning', formatter=formatter)
    logger_error = create_sub_logger(name_log='error', formatter=formatter)
    logger_fatal = create_sub_logger(name_log='fatal', formatter=formatter)


basic_configuration()
