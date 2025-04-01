"""
This is the functionality required for loading into memory the data from the Global Players sheet using Google's API.
Sheet: https://docs.google.com/spreadsheets/d/155CSxnOt54M16DvY7vNeBuKnup1WVfX8ARoOqSFcCZ0/edit?gid=1988193305#gid=1988193305
"""
import gspread

_MAIN_SHEET_KEY = '155CSxnOt54M16DvY7vNeBuKnup1WVfX8ARoOqSFcCZ0'

def _get_all_players(all_players_worksheet: gspread.worksheet.Worksheet) -> list[tuple[str, str, str, str, str]]:
    """
    Method to retrieve the information from all players in the spreadsheet.

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
    all_players = []
    check_set = {'\xa0', '', None}

    # NOTE skipping row 0 as it is the header row
    for row in all_players_worksheet.get_all_values()[1:]:
        """
        row[1] = B Column = AMQ Name
        row[2] = C Column = List Name
        row[4] = E Column = List From
        row[5] = F Column = List Sections
        row[6] = G Column = Comment
        """
        # Check if it is an empty row
        if row[1] in check_set or row[2] in check_set or row[4] in check_set or row[5] in check_set:
            # In case it is not an empty row, but it is missing some information, we print it
            if row[1] not in check_set or row[2] not in check_set or row[4] not in check_set or row[5] not in check_set:
                print(f'ALL PLAYERS: Skipping row ({row[1]}, {row[2]}, {row[4]}, {row[5]}) due to containing some empty value')
            continue

        all_players.append((row[1], row[2], row[4], row[5], row[6]))
    
    #print(len(all_players))
    return all_players

def _get_active_players(active_players_worksheet: gspread.worksheet.Worksheet) -> list[tuple[str, str, str, str, str]]:
    """
    Method to retrieve the information from the active players in the spreadsheet.

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
    active_players = []
    check_set = {'\xa0', '', None}

    # NOTE skipping row 0 as it is the header row
    for row in active_players_worksheet.get_all_values()[1:]:
        """
        row[2] = C Column = AMQ Name
        row[3] = D Column = List Name
        row[5] = F Column = List From
        row[6] = G Column = List Sections
        row[7] = H Column = Comment
        """
        # Check if it is an empty row
        if row[2] in check_set or row[3] in check_set or row[5] in check_set or row[6] in check_set:
            # In case it is not an empty row, but it is missing some information, we print it
            if row[2] not in check_set or row[3] not in check_set or row[5] not in check_set or row[6] not in check_set:
                print(f'ACTIVE PLAYERS: Skipping row ({row[2]}, {row[3]}, {row[5]}, {row[6]}) due to containing some empty value')
            continue

        active_players.append((row[2], row[3], row[5], row[6], row[7]))
    
    #print(len(active_players))
    return active_players


def get_global_players_data(client: gspread.Client) -> tuple[
        list[tuple[str, str, str, str, str]],
        list[tuple[str, str, str, str, str]]
    ]:
    """
    Method to retrieve the information from the global players spreadsheet.

    Return:
    -----------
    Two (2) list of tuples, each of the lists containing the next 5 elements (ordered as follow):
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
    spreadsheet = client.open_by_key(_MAIN_SHEET_KEY)

    # NOTE skipping worksheet 0 as it is a hidden "Archive" sheet that we will ignore
    input_data, active_players, inactive_players = (spreadsheet.get_worksheet(i) for i in range(1, 4))
    #print(input_data.title, active_players.title, inactive_players.title)
    
    # TODO store inactive players data?
    all_players = _get_all_players(input_data)
    active_players = _get_active_players(active_players)
    
    return all_players, active_players