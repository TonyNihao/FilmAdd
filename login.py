import requests
from bs4 import BeautifulSoup
import parser

username = 'MyUserName'
password = 'My-Password12$'
url = 'https://LoginUrl'
create_url = 'https://FilmCreateUrl'

film_info = parser.main()

youtube = input('Enter trailer url: ')
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

data = {'_csrf-backend' : token,
             'LoginForm[email]': username,
             'LoginForm[password]' : password,
             'login-button' : ''}


film_param = {
    '_csrf - backend' : token,
    'CinemaFilmsModel[name]' : film_info['name'],
    'CinemaFilmsModel[original_name]' : film_info['alt_name'],
    'CinemaFilmsModel[alias]' : ' ',
    'CinemaFilmsModel[small_desc]' : film_info['description'],
    'CinemaFilmsModel[released_date]' : '2019-12-07',
    'CinemaFilmsModel[premier_status]' : '0',
    'CinemaFilmsModel[type]' : '2', # скоро на экранах - 2, в прокате - 1
    'CinemaFilmsModel[status]' : '0', # 0- неактивный, 1 - активный
    'CinemaFilmsModel[booking_off]' : '0',
    'CinemaFilmsModel[reserve_off]' : '0',
    'CinemaFilmsModel[is_original]' : '0',
    'CinemaFilmsModel[is_expected]' : '0',
    'CinemaFilmsModel[player_code]' : youtube,
    'CinemaFilmsModel[age_limit]' : ' ',
    'CinemaFilmsModel[country_creator]' : '',#film_info['country'],
    'CinemaFilmsModel[country_creator][]' : ['country', 'test', 'just'],
    'CinemaFilmsModel[genres]' : '',#list(film_info['genre']),
    'CinemaFilmsModel[genres][]' : ['genre', 'list', 'test'],
    'CinemaFilmsModel[actors]' : '',#film_info['actors'],
    'CinemaFilmsModel[actors][]' : ['actors', 'test', 'just'],
    'CinemaFilmsModel[director]' : '',#film_info['director'],
    'CinemaFilmsModel[director][]' : ['director', 'test', 'just'],
    'CinemaFilmsModel[screenplay]' : '',#film_info['screenplay'],
    'CinemaFilmsModel[screenplay][]' : ['screenplay', 'test', 'just'],
    'CinemaFilmsModel[movie_time]' : film_info['timing'],
    'CinemaFilmsModel[movie_lang]' : 'Українська',
    'CinemaFilmsModel[movie_subtitle]' : ' ',
    'CinemaFilmsModel[FileCover]' : '',
    'CinemaFilmsModel[FileCover]': '(binary)',
    'CinemaFilmsModel[FilePlayerCover]' : '',
    'CinemaFilmsModel[FilePlayerCover]' : '(binary)',
    'CinemaFilmsModel[FileSlider][]' : '',
    'CinemaFilmsModel[FileSlider][]' : '(binary)',
    'CinemaFilmsModel[content]' : '< p >' + film_info['description'] +'< / p >'
    }

def film_create(data_dec, in_url):
    r = requests.Session()
    response = r.get(in_url, data=data_dec)
    file = open('film_create', 'w')
    file = file.write (response.text)

    return response

def main(in_url, data_dec):
    req = requests.Session()
    response = req.get(in_url, data=data_dec)
    response_status = response.history
    if response_status:
        print ('Login: OK')
    elif response_status == []:
        print('Login: FILED')
    else:
        print('Check errors')






if __name__ == '__main__':
    main(url, data)
    print(film_create(film_param, create_url))
