# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from sys import exit
from traceback import extract_stack

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from src.logs.config import is_file_info, is_file_debug, is_file_warning, is_file_error, is_file_fatal, is_console_handler
from src.logs.loggers import logger_main, logger_info, logger_debug, logger_warning, logger_error, logger_fatal
from src.utilities.utilities import creating_necessary_folders, clearing_logs

def log_info(message:str) -> None:
    if not is_console_handler:
        print(message)
    message: str = f'Module: {extract_stack(limit=2)[0].filename.split('/')[-1]} | Func: {extract_stack(limit=2)[0].name} | Line: {extract_stack(limit=2)[0].lineno} | Message: {message}'
    logger_main.info(msg=message)
    if is_file_info:
        logger_info.info(msg=message)
    

def log_debug(message:str) -> None:
    message: str = f'Module: {extract_stack(limit=2)[0].filename.split('/')[-1]} | Func: {extract_stack(limit=2)[0].name} | Line: {extract_stack(limit=2)[0].lineno} | Message: {message}'
    logger_main.debug(msg=message)
    if is_file_debug:
        logger_debug.debug(msg=message)    
    

def log_warning(message:str) -> None:
    message: str = f'Module: {extract_stack(limit=2)[0].filename.split('/')[-1]} | Func: {extract_stack(limit=2)[0].name} | Line: {extract_stack(limit=2)[0].lineno} | Message: {message}'
    logger_main.warning(msg=message)
    if is_file_warning:
        logger_warning.warning(msg=message)


def log_error(message:str, module_name=None, line_no=None) -> None:
    if line_no is None:
        message: str = f'Module: {extract_stack(limit=2)[0].filename.split('/')[-1]} | Func: {extract_stack(limit=2)[0].name} | Line: {extract_stack(limit=2)[0].lineno} | Message: {message}'
    else:
        message: str = f'Module: {module_name} | Func: {extract_stack(limit=2)[0].name} | Line: {line_no} | Message: {message}'
    logger_main.error(msg=message)
    if is_file_error:
        logger_error.error(msg=message)


def log_fatal(message:str, module_name=None, line_no=None) -> None:
    if line_no is None:
        message: str = f'Module: {extract_stack(limit=2)[0].filename.split('/')[-1]} | Func: {extract_stack(limit=2)[0].name} | Line: {extract_stack(limit=2)[0].lineno} | Message: {message}'
    else:
        message: str = f'Module: {module_name} | Func: {extract_stack(limit=2)[0].name} | Line: {line_no} | Message: {message}'
    logger_main.fatal(msg=message)
    if is_file_fatal:
        logger_fatal.fatal(msg=message)
    exit()


def start_logs() -> None:
    creating_necessary_folders(path='logs')
    clearing_logs()


start_logs()
