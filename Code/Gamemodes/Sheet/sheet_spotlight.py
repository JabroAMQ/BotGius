"""
This is the functionality required for loading into memory the data from Sgtvp's sheet containing the rolls for the group spotlight modes using the Google's API.
Sheet: https://docs.google.com/spreadsheets/d/1x1a-9tLyfJLjatqv5EU5ne6LuoIfPLsN8__AUw3bYy4
"""
import gspread

_MAIN_SHEET_KEY = '1x1a-9tLyfJLjatqv5EU5ne6LuoIfPLsN8__AUw3bYy4'

def _get_default(worksheet: gspread.worksheet.Worksheet) -> list[tuple[str, str]]:
    """
    Method to retrieve a default worksheet, which are the ones which contains only 2 columns of information per row, which is the first column.\n
    The first column contain the name of the artist/group, and the second column contains its community quiz ID.\n
    Return a list of tuples with the information stored in the sheet.
    """
    all_artists = []
    check_set = {'\xa0', '', None}

    # NOTE skipping row 0 as it is the header row
    for row in worksheet.get_all_values()[1:]:
        # Check if it is an empty row
        # NOTE the way the sheet is designed, a field occupies 2 columns instead of one (check 0 and 2 rather than 0 and 1)
        if row[0] in check_set or row[2] in check_set:
            # In case it is not an empty row, but it is missing some information, we print it
            if row[0] not in check_set or row[2] not in check_set:
                print(f'SPOTLIGHT: Skipping row ({row[0]}, {row[2]}) due to containing some empty value')
            continue

        all_artists.append((row[0], row[2]))

    return all_artists

def get_spotlight_groups(client: gspread.Client) -> tuple[
        list[tuple[str, str]],
        list[tuple[str, str]],
        list[tuple[str, str]],
        list[tuple[str, str]],
        list[tuple[str, str]],
        list[tuple[str, str]],
        list[tuple[str, str]]
    ]:
    """
    Method to retrieve the information from the spotlight spreadsheet.

    Return:
    -----------
    A tuple with the next 7 elements (ordered as follow):
    - Male Artist: `list[tuple[str, str]]`
        A list of tuples with all the Male Artist information (see _get_default() docstring for further explanation).
    - Male VA: `list[tuple[str, str]]`
        A list of tuples with all the Male VA information (see _get_default() docstring for further explanation).
    - Female Artist: `list[tuple[str, str]]`
        A list of tuples with all the Female Artist information (see _get_default() docstring for further explanation).
    - Female VA: `list[tuple[str, str]]`
        A list of tuples with all the Female VA information (see _get_default() docstring for further explanation).
    - Groups: `list[tuple[str, str]]`
        A list of tuples with all the Groups information (see _get_default() docstring for further explanation).
    - Composers: `list[tuple[str, str]]`
        A list of tuples with all the Composers information (see _get_default() docstring for further explanation).
    - Franchises: `list[tuple[str, str]]`
        A list of tuples with all the Franchises information (see _get_default() docstring for further explanation).
    """
    spreadsheet = client.open_by_key(_MAIN_SHEET_KEY)
    all_sheets = spreadsheet.worksheets()
    # NOTE skipping worksheet 0 as it not contain useful information for the bot
    male_artists_ws, male_vas_ws, female_artists_ws, female_vas_ws, groups_ws, composers_ws, franchises_ws = all_sheets[1:8]

    male_artists = _get_default(male_artists_ws)
    male_vas = _get_default(male_vas_ws)
    female_artists = _get_default(female_artists_ws)
    female_vas = _get_default(female_vas_ws)
    groups = _get_default(groups_ws)
    composers = _get_default(composers_ws)
    franchises = _get_default(franchises_ws)

    return male_artists, male_vas, female_artists, female_vas, groups, composers, franchises