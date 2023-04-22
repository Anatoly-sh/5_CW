import json
import time
from pprint import pprint

import pandas as pandas
import pandas.io.sql as psql
import psycopg2
import requests

"""
response = requests.get(url='https://api.hh.ru/employers/' + '1')
# response = requests.get(url='https://api.hh.ru/employers/', params={'open_vacancies': True, 'text': 'VK'})
data = response.content.decode()
# print(response)
# data_ = response.json()
with open('./111.json', 'w') as file:
    pprint(data)
    print(len(data))
    json.dump(data, file, indent=2, ensure_ascii=False)

"""


def get_employers():
    req = requests.get('https://api.hh.ru/employers', params={'text': 'разработка', 'only_with_vacancies': True})
    data = req.content.decode()
    req.close()
    count_of_employers = json.loads(data)['found']
    print(count_of_employers)
    employers = []
    i = 0
    # j = count_of_employers
    j = 20
    while i < j:
        req = requests.get('https://api.hh.ru/employers/' + str(i + 1),
                           params={'text': 'разработка', 'only_with_vacancies': True})
        data = req.content.decode()
        req.close()
        jsObj = json.loads(data)
        try:
            if jsObj['open_vacancies'] > 20:
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
        'text': '',
        'only_with_vacancies': True,
        'only_with_salary': True
    })
    count_of_pages = req.json()['pages']  # Узнаем количество страниц вакансий
    req.close()
    vacancy_list = []
    for page in range(count_of_pages):
        req = requests.get('https://api.hh.ru/vacancies/', params={
            'employer_id': f'{company_id}',
            'text': '',
            'only_with_vacancies': True,
            'only_with_salary': True,
            'page': f'{page}'
        })
        page_data = req.json()
        req.close()
        vacancy_list.extend(page_data['items'])
    return vacancy_list


def load_db_employees(company: list) -> None:
    """
    Функция записывает в БД 5_CW таблицу employees данные из списка,
    полученного в переданном параметре.
    :param company:
    :return: Ничего не возвращает.
    """
    # connect to db
    conn = psycopg2.connect(host='localhost', port=5433, database='5_CW', user='postgres', password='12345')
    try:
        with conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO employees VALUES (%s, %s, %s)", company)
        conn.commit()
    finally:
        conn.close()
    # for company in companies:
    #     print(company)

def load_db_vacancy_param(vacancy: list) -> None:
    """
    Функция записывает в БД 5_CW таблицу employees данные из списка словарей,
    полученного в переданном параметре. Каждый словарь - вакансия.
    :param vacancy:
    :return:
    """
    # connect to db
    conn = psycopg2.connect(host='localhost', port=5433, database='5_CW', user='postgres', password='12345')
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
                pprint(vacancy_data)
    finally:
        conn.close()


# with open('./company.txt') as file:
#     for each_company in file:
#         company_data = get_employer(each_company)
#         print(company_data)
#         load_db_employees(company_data)
#
# vacancy_list = get_vacancies('1122462')
# load_db_vacancy_param(vacancy_list)

conn = psycopg2.connect(host='localhost', port=5433, database='5_CW', user='postgres', password='12345')
try:
    with conn:
        # my_table = psql.read_sql('SELECT * FROM employees', conn)
        cur = conn.cursor()
        cur.execute("CREATE DATABASE TMP")
    conn.commit()
finally:
    conn.close()
# print(my_table)

# матюк
# conn = psycopg2.connect(dbname='postgres', host='localhost', user='postgres', password='54321')
#         conn.autocommit = True
#         cur = conn.cursor()
#
#         cur.execute("DROP DATABASE course_work")
#         cur.execute("CREATE DATABASE course_work")
#
#         cur.close()
#         conn.close()
# рекомендации по .env - там все переменные
# https://github.com/skypro-008/github_stats_to_postgres/blob/main/src/main.py


    # my_table = pd.read_sql('select * from my-table-name', connection)
    # another_attempt = psql.read_sql("SELECT * FROM my-table-name", connection)
    # print(my_table)
    # OR
    # print(another_attempt)

        # print(line.rstrip())
        # data = get_employer(line)
        # print(data)

# company_id = '6093775'
# req = requests.get(f'https://api.hh.ru/vacancies/', params={
#     'employer_id': f'{company_id}',
#     'text': 'программист',
#     'only_with_vacancies': True,
#     'only_with_salary': True
# })
# data = req.json()
# count_of_pages = data['pages']  # Узнаем количество страниц вакансий
#
# req.close()
# print(count_of_pages)



# data = get_vacancies(company_name)
# load_db_employees(data)
# with open('./HH_vacancies_.json', 'w') as file:
#     json.dump(data, file, indent=2, ensure_ascii=False)

'''
"published_at"
"salary"["from"]    null[null]
"alternate_url"
"id"
"area"["name"]

  "found": 232,
  "pages": 12,
  "per_page": 20,
  "page": 0,

  "found": 2,
  "pages": 1,
  "per_page": 20,
  "page": 0,


'''