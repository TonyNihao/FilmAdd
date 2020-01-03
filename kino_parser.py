import requests
from bs4 import BeautifulSoup
from datetime import datetime

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

def genre_converter(genre):
    '''
    Принимает строку с названием жанра и выдает соответствующий номер.
    Возвращает номер
    '''
    genres = {'аніме': 1, 'біографічний': 2, 'бойовик': 3, 'вестерн': 4, 'військовий': 5,
              'детектив': 6, 'дитячий': 7, 'документальний': 8, 'драма': 9, 'історичний': 10,
              'кінокомікс': 11, 'комедія': 12, 'концерт': 13, 'короткометражний': 14, 'кримінал': 15,
              'мелодрама': 16, 'містика': 17, 'музика': 18, 'науковий':19 , 'пригоди': 20 }
    genre_index = []
    for i in genre:
        for j in genres:
            if i[1:] == j:  # начинаем с первого элемента т.к. парсер возвращает название жанра с пробелом
                genre_index.append(genres[j])
    return genre_index
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

    film_info = {'name': '', 'alt-name': '', 'country': '',
                 'genre': '', 'director': ' ', 'screenplay': '',
                 'actors': '', 'premier': '2019-10-10', 'timing': '', 'description': ''}

    soup = BeautifulSoup(html, 'lxml')
    info = soup.find('div', class_='content hreview-aggregate')

    film_name = info.find('h1', class_='margin-left item')
    name = film_name.find('span', class_='fn').text
    film_info['name'] = name
    try:
        alt_name = film_name.find('span', class_='alt-name').text
        film_info['alt_name'] = alt_name
    except:
        alt_name = ''
        film_info['alt_name'] = alt_name

    film_detail = info.find('div', class_='left-side')
    film_detail = film_detail.find('div', class_='film-detail')
    film_detail_text = film_detail.find('div', class_='text')
    film_detail_text = film_detail_text.find_all('p')
    film_image = film_detail.find('div', class_='thumbHolder')
    film_image = film_image.find('a', class_='photo').get('href')  # ссылка на скачивание фото
    film_image = url + film_image

    for detail in film_detail_text:
        detail_text = detail.text.split(':')

        if detail_text[0] == 'Країна, рік':
            country = [0]
            country[0] = detail_text[1]
            film_info['country'] = country

        elif detail_text[0] == 'Жанр':

            genre = detail_text[1]
            genre = genre.split(',')
            genre = genre_converter(genre)
            film_info['genre'] = genre
        elif detail_text[0] == 'Режисер':
            director = [0]
            director[0] = detail_text[1]
            film_info['director'] = director
        elif detail_text[0] == 'Сценарист':
            screenplay = [0]
            screenplay[0] = detail_text[1]
            film_info['screenplay'] = screenplay
        elif detail_text[0] == 'Актори':
            actors = [0]
            actors_str = detail_text[1]
            actors_str = actors_str.split('...')  # Парсер возвращает список актеров в фосмате "короткий" - "полный"
            actors[0] = actors_str[1]
            film_info['actors'] = actors
        elif detail_text[0] == "Прем'єра в Україні":
            premier = detail_text[1]
            premier = premier[1:].split('.')
            premier = premier[::-1]
            premier = premier[0]+'-'+premier[1]+'-'+premier[2]  # Переворачивает формат даты
            film_info['premier'] = premier
        elif detail_text[0] == 'Тривалість':
            timing = detail_text[1]
            timing = timing.split(' ')
            timing = timing[1] + timing[2] + ' ' + timing[3]   # пример - 2год. 2
            film_info['timing'] = timing
    try:
        description = soup.find('div', class_='description')
        description = description.find('p').text
        film_info['description'] = description
    except film_info:
        film_info['description'] = 'Description'
        print('description error')

    request_img = requests.get(film_image)
    # name_img = "{0}.jpg".format((film_info['alt_name']).replace("'", "1") + str(datetime.now())[-6:-1])
    # name_img = name_img
    # image = open(name_img, 'wb')
    # image.write(request_img.content)
    # image.close()


    return film_info


def main():
    film_page = url + get_film_url(search_url)

    info = get_film_info(get_html(film_page))
    return info


if __name__ == '__main__':
    main()
