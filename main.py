import json

import requests
from bs4 import BeautifulSoup

URL: str = 'https://www.tutu.ru/spb/rasp.php'
HEADERS: dict = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
    "Accept": '*/*'
}

with open('stations.json') as data:
    stations: dict = json.load(data)

departure_st: str = input('Enter departure station: ')
arrival_st: str = input('Enter arrival station: ')

departure_options: list = []
arrival_options: list = []

for name in stations.keys():
    if departure_st in name:
        departure_options.append(name)
    if arrival_st in name:
        arrival_options.append(name)

if not departure_options:
    print('Departure station not found.')
if not arrival_options:
    print('Arrival station not found.')


def choose_station(options: list):
    for i, v in enumerate(options):
        print(f'{i + 1}. {v}.')

    chosen: str = input()
    if not chosen.isdigit() or int(chosen) - 1 not in range(len(options)):
        print('Invalid number!')
        choose_station(options)

    return options[int(chosen) - 1]


if len(departure_options) > 1:
    print('Please, choose departure station from the list below.')
    departure_st = choose_station(departure_options)
else:
    departure_st = departure_options[0]
if len(arrival_options) > 1:
    print('Please, choose arrival station from the list below.')
    arrival_st = choose_station(arrival_options)
else:
    arrival_st = arrival_options[0]

params: dict = {
    "st1": stations[departure_st],
    "st2": stations[arrival_st]
}

r = requests.get(URL, params, headers=HEADERS)
if not r.ok:
    print(f'Something went wrong...\nStatus code: {r.status_code}')

with open('1.html', 'wb') as h:
    h.write(r.content)

soup: BeautifulSoup = BeautifulSoup(r.text, 'html.parser')
table: BeautifulSoup = soup.find('tbody', class_='desktop__timetable__3wEtY')

timetable: list = []

print('Departure | Arrival  |  Price ')

for tr in table.find_all('tr', class_='desktop__card__yoy03'):
    departure_time: str = tr.find(class_='desktop__cell__2cdVW desktop__depTime__2Ue-g').a.text
    arrival_time: str = tr.find(class_='desktop__cell__2cdVW desktop__arrTime__1N9Pw').a.text
    price: str = tr.find(class_='t-txt-s desktop__cell__2cdVW desktop__price__31Jsd').span.text.replace(' ₽', ' RUB')
    timetable.append(
        {
            "departure time": departure_time,
            "arrival time": arrival_time,
            "price": price
        }
    )
    print(f'{departure_time.center(10)}|{arrival_time.center(10)}|{price.center(8)}')

with open('timetable.json', 'w') as tt:
    json.dump(timetable, tt, indent=4)
