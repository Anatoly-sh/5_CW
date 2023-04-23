import psycopg2


class DBManager:

    def __init__(self, database: str, params: dict):
        self.database = database
        self.params = params

    def to_make_query(self, query) -> list:
        """
        Обращается к БД с запросом SQL и возвращает результат в виде списка кортежей.
        :param query:
        :return:
        """
        conn = psycopg2.connect(dbname=self.database, **self.params)
        try:
            with conn.cursor() as cur:
                cur.execute(query)
                answer = cur.fetchall()
        finally:
            conn.close()
        return answer

    def get_companies_and_vacancies_count(self):
        """
        Запрашивает в БД список всех компаний и количество вакансий у каждой компании,
        отправляя строку запроса в метод to_make_query.
        :return: Строку SQL-запроса
        """
        answer = self.to_make_query("""
            SELECT company_name, COUNT(*) as vacancies_quantity
            FROM vacancy_param 
            JOIN employers USING(employer_id) 
            GROUP BY company_name 
            ORDER BY vacancies_quantity DESC, company_name
            """)
        return answer

    def get_all_vacancies(self):
        """
        Запрашивает в БД список всех вакансий у каждой компании,
        отправляя строку запроса в метод to_make_query.
        :return: Строку SQL-запроса.
        """
        answer = self.to_make_query("""
            SELECT employers.company_name, vacancy_name, salary_from, url 
            FROM vacancy_param 
            JOIN employers USING(employer_id) 
            WHERE salary_from IS NOT NULL 
            ORDER BY salary_from DESC, vacancy_name
            """)
        return answer

    def get_avg_salary(self):
        """
        Запрашивает в БД среднюю зарплату по вакансиям,
        отправляя строку запроса в метод to_make_query.
        :return: Строку SQL-запроса.
        """
        answer = self.to_make_query("""
            SELECT ROUND(AVG(salary_from)) as average_salary 
            FROM vacancy_param
            """)
        return answer

    def get_vacancies_with_higher_salary(self):
        """
        Запрашивает в БД список всех вакансий, у которых зарплата выше средней по всем вакансиям,
        отправляя строку запроса в метод to_make_query.
        :return: Строку SQL-запроса.
        """
        answer = self.to_make_query("""
            SELECT vacancy_name, salary_from FROM vacancy_param 
            WHERE salary_from > (SELECT AVG(salary_from) FROM vacancy_param) 
            ORDER BY salary_from DESC, vacancy_name
            """)
        return answer

    def get_vacancies_with_keyword(self, keyword: str):
        """
        Запрашивает в БД список всех вакансий,
        в названии которых содержатся переданные в метод слова, например “python”,
        отправляя строку запроса в метод to_make_query.
        :return: Строку SQL-запроса.
        """
        answer = self.to_make_query(f"""
            SELECT vacancy_name FROM vacancy_param 
            WHERE vacancy_name LIKE '%{keyword}%'
            ORDER BY vacancy_name
            """)
        return answer

"""
SELECT vacancy_name FROM vacancy_param
WHERE vacancy_name LIKE '{keyword}' 
ORDER BY vacancy_name;
"""