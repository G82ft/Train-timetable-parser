import json
import logging
import sys

import requests
from bs4 import BeautifulSoup

URL: str = 'https://www.tutu.ru/spb/rasp.php'
HEADERS: dict = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
    "Accept": '*/*'
}
with open('stations.json') as data:
    STATIONS: dict = json.load(data)
LOGGER: logging.Logger = logging.getLogger(__name__)


def choose_station(options: list, type_of_st: str) -> str:
    if not options:
        LOGGER.critical(f'{type_of_st.capitalize()} station not found. Please check for errors in station names.')
        raise KeyError

    for i, v in enumerate(options):
        print(f'{i + 1}. {v}.')

    chosen: str = input()
    if not chosen.isdigit() or int(chosen) - 1 not in range(len(options)):
        LOGGER.error('Invalid number!')
        choose_station(options, type_of_st)

    return options[int(chosen) - 1]


def get_stations_id(type_of_st: str) -> str:
    st: str = input(f'Enter {type_of_st} station: ')

    options: list = []

    for name in STATIONS.keys():
        if st.lower() in name.lower:
            options.append(name)

    if len(options) > 1:
        LOGGER.info('Please, choose departure station from the list below.')
        st = choose_station(options, type_of_st)
    else:
        st = options[0]

    return STATIONS[st]


def get_timetable(params: dict) -> list:
    r: requests.Response = requests.get(URL, params, headers=HEADERS)
    if not r.ok:
        LOGGER.critical(f'Something went wrong...\nStatus code: {r.status_code}')

    soup: BeautifulSoup = BeautifulSoup(r.text, 'html.parser')
    table: BeautifulSoup = soup.find('tbody', class_='desktop__timetable__3wEtY')

    timetable: list = []

    LOGGER.info('Departure | Arrival  |  Price ')
    for tr in table.find_all('tr', class_='desktop__card__yoy03'):
        departure_time: str = tr.find(class_='desktop__cell__2cdVW desktop__depTime__2Ue-g').a.text
        arrival_time: str = tr.find(class_='desktop__cell__2cdVW desktop__arrTime__1N9Pw').a.text

        price: str = tr.find(class_='t-txt-s desktop__cell__2cdVW desktop__price__31Jsd').span.text
        price = price.replace(' ₽', ' RUB')

        timetable.append(
            {
                "departure time": departure_time,
                "arrival time": arrival_time,
                "price": price
            }
        )

        LOGGER.info(f'{departure_time.center(10)}|{arrival_time.center(10)}|{price.center(8)}')

    return timetable


def main():
    st1: str
    st2: str

    if len(sys.argv) > 2:
        st1 = sys.argv[1]
        st2 = sys.argv[2]
    else:
        st1 = get_stations_id('departure')
        st2 = get_stations_id('arrival')

    params: dict = {
        "st1": st1,
        "st2": st2
    }

    timetable: list = get_timetable(params)
    with open('timetable.json', 'w') as tt:
        json.dump(timetable, tt, indent=4)


main()
