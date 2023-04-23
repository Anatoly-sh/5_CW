"""
Пятая курсовая работа по SQL
Программа выполняет запрос вакансий
"""
import os
import dotenv
from dotenv import load_dotenv

from config import config
from db_manager import DBManager
from utils import get_employer, load_db_employees, get_vacancies, load_db_vacancy_param, create_db, create_tables


def main():
    global option
    load_dotenv()
    # database = 'five_cw'
    params = config()
    conn = None
    menu_options = """
        1: Создать БД и структуру таблиц
        2: Заполнить базу данных
        3: 3
        4: 4
        5: 5
        6: Завершение программы
        """
    while True:
        print(menu_options)
        # option = ''
        try:
            option = input('Сделайте выбор: ')
        except:
            print('Неверный ввод. Пожалуйста введите цифру...')
        # Проверка выбора и действие
        if option == '1':
            database = 'five_cw'
            create_db(database, params)
            create_tables(database, params)
        elif option == '2':
            load_db()
        elif option == '3':
            method1()
        elif option == '4':
            method2()
        elif option == '6':
            print('Спасибо за использование программы')
            exit()
        else:
            print('Неверный ввод. Пожалуйста, введите цифру от 1 до 6')


def load_db() -> None:
    file_name = input('Укажите источник данных для поиска вакансий (по умолчанию company.txt):')
    if file_name == '':
        file_name = 'company.txt'
    if os.path.exists(file_name) is False:
        print('Файл не найден')
        return
    with open(file_name) as file:
        for each_company in file:
            company_data = get_employer(each_company)
            print(company_data)
            load_db_employees(company_data, params)                 #
            vacancy_list = get_vacancies(company_data[0])
            load_db_vacancy_param(vacancy_list, params)             #


    # vacancy_list = get_vacancies('1122462')
    # load_db_vacancy_param(vacancy_list)


def method1():
    pass


def method2():
    pass


if __name__ == '__main__':
    main()

