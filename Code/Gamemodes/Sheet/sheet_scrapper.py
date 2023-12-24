"""
This is the functionality required for loading into memory the data from the Global Players sheet.
Using webscrapping as the sheet does not belong to Jabro.
"""

import requests
from bs4 import BeautifulSoup


_SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/u/0/d/155CSxnOt54M16DvY7vNeBuKnup1WVfX8ARoOqSFcCZ0/gviz/tq?tqx=out:html&tq&gid=1'


def get_global_players() -> list[tuple[str, str, str, str, str]]:
    """
    Method to retrieve the information from the global players spreadsheet.

    Return:
    -----------
    A list of tuples, each of them containing the next 5 elements (ordered as follow):
    - AMQ Name: `str`
        Tha AMQ name of the player that the list belongs to.
    - List Name: `str`
        The name of the list (in Anilist / MyAnimeList).
    - List From: `str`
        Whether the list is from Anilist or MyAnimeList.
    - List Sections: `str`
        The sections that must be used when loading the list into your AMQ list.
    - Comment: `str`
        A comment that the player has left as additional information.
    """
    html_content = requests.get(_SPREADSHEET_URL).text
    soup = BeautifulSoup(html_content, 'lxml')
    global_players_table = soup.find_all('table')[0]
    
    rows = global_players_table.find_all('tr')
    global_players = [
        [cell.text for cell in row.find_all('td')]
        for row in rows
    ]

    return [
        tuple(global_player[1:6])
        for global_player in global_players
        if global_player[1] not in {'\xa0', ''}
    ]