import shutil
import requests

url = 'https://kinoafisha.ua/upload/2017/09/films/7972/205n4fd9malefisenta-2.jpg'

response = requests.get(url, stream=True)
with open('image.jpg', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)

del response