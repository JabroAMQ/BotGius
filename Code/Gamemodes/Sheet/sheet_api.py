import os

import gspread

"""
This is the functionality required for loading into memory the data from Jabro's sheet using the Google API.
Sheet: https://docs.google.com/spreadsheets/d/1VxqdLA3T_coSpoFXhSnaNgAk3BZ2XQ7drvNgcUf6OXQ/
"""

_MAIN_SHEET_KEY = '1VxqdLA3T_coSpoFXhSnaNgAk3BZ2XQ7drvNgcUf6OXQ'


def _get_gamemodes_description(descriptions_worksheet : gspread.worksheet.Worksheet) -> dict[str, str]:
    """Return a dictionary with the names of the gamemodes (lowercase) as Keys and their description as Values."""
    return {row[0].lower(): row[1] for row in descriptions_worksheet.get_all_values()}

def _get_artists(artists_worksheet : gspread.worksheet.Worksheet) -> list[tuple[str, str, str, str, str, str]]:
    """
    Return a list of tuples with all the artist information:
        - First Element: The Artist(s) name(s).
        - Second Element: The Username (Anilist / MyAnimeList) that has the list.
        - Third Element: The Score to be used in the AMQ settings (if any).
        - Fourth Element: The List's section(s) that contain the artist(s) shows (Watching, Completed, etc.).
        - Fifth Element: Where the List is from (Anilist / MyAnimeList).
        - Sixth Element: The Player who created the list.
    """
    return [(row[0], row[1], row[2], row[3], row[4], row[5]) for row in artists_worksheet.get_all_values()]

def _get_specialLists(specialLists_worksheet : gspread.worksheet.Worksheet) -> list[tuple[str, str, str, str, str, str, str]]:
    """
    Return a list of tuples with all the special list information:
        - First Element: The SpecialList name.
        - Second Element: The Username (Anilist / MyAnimeList) that has the list.
        - Third Element: Where the List is from (Anilist / MyAnimeList).
        - Fourth Element: The List's section(s) that contain the artist(s) shows (Watching, Completed, etc.).
        - Fifth Element: The Difficulty range that should be used (0-100%, 0-60%, etc.).
        - Sixth Element: The SpecialList description.
        - Seventh Element: The Player who created the list.
    """
    return [(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in specialLists_worksheet.get_all_values()]

def _get_default(worksheet : gspread.worksheet.Worksheet, new_line : bool = True) -> list[str]:
   """
   Method to retrieve a default worksheet, which are the ones which contains only 1 column of information per row, which is the first column.\n
   new_line parameter is used to add (or not) a new line between rows.\n
   Return a list of strings with the sheet information.
   """
   return [row[0]+'\n' for row in worksheet.get_all_values()] if new_line else [row[0] for row in worksheet.get_all_values()]

def get_sheet_data() -> tuple[dict[str, str], list[str], list[str], list[tuple[str, str, str, str, str, str]], list[str], list[tuple[str, str, str, str, str, str, str]]]:
    """
    Method to retrieve the information from the gamemodes spreadsheet.

    Return:
    -----------
    A tuple with the next 6 elements (ordered as follow):
    - Description: A dictionary with the names of the gamemodes (lowercase) as Keys and their description as Values.
    - Metronomes: A list of strings with all the possible metronome powers.
    - Items: A list of strings with all the possible items.
    - Artists: A list of tuples with all the artists information (see _get_artists docstring for further explanation).
    - Tags: A list of strings with all the possible tags.
    - SpecialLists: A list of tuples with all the special lists information (see _get_specialList docstring for further explanation).
    """
    filename = os.path.join('Code', 'Gamemodes', 'Sheet', 'credentials-sheets-api.json')    # Private, it isn't added to the GitHub repository
    gspread_client = gspread.service_account(filename=filename)
    spreadsheet = gspread_client.open_by_key(_MAIN_SHEET_KEY)

    descriptions_ws, metronomes_ws, items_ws, artists_ws, tags_ws, specialLists_ws = (spreadsheet.get_worksheet(i) for i in range(6))
    descriptions = _get_gamemodes_description(descriptions_ws)
    metronomes = _get_default(metronomes_ws)
    items = _get_default(items_ws)
    artists = _get_artists(artists_ws)
    tags = _get_default(tags_ws, new_line=False)
    specialLists = _get_specialLists(specialLists_ws)

    return descriptions, metronomes, items, artists, tags, specialLists