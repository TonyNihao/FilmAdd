import requests
from bs4 import BeautifulSoup



query = input('Enter search query ')  # ввод от пользователя запроса искомой информации
url = 'https://kinoafisha.ua'      # основной адрес сайта
search_url = 'https://kinoafisha.ua/ua/search?query=' + query + '&category=site'
def get_html(url):
    '''
    Функция принимает адрес в виде ссылки возвращает HTML код
    в виде текста
    '''
    r = requests.get(url)
    return r.text

def get_film_url(url):
    '''
    Функция принимает адрес поискового запроса
    Возвращает адрес страницы в транскрипции
    '''
    soup = BeautifulSoup(get_html(url), 'lxml')
    film_url = soup.find('div', class_='content')
    film_url = film_url.find('div', class_='left-side')
    film_url = film_url.find('div', class_='results-search')
    film_url = film_url.find('div', class_='list-films')
    film_url = film_url.find('div', class_='text')
    film_url = film_url.find('a')
    film_url = film_url.get('href')               # конечный урл формата /ua/<транскрипция>
    return film_url

def get_film_info(html):
    '''
    Функция выполняет поиск и запись информации о фильме
    -Название
    -Оригинальное название
    -Страна, год
    -Жанр
    -Режисер
    -Сценарист
    -Актеры
    -Премьера в Украине
    -Продолжительность фильма
    Если параметра нет либо он не найден, возвращает пустую строку
    '''
    film_info = {}                #пустой список для записи информации о фильме

    soup = BeautifulSoup(html, 'lxml')
    info = soup.find('div', class_='content hreview-aggregate vevent')

    film_name = info.find('h1', class_='margin-left item')
    name = film_name.find('span', class_='fn').text
    film_info['name'] = name
    try:
        alt_name = film_name.find('span', class_='alt-name').text
        film_info['alt_name'] = alt_name
    except:
        alt_name = ' '
        film_info['alt_name'] = alt_name
    film_detail = info.find('div', class_='left-side')
    film_detail = film_detail.find('div', class_='film-detail')
    film_detail = film_detail.find('div', class_='text')
    film_detail = film_detail.find_all('p')


    for detail in film_detail:
        detail_text = detail.text.split(':')

        if detail_text[0] == 'Країна, рік':
            film_info['country'] = detail_text[1]
        elif detail_text[0] == 'Жанр':
            film_info['genre'] = detail_text[1]
        elif detail_text[0] == 'Режисер':
            film_info['director'] = detail_text[1]
        elif detail_text[0] == 'Сценарист':
            film_info['screenplay'] = detail_text[1]
        elif detail_text[0] == 'Актори':
            film_info['actors'] = detail_text[1]
        elif detail_text[0] == "Прем'єра в Україні":
            film_info['premier'] = detail_text[1]
        elif detail_text[0] == 'Тривалість':
            film_info['timing'] = detail_text[1]

    description = soup.find('div', class_='description')
    description = description.find('p').text
    film_info['description'] = description

    return film_info

def main():
    film_page = url + get_film_url(search_url)

    info = get_film_info(get_html(film_page))
    return info