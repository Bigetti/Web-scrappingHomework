import requests
from fake_headers import Headers
from bs4 import BeautifulSoup

def get_headers():
    headers = Headers(browser="firefox", os='win')
    return headers.generate()

def hh_parsing_rubbles():
    HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
    response_vacancies = requests.get(HOST, headers=get_headers())
    response_vacancies.raise_for_status()  # Проверка на ошибки при запросе
    soup = BeautifulSoup(response_vacancies.text, 'lxml')
    
    vacancies_list = soup.find('div', class_='vacancy-serp')
    
    if vacancies_list is not None:
        vacancies = vacancies_list.find_all('div', class_='vacancy-serp-item')
    else:
        print("Список вакансий не найден на странице.")
        return []

    parsed = []

    for vacancy in vacancies:
        title = vacancy.find('a', class_='bloko-link HH-LinkModifier')
        link = title['href']

        response = requests.get(link, headers=get_headers())
        response.raise_for_status()  # Проверка на ошибки при запросе
        vacancy_article = BeautifulSoup(response.text, 'lxml')
        vacancy_description = vacancy_article.find('div', {'data-qa': 'vacancy-description'})
        
        if vacancy_description is not None:
            description_text = vacancy_description.get_text(separator=" ")
        else:
            description_text = "Description not found"

        if ('django' in description_text.lower()) or ('flask' in description_text.lower()):
            fork = vacancy.find('span', class_='bloko-header-3')
            if fork is not None:
                fork = fork.text.strip()
            else:
                fork = 'з/п не указана'
            company = vacancy.find('a', class_='bloko-link bloko-link_secondary')
            if company is not None:
                company = company.text.strip()
            else:
                company = 'Компания не указана'
            city = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-address'})
            if city is not None:
                city = city.text
            else:
                city = 'Город не указан'
            
            item = {
                'Ссылка': link,
                'Вилка зп': fork,
                'Компания': company,
                'Город': city,
                'Описание': description_text
            }
            parsed.append(item)
    return parsed

if __name__ == "__main__":
    parsed_rub = hh_parsing_rubbles()
    for item in parsed_rub:
        print(item)
        