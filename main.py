import sys
import re
import requests
from bs4 import BeautifulSoup



def hh_parsing(headers, search_quantity_of_vac):

    HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'

    # Получите HTML-код страницы hh
    res = requests.get(HOST, headers=headers)
    # print (res)
    print('------')
    if res.status_code == 200:
        print("Запрос прошел успешно")
    else:
        print(f"Ошибка запроса, статус-код {res.status_code}")


    soup = BeautifulSoup(res.text, 'html.parser')
    #print(soup)

    with open('parsed_page.html', 'w', encoding='utf-8') as html_file:
        html_file.write(soup.prettify())


    # Найти все элементы с атрибутом data-qa="serp__novafilter-title"
    city_elements = soup.find_all('span', {'data-qa': 'serp__novafilter-title'})

    # Извлечь текст из найденных элементов и привести его к нижнему регистру
    city_texts = [element.text.strip() for element in city_elements]
    # print(city_texts)

    found_cities =[]

    for city_text in city_texts:
        for city in SEARCH_CITIES:
            if city in city_text:
                found_cities.append(city)

    # print(found_cities)

    # Проверить, что хотя бы один из текстов городов соответствует одному из городов из SEARCH_CITIES
    if any(found_cities):
        print(f"На странице найдены города из SEARCH_CITIES: {found_cities}")
    else:
        print("На странице не найдены города из SEARCH_CITIES.")
        sys.exit()  # Завершаем программу

    # Извлекаем вакансии
    vacation_elements = soup.find_all('a', class_='serp-item__title')

    found_vacancies = 0
    parced_vacancies = []

    for vacation_element in vacation_elements:
        vacation_name = vacation_element.text.strip().lower()
        vacation_link = vacation_element['href']
        words = re.findall(r'\w+', vacation_name)  # Разделение текста на слова
        print('---------Ищем вакансии по названию----')
        print('в названии данной вакансии есть такие слова:',  words)
        # print('Имя и ссылка на вакансию',vacation_name, vacation_link)

        for keyword in SEARCH_WORDS:
            if keyword in words:
                found_vacancies += 1
                print(f"Найдена вакансия с ключевым словом {keyword}: {vacation_name}, ссылка : {vacation_link}")
                #Создаем словарь для вакансии
                vacancy_info = {'vacancy-name': vacation_name, 'vacancy-link': vacation_link}
                parced_vacancies.append(vacancy_info)


        # Проверяем, если достигли нужного количества совпадений
        if found_vacancies >= search_quantity_of_vac:
            break  # Прерываем цикл, если найдено достаточно вакансий

    result_vacancies =[]
    final_vacations_count = 0

    for parced_vacancy in parced_vacancies:
        name = parced_vacancy['vacancy-name']
        link = parced_vacancy['vacancy-link']
        res = requests.get(link, headers=headers)

        print('------')
        if res.status_code == 200:
            print("Запрос по ссылке на вакансию прошел успешно")
        else:
            print(f"Ошибка запроса, статус-код {res.status_code}")

        vacancy_soup = BeautifulSoup(res.text, 'html.parser')
        vacancy_description = vacancy_soup.find('div', {'data-qa': 'vacancy-description'})

        text_fork = ''
        text_company = ''
        text_city = ''
        description_text_lower = ''  # Инициализируем переменную перед использованием
        # print (vacancy_description)

        if vacancy_description is not None:
            description_text = vacancy_description.get_text(separator=" ")
            description_text_lower = description_text.lower()

            vacancy_fork = vacancy_soup.find('span', class_='bloko-header-section-2 bloko-header-section-2_lite')
            if vacancy_fork:
                text_fork = vacancy_fork.text
                print(f"Вилка ЗП: {text_fork}")

            vacancy_company = vacancy_soup.find('a', {'data-qa': 'vacancy-company-name'})
            if vacancy_company:
                text_company = vacancy_company.text
                print(f"Название Компании: {text_company}")

            vacancy_city = vacancy_soup.find('p', {'data-qa': 'vacancy-view-location'})
            if vacancy_city:
                city_words = vacancy_city.text.split()
                text_city = city_words[0].strip()
                print(f"Название города: {text_city}")

            #is_match_found = False

            for key in SEARCH_DESCRIP:
                if key.lower() in description_text_lower:
                    is_match_found = True
                    break

            #if is_match_found:
                result_vacancy = {
                    'Вакансия': name,
                    'Ссылка': link,
                    'Компания': text_company,
                    'Город': text_city,
                    'Вилка ЗП': text_fork
                }
                print(f" Вот одна из искомых вакансий {result_vacancy}")
                result_vacancies.append(result_vacancy)
                final_vacations_count += 1

    return   result_vacancies, final_vacations_count



if __name__ == "__main__":

    search_quantity_of_vac = 9

    # Пасинг нужен поиском по "Python" и городами "Москва" и "Санкт-Петербург". ссылка вот: https://spb.hh.ru/search/vacancy?text=python&area=1&area=2
    SEARCH_WORDS = ['дизайн', 'фото', 'web', 'python', 'art']
    SEARCH_CITIES = ['Москва', 'Санкт-Петербург']
    SEARCH_DESCRIP = ['Django', 'Flask']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', }

    result = hh_parsing(headers, search_quantity_of_vac)

    #
    # print("----")
    # print(f"-----------Результирующий список вакансий в количестве : {result[1]}")
    # for element in result[0]:
    #     print(element)

    # Создаем пустое множество, в которое будем добавлять кортежи (ключ, значение)
    result_vacancies_set = set()

    # Проходим по каждому словарю в списке и добавляем в множество кортежи (ключ, значение)
    for dictionary in result[0]:
        # Получаем элементы словаря в виде кортежей (ключ, значение) и добавляем их в множество
        items = tuple(dictionary.items())
        result_vacancies_set.add(items)
    final_quantity_of_vac = len(result_vacancies_set)
    # Выводим полученное множество
    print(f"--------Итого количество уникальных вакансий = {final_quantity_of_vac}")
    for el in result_vacancies_set:
        print(el)
