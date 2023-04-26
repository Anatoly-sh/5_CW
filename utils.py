import json
import time
from typing import Any
import psycopg2
import requests


def get_employers() -> list:
    """
    Формирует список работодателей перебором всех ID HeadHunter
    с ключевым словом 'разработка' и с открытыми вакансиями.
    :return: Список вакансий
    """
    req = requests.get('https://api.hh.ru/employers', params={'text': 'разработка', 'only_with_vacancies': True})
    data = req.content.decode()
    req.close()
    count_of_employers = json.loads(data)['found']
    print(count_of_employers)
    employers = []
    i = 0
    j = count_of_employers
    # j = 20
    while i < j:
        req = requests.get('https://api.hh.ru/employers/' + str(i + 1),
                           params={'text': 'разработка', 'only_with_vacancies': True})
        data = req.content.decode()
        req.close()
        jsObj = json.loads(data)
        try:
            if jsObj['open_vacancies'] > 1:
                employers.append([jsObj['id'], jsObj['name'], jsObj['open_vacancies']])
                print([jsObj['id'], jsObj['name'], jsObj['open_vacancies']])
            i += 1
        except:
            i += 1
            j += 1
        if i % 200 == 0:
            time.sleep(0.2)
    return employers


def get_employer(company: str) -> list:
    """
    Функция обращается к параметрам работодателя по его названию,
    переданному в параметре функции.
    :param company: название компании.
    :return: список параметров (идентификационный номер, название в базе HH, количество открытых вакансий).
    """
    req = requests.get('https://api.hh.ru/employers/',
                       params={'text': f'{company}', 'only_with_vacancies': True})
    employer_data = req.json()
    req.close()
    return [employer_data['items'][0]['id'],
            employer_data['items'][0]['name'],
            employer_data['items'][0]['open_vacancies']]


def get_vacancies(company_id) -> list:
    """
    Функция постранично считывает вакансии указанной в переданном параметре
    компании и возвращает список словарей вакансий.
    :param company_id: id компании.
    :return: список вакансий указанной компании.
    """
    req = requests.get(f'https://api.hh.ru/vacancies/', params={
        'employer_id': f'{company_id}',
        'text': 'разработка',
        'only_with_vacancies': True,
        'only_with_salary': True
    })
    count_of_pages = req.json()['pages']  # Узнаем количество страниц вакансий
    req.close()
    vacancy_list = []
    for page in range(count_of_pages):
        req = requests.get('https://api.hh.ru/vacancies/', params={
            'employer_id': f'{company_id}',
            'text': 'разработка',
            'only_with_vacancies': True,
            'only_with_salary': True,
            'page': f'{page}'
        })
        page_data = req.json()
        req.close()
        vacancy_list.extend(page_data['items'])
        time.sleep(0.2)
    return vacancy_list


def load_db_employers(company: list, database: str, **params: dict[Any]) -> None:
    """
    Функция записывает в БД таблицу employers данные из списка,
    полученного в переданном параметре.
    :param database:
    :param company:
    :return: Ничего не возвращает.
    """
    # connect to db
    conn = psycopg2.connect(dbname=database, **params)
    try:
        with conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO employers VALUES (%s, %s, %s)", company)
        conn.commit()
    finally:
        conn.close()


def load_db_vacancy_param(vacancy: list, database: str, **params) -> None:
    """
    Функция записывает в БД таблицу employers данные из списка словарей,
    полученного в переданном параметре. Каждый словарь - вакансия.
    :param database:
    :param vacancy:
    :return:
    """
    # connect to db
    conn = psycopg2.connect(dbname=database, **params)
    try:
        with conn:
            cur = conn.cursor()
            for vacancy_dict in vacancy:
                if vacancy_dict["salary"]["from"] is None:
                    continue
                vacancy_data = (vacancy_dict["employer"]["id"],
                                vacancy_dict["id"],
                                vacancy_dict["name"],
                                vacancy_dict["salary"]["from"],
                                vacancy_dict["alternate_url"],
                                vacancy_dict["published_at"][:10],
                                vacancy_dict["area"]["name"],
                                vacancy_dict["snippet"]["requirement"])
                cur.execute("INSERT INTO vacancy_param VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", vacancy_data)
                # pprint(vacancy_data)
                print('.', end='')
    finally:
        conn.close()


def create_db_and_tables(database: str, params: dict) -> None:
    """
    Создает новую БД и таблицы. Все имена и параметры внутри кода.
    :return: None
    """
    # Создание БД
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database}")
    cur.execute(f"CREATE DATABASE {database}")
    print(f'БД "{database}" создана')
    cur.close()
    conn.close()

    # Создание таблиц
    conn = psycopg2.connect(dbname=database, **params)
    try:
        # conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS employers, vacancy_param")

            cur.execute("""
            CREATE TABLE employers (
                employer_id varchar(30) PRIMARY KEY, 
                company_name varchar(50), 
                vacancy_quantity int
            )
            """)

            cur.execute("""
            CREATE TABLE vacancy_param (
                employer_id varchar(30),
                FOREIGN KEY (employer_id)
                REFERENCES employers(employer_id),
                vacancy_id int UNIQUE,
                vacancy_name varchar(100),
                salary_from int NOT NULL,
                url varchar(100),
                publicy_date date,
                area varchar(50),
                requirement text
            )
        """)
        conn.commit()
    finally:
        conn.close()
    print(f'Таблицы в БД "{database}" созданы')
