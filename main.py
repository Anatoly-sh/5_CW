"""
Пятая курсовая работа по SQL
Программа выполняет запрос вакансий
"""
import os


from config import config
from db_manager import DBManager
from utils import get_employer, load_db_employers, get_vacancies, load_db_vacancy_param, create_db_and_tables


def main():
    params = config()
    database = 'five_cw'
    db_ack = DBManager(database, params)
    menu_options = """
        1: Создать БД и структуру таблиц
        2: Заполнить базу данных
        3: Список всех компаний с количеством вакансий
        4: Список всех вакансий (компания, вакансия, зарплата, ссылка)
        5: Средняя зарплата по вакансиям
        6: Вакансии с зарплатой выше средней
        7: Вакансии с селекцией
        8: Завершение программы
        """
    while True:
        print(menu_options)
        try:
            option = input('Сделайте выбор: ')
        except:
            print('Неверный ввод. Пожалуйста введите цифру...')
        # Проверка выбора и действие
        if option == '1':
            create_db_and_tables(database, params)
        elif option == '2':
            load_db(database, params)
        elif option == '3':
            answer = db_ack.get_companies_and_vacancies_count()
            for i in answer:
                print(i)
        elif option == '4':
            answer = db_ack.get_all_vacancies()
            for i in answer:
                print(i)
        elif option == '5':
            answer = db_ack.get_avg_salary()
            for i in answer:
                print(i)
        elif option == '6':
            answer = db_ack.get_vacancies_with_higher_salary()
            for i in answer:
                print(i)
        elif option == '7':
            answer = db_ack.get_vacancies_with_keyword('Python')
            for i in answer:
                print(i)
        elif option == '8':
            print('Спасибо за использование программы')
            exit()
        else:
            print('Неверный ввод. Пожалуйста, введите цифру от 1 до 6')


def load_db(database, params: dict) -> None:
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
            load_db_employers(company_data, database, **params)                 #
            vacancy_list = get_vacancies(company_data[0])
            load_db_vacancy_param(vacancy_list, database, **params)             #


if __name__ == '__main__':
    main()

