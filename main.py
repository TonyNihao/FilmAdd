import requests
from bs4 import BeautifulSoup
import kino_parser
from datetime import datetime
username = 'MyUsername'   #input('Enter user name: ')
password = 'My-super-pa$$-worD'     #input ('Enter password: ')
youtube = input('Enter trailer url: ')

url = 'https://CCadminURL'
create_url = 'https://CCFilmCreateURL'

def get_html(url):
    r = requests.get(url)
    return r.text

def set_token(html):
    soup = BeautifulSoup(html, 'lxml')
    find_token = soup.find('div', class_='panel panel-info mt10 br-n bg-gradient-1 mw500 mauto')
    find_token = find_token.find('input', type='hidden')
    find_token = find_token.get('value')
    return find_token
token = set_token(get_html(url))

data = {'_csrf-backend': token,
        'LoginForm[email]': username,
        'LoginForm[password]': password,
        'login-button': ''}

film_info = kino_parser.main()

def make_alias(name):
    if len(name) == 0:
        alias = 'film' + str(datetime.now())
    else:
        alias = name.replace(' ', '')
    return alias

film_param = {
    '_csrf - backend': token,
    'CinemaFilmsModel[name]': film_info['name'],
    'CinemaFilmsModel[original_name]': film_info['alt_name'],
    'CinemaFilmsModel[alias]': make_alias(film_info['alt_name']),
    'CinemaFilmsModel[small_desc]': film_info['description'],
    'CinemaFilmsModel[released_date]': film_info['premier'],
    'CinemaFilmsModel[premier_status]': '1',
    'CinemaFilmsModel[type]': '2',  # скоро на экранах - 2, в прокате - 1
    'CinemaFilmsModel[status]': '0',  # 0- неактивный, 1 - активный
    'CinemaFilmsModel[booking_off]': '0',
    'CinemaFilmsModel[reserve_off]': '0',
    'CinemaFilmsModel[is_original]': '0',
    'CinemaFilmsModel[is_expected]': '0',
    'CinemaFilmsModel[player_code]': youtube,
    'CinemaFilmsModel[age_limit]': '',
    'CinemaFilmsModel[country_creator]': '',
    'CinemaFilmsModel[country_creator][]': film_info['country'],
    'CinemaFilmsModel[genres]': '',
    'CinemaFilmsModel[genres][]': film_info['genre'],
    'CinemaFilmsModel[actors]': '',
    'CinemaFilmsModel[actors][]': film_info['actors'],
    'CinemaFilmsModel[director]': '',
    'CinemaFilmsModel[director][]': film_info['director'],
    'CinemaFilmsModel[screenplay]': '',
    'CinemaFilmsModel[screenplay][]': film_info['screenplay'],
    'CinemaFilmsModel[movie_time]': film_info['timing'],
    'CinemaFilmsModel[movie_lang]': 'Українська',
    'CinemaFilmsModel[movie_subtitle]': '',
    'CinemaFilmsModel[FileCover]': '',#image,
    'CinemaFilmsModel[FileCover]': '',#image,
    'CinemaFilmsModel[FilePlayerCover]': '',
    'CinemaFilmsModel[FilePlayerCover]': '(binary)',
    'CinemaFilmsModel[FileSlider][]': '',
    'CinemaFilmsModel[FileSlider][]': '(binary)',
    'CinemaFilmsModel[content]': film_info['description']
    }

def film_create(data_dec, in_url):
    r = requests.Session()
    response = r.get(in_url, data=data_dec)
    
    return response

def main(in_url, data_dec):
    req = requests.Session()
    response = req.get(in_url, data=data_dec)
    response_status = response.history
    if response_status:
        print('Login: OK')
    elif response_status == []:
        print('Login: FILED')
    else:
        print('Check errors')

if __name__ == '__main__':
    main(url, data)
    print(film_create(film_param, create_url))