import requests
from bs4 import BeautifulSoup


# Пасинг нужен поиском по "Python" и городами "Москва" и "Санкт-Петербург". ссылка вот: https://spb.hh.ru/search/vacancy?text=python&area=1&area=2
SEARCH_WORDS = ['дизайн', 'фото', 'web', 'python', 'art']
SEARCH_CITIES = ['Москва', 'Санкт-Петербург']

# Получите HTML-код страницы с хабами
res = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2')

if res.status_code == 200:
    print("Запрос прошел успешно")
else:
    print(f"Ошибка запроса, статус-код {res.status_code}")

soup = BeautifulSoup(res.text, 'html.parser')
print(soup)

# Извлекаем вакансии
vacation_elements = soup.find_all('span', class_='serp-item__title')
print(vacation_elements)
for vacation_element in vacation_elements:
    vacation_name = vacation_element.text.lower()
    #found = False  # Флаг, указывающий, найдено ли совпадение

    for keyword in SEARCH_WORDS:
        n = 0
        while n < 101:

            if keyword in vacation_name:
                # Выводите информацию о вакансии, которая содержит желаемое ключевое слово
                print(f"Найдена вакансия с ключевым словом '{keyword}': {vacation_name}")
            n+=1
                #found = True
                #break
    # if found:
    #     break  # Прерываем внешний цикл, если найдено совпадение

# # Получите HTML-код страницы с постами
# ret = requests.get('https://habr.com/ru/all/')
#
# soup = BeautifulSoup(ret.text, 'html.parser')
# #print(soup)
#
# # Извлекаем посты
# post_elements = soup.find_all('article', class_='post')
# for post_element in post_elements:
#     # Извлекаем информацию о посте, например, заголовок и ссылку
#     title_element = post_element.find('a', class_='post__title_link')
#     if title_element:
#         print('Заголовок:', title_element.text)
#         print('Ссылка:', title_element['href'])