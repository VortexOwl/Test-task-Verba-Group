# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from datetime import timedelta, datetime
from os import mkdir
from os.path import isdir, getsize
from pathlib import Path

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from src.logs.config import is_clear_logs


def creating_necessary_folders(path:str) -> None:
    if not isdir(s=path):
        mkdir(path=path)


def clearing_logs() -> None:
    if is_clear_logs:
        print('Введитие названия файлов журнала для их очистки через пробел.')
        files_names = input().split(' ')
        if files_names[0] == '':
            files_names[0] = 'logs'
        for file_name in files_names:
            if file_name == 'info' or file_name == 'debug' or file_name == 'error' or file_name == 'warning' or file_name == 'fatal':
                file_name = f'log_{file_name}'
        for file_name in files_names:
            if getsize(f'logs/{file_name}.log') / 1048576 > 1024:
                print(f'Начата очистка файла {file_name}.log от данных месячной давности')
                with open(f'logs/{file_name}.log', 'r') as file_logs:
                    lines = file_logs.readlines()
                with open(f'logs/{file_name}.log', 'w') as file_logs:
                    last_date = datetime.now()
                    last_date_log = last_date
                    for line in lines:
                        if line.find('INFO') != -1 or line.find('DEBUG') != -1 or line.find('WARNING') != -1 or line.find(
                                'ERROR') != -1 or line.find('FATAL') != -1:
                            date = datetime.strptime(line.split(' |')[0], '%Y-%m-%d %H:%M:%S')
                            last_date_log = date
                            if last_date - date <= timedelta(days=30):
                                file_logs.write(line)
                        else:
                            if last_date - last_date_log <= timedelta(days=30):
                                file_logs.write(line)

