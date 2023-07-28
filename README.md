# course_work5

В БД две таблицы:
1. companies:
company_id;
company_title.
2. vacancies:
vacancy_id;
company_id;
vacancy_title;
salary;
url

Класс для работы с БД и выводом информаций с таблиц:
DBManager.py
Функций для получения информаций о компаниях, создания БД, и заполнения таблиц с платформы HH:
utils.py
Скрипт подключения к Postgresql:
config.py
Импортируемые вспомогательные пакеты:
requests
psycopg2
