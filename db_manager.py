import psycopg2


class DBManager:
    conn = None

    def __init__(self, host='localhost', port=5433, database='five_cw', user='postgres', password='12345'):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.conn = psycopg2.connect(host=self.host, 
                                     port=self.port, 
                                     database=self.database, 
                                     user=self.user, 
                                     password=self.password)


@staticmethod
def get_companies_and_vacancies_count():
    """
    Получает список всех компаний и количество вакансий у каждой компании.
    :return:
    """
    try:
        # conn.autocommit = True
        with DBManager.conn:
            # my_table = psql.read_sql('SELECT * FROM employees', conn)
            cur = DBManager.conn.cursor()
            cur.execute("DROP TABLE IF EXISTS employees, vacancy_param")


        DBManager.conn.commit()
    finally:
        DBManager.conn.close()
    print('Таблицы в БД "five_cw" созданы')


@staticmethod
def get_all_vacancies():
    """
    Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
    :return:
    """
    ...


@staticmethod
def get_avg_salary():
    """
    Получает среднюю зарплату по вакансиям.
    :return:
    """
    ...


@staticmethod
def get_vacancies_with_higher_salary():
    """
    Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
    :return:
    """
    ...


@staticmethod
def get_vacancies_with_keyword():
    """
    Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
    :return:
    """
    ...
