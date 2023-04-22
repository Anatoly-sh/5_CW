"""
Пятая курсовая работа по SQL
Программа выполняет запрос вакансий
"""
import os
import dotenv
from dotenv import load_dotenv

load_dotenv()
# if DB_IS_FULL == '1':
menu_options = """
    1: Заполнить базу данных
    2: Запросить/обновить данные с сайтов вакансий в локальных файлах
    3: Посмотреть вакансии в указанном городе
    4: Вывести 10 самых высокооплачиваемых вакансий
    5: Запись обрабатываемых вакансий в файл json
    6: Завершение программы
"""


def load_db() -> None:
    file_name = input('Укажите источник данных для поиска вакансий (по умолчанию company.txt):')
    if file_name == '':
        file_name = 'company.txt'
    if os.path.exists(file_name) is False:
        print('Файл не найден')
        return
    print('OK')



def method1():
    pass


def method2():
    pass



if __name__ == '__main__':

    while True:
        print(menu_options)
        # option = ''
        try:
            option = input('Сделайте выбор: ')
        except:
            print('Неверный ввод. Пожалуйста введите цифру...')
        # Проверка выбора и действие
        if option == '1':
            load_db()
        elif option == '2':
            method1()
        elif option == '3':
            method2()
        elif option == '6':
            print('Спасибо за использование программы')
            exit()
        else:
            print('Неверный ввод. Пожалуйста, введите цифру от 1 до 6')

