from src.DBManager import DBManager
from src.config import config
from src.utils import get_companies, create_database, save_data_to_database

PARAMS = config()
DATA_BASE_NAME = 'data'


def main():
    companies_id = ['195398', '4181', '4484134', '4496', '78638', '4019151', '80660', '6082361', '2489601',
                    '740349']  # id компаний
    companies = get_companies(companies_id)  # Получение списка работодателей и их вакансий с платформы HeadHunter
    create_database(DATA_BASE_NAME, PARAMS)  # Создание базы данных
    save_data_to_database(companies, DATA_BASE_NAME,
                          PARAMS)  # Добавление информаций по вакансиям и компаниям в таблицы"


data_base = DBManager(DATA_BASE_NAME)

if __name__ == "__main__":
    main()
    print(data_base.get_all_vacancies())
