# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from utilities import base_config_project
from src.logs import log_info, log_debug, log_error
from src.web.products import start_web
from src.table.products import create_table


def start() -> None:
    log_info('Запуск скрипта.')
    create_table(list_products=start_web())
    create_table(list_products=start_web(quest_number=2), sheet_name='Quest 2')
    log_info('Завершение скрипта.')
    

start()
