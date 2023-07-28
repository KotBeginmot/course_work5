from typing import Any

import psycopg2
import requests

API_HH = 'https://api.hh.ru/employers/'


def get_companies(companies: list) -> list[dict[str, Any]]:
    """Функция для получения списка работодателей и их вакансий с платформы HH"""
    companies_list = []
    for company in companies:
        url = f'{API_HH}{company}'
        companies_response = requests.get(url).json()
        vacancy_response = requests.get(companies_response['vacancies_url']).json()
        companies_list.append({
            'company': companies_response,
            'vacancies': vacancy_response['items']
        })

    return companies_list


def filter_salary(salary):
    """Функция для установки фильтра по параметру заработная плата"""
    if salary is not None:
        if salary['from'] is not None and salary['to'] is not None:
            return round((salary['from'] + salary['to']) / 2)
        elif salary['from'] is not None:
            return salary['from']
        elif salary['to'] is not None:
            return salary['to']
    return None


def create_database(data_base_name: str, params: dict) -> None:
    """Функция для создания базы данных"""
    conn = psycopg2.connect(dbname=data_base_name, **params)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(f"DROP DATABASE IF EXISTS {data_base_name}")
        cur.execute(f"CREATE DATABASE {data_base_name}")
    conn.close()

    conn = psycopg2.connect(dbname=data_base_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
                    CREATE TABLE companies (
                        company_id SERIAL PRIMARY KEY,
                        company_title VARCHAR(255) NOT NULL
                    )
                """)

        cur.execute("""
                        CREATE TABLE vacancies (
                            vacancy_id SERIAL PRIMARY KEY,
                            company_id int REFERENCES companies(company_id),
                            vacancy_title VARCHAR(255) NOT NULL,
                            salary INTEGER,
                            url TEXT NOT NULL 
                        )
                    """)
    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], data_base_name: str, params: dict) -> None:
    """Функция для добавления информаций по вакансиям и компаниям в таблицы"""
    conn = psycopg2.connect(dbname=data_base_name, **params)

    with conn.cursor() as cur:
        for company in data:
            cur.execute(
                """
                INSERT INTO companies (company_title)
                VALUES (%s)
                RETURNING company_id
                """,
                (company['company']['name'],))
            company_id = int(cur.fetchone()[0])
            for vacancy in company['vacancies']:
                salary = filter_salary(vacancy['salary'])
                cur.execute("""
                INSERT INTO vacancies (company_id, vacancy_title, salary, url)
                VALUES (%s, %s, %s, %s)""",
                            (company_id, vacancy['name'], salary,
                             vacancy['alternate_url']))
    conn.commit()
    conn.close()
