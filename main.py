import json
import logging
import sys

import requests
from bs4 import BeautifulSoup

URL: str = 'https://www.tutu.ru/prigorod/search.php'
HEADERS: dict = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
    "Accept": '*/*'
}
with open('stations.json') as data:
    STATIONS: dict = json.load(data)
LOGGER: logging.Logger = logging.getLogger(__name__)

# Change logging level
LOGGER.setLevel('DEBUG')

LOGGER.addHandler(logging.StreamHandler(sys.stdout))


def get_timetable(params: dict) -> list:
    timetable: list = []

    # Page with link to timetable
    response: requests.Response = requests.get(URL, params, headers=HEADERS)

    if not response.ok:
        LOGGER.critical(f'Something went wrong...\nStatus code: {response.status_code}')
        return timetable

    # Getting the link
    soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')

    if soup.find('div', class_='title_block') is not None:
        name: BeautifulSoup = soup.find('div', class_='center_block').div.p
        if name is None:
            LOGGER.critical('Stations not found!')
        else:
            LOGGER.critical(f'Station "{name.span.text}" is not found!')
        return timetable

    rel_link_to_timetable: str = soup.find('div', class_='b-etrain__date_navigation').a["href"]

    response = requests.get('https://www.tutu.ru' + rel_link_to_timetable, headers=HEADERS)

    if not response.ok:
        LOGGER.critical(f'Something went wrong...\nStatus code: {response.status_code}')
        return timetable

    soup = BeautifulSoup(response.text, 'html.parser')

    table: BeautifulSoup = soup.find('tbody', class_='desktop__timetable__3wEtY')

    if table is None:
        LOGGER.critical('Timetable not found!')
        return timetable

    LOGGER.info('Departure | Arrival  |  Price')
    for tr in table.find_all('tr', class_='desktop__card__yoy03'):
        departure_time: str = tr.find('td', class_='desktop__depTime__2Ue-g').a.text
        arrival_time: str = tr.find('td', class_='desktop__arrTime__1N9Pw').a.text

        price: str = tr.find('td', class_='desktop__price__31Jsd').span.text
        price = price.replace(' ₽', ' RUB')

        timetable.append(
            {
                "departure time": departure_time,
                "arrival time": arrival_time,
                "price": price
            }
        )

        LOGGER.info(f'{departure_time.center(10)}|{arrival_time.center(10)}|{price.center(10)}')

    return timetable


def main():
    st1: str
    st2: str

    if len(sys.argv) > 2:
        st1 = sys.argv[1]
        st2 = sys.argv[2]
    else:
        st1 = input(f'Enter departure station: ')
        st2 = input(f'Enter arrival station: ')

    params: dict = {
        "st1": st1,
        "st2": st2
    }

    timetable: list = get_timetable(params)
    with open('timetable.json', 'w') as tt:
        json.dump(timetable, tt, indent=4)


main()
