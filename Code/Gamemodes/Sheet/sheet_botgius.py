"""
This is the functionality required for loading into memory the data from Jabro's sheet using the Google's API.
Sheet: https://docs.google.com/spreadsheets/d/1VxqdLA3T_coSpoFXhSnaNgAk3BZ2XQ7drvNgcUf6OXQ/
"""
import gspread

_MAIN_SHEET_KEY = '1VxqdLA3T_coSpoFXhSnaNgAk3BZ2XQ7drvNgcUf6OXQ'

def _get_gamemodes_description(descriptions_worksheet: gspread.worksheet.Worksheet) -> dict[str, str]:
    """Return a dictionary with the names of the gamemodes (lowercase) as Keys and their description as Values."""
    return {
        row[0].lower(): row[1]
        for row in descriptions_worksheet.get_all_values()[1:]
    }

def _get_og_artists(og_artists_worksheet: gspread.worksheet.Worksheet) -> list[tuple[str, str, str, str, str, str]]:
    """
    Return a list of tuples with all the artist information:
    - First Element: `str`
        The Artist(s) name(s).
    - Second Element: `str`
        The Username (Anilist / MyAnimeList) that has the list.
    - Third Element: `str`
        The Score to be used in the AMQ settings (if any).
    - Fourth Element: `str`
        The List's section(s) that contain the artist(s) shows (Watching, Completed, etc.).
    - Fifth Element: `str`
        Where the List is from (Anilist / MyAnimeList).
    - Sixth Element: `str`
        The Player who created the list.
    """
    return [
        (row[0], row[1], row[2], row[3], row[4], row[5])
        for row in og_artists_worksheet.get_all_values()[1:]
    ]

def _get_cq_artists(cq_artists_worksheet: gspread.worksheet.Worksheet) -> list[tuple[str, str, str, str, str]]:
    """
    Return a list of tuples with all the artist information:
    - First Element: `str`
        The Community quiz ID.
    - Second Element: `str`
        The Artist(s) name(s).
    - Third Element: `str`
        The Community Quiz name.
    - Fourth Element: `str`
        The number of songs that the quiz has.
    - Fifth Element: `str`
        The Player who created the list.
    """
    return [
        (row[0], row[1], row[2], row[3], row[4])
        for row in cq_artists_worksheet.get_all_values()[1:]
    ]

def _get_og_specialLists(og_specialLists_worksheet: gspread.worksheet.Worksheet) -> list[tuple[str, str, str, str, str, str, str]]:
    """
    Return a list of tuples with all the special list information:
        - First Element: `str`
            The SpecialList name.
        - Second Element: `str`
            The Username (Anilist / MyAnimeList) that has the list.
        - Third Element: `str`
            Where the List is from (Anilist / MyAnimeList).
        - Fourth Element: `str`
            The List's section(s) that contain the artist(s) shows (Watching, Completed, etc.).
        - Fifth Element: `str`
            The Difficulty range that should be used (0-100%, 0-60%, etc.).
        - Sixth Element: `str`
            The SpecialList description.
        - Seventh Element: `str`
            The Player who created the list.
    """
    return [
        (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        for row in og_specialLists_worksheet.get_all_values()[1:]
    ]

def _get_cq_specialLists(cq_specialLists_worksheet: gspread.worksheet.Worksheet) -> list[tuple[str, str, str, str, str]]:
    """
    Return a list of tuples with all the special list information:
    - First Element: `str`
        The Community Quiz name ID.
    - First Element: `str`
        The Special List name.
    - Second Element: `str`
        The Community Quiz name.
    - Third Element: `str`
        The number of songs that the quiz has.
    - Fourth Element: `str`
        The Player who created the list.
    """
    return [
        (row[0], row[1], row[2], row[3], row[4])
        for row in cq_specialLists_worksheet.get_all_values()[1:]
    ]

def _get_default(worksheet: gspread.worksheet.Worksheet, add_new_line: bool = True) -> list[str]:
    """
    Method to retrieve a default worksheet, which are the ones which contains only 1 column of information per row, which is the first column.\n
    `add_new_line` parameter is used to add (or not) a new line between rows.\n
    Return a list of strings with the sheet information.
    """
    new_line = '\n' if add_new_line else ''
    return [
        f'{row[0]}{new_line}'
        for row in worksheet.get_all_values()[1:]
    ]

def get_botgius_data(client: gspread.Client) -> tuple[
        dict[str, str],
        list[str],
        list[str],
        list[str],
        list[tuple[str, str, str, str, str, str]],
        list[tuple[str, str, str, str, str]],
        list[tuple[str, str, str, str, str, str, str]],
        list[tuple[str, str, str, str, str]]
    ]:
    """
    Method to retrieve the information from the gamemodes spreadsheet.

    Return:
    -----------
    A tuple with the next 6 elements (ordered as follow):
    - Description: `dict[str, str]`
        A dictionary with the names of the gamemodes (lowercase) as Keys and their description as Values.
    - Metronomes: `list[str]`
        A list of strings with all the possible metronome powers.
    - Items: `list[str]`
        A list of strings with all the possible items.
    - Tags: `list[str]`
        A list of strings with all the possible tags.
    - OG_Artists: `list[tuple[str, str, str, str, str, str]]`
        A list of tuples with all the artists information (see _get_og_artists docstring for further explanation).\n
        These are Anilist/MyAnimeList lists that have all the shows where the artist(s) sings in (songs from those shows by different artist can play).
    - CQ_Artists: `list[tuple[str, str, str, str]]`
        A list of tuples with all the artists information (see _get_cq_artists docstring for further explanation).\n
        These are Community Quizes to get only the songs from the artist rather than all songs from the shows were the artist sings in.
    - OG_SpecialLists: `list[tuple[str, str, str, str, str, str, str]]`
        A list of tuples with all the special lists information (see _get_og_specialList docstring for further explanation).
        These are Anilist/MyAnimeList lists that have all the shows included in the special lists (all songs from those shows can play).
    - CQ_SpecialLists: `list[tuple[str, str, str, str, str, str, str]]`
        A list of tuples with all the special lists information (see _get_cq_specialList docstring for further explanation).
        These are Community Quizes to get only the songs from the composer/shows/whatever rather than all songs from the shows like in OG_SpecialLists.
    """
    spreadsheet = client.open_by_key(_MAIN_SHEET_KEY)

    descriptions_ws, metronomes_ws, items_ws, tags_ws, og_artists_ws, cq_artists_ws, og_specialLists_ws, cq_specialLists_ws = (spreadsheet.get_worksheet(i) for i in range(8))
    descriptions = _get_gamemodes_description(descriptions_ws)
    metronomes = _get_default(metronomes_ws)
    items = _get_default(items_ws)
    tags = _get_default(tags_ws, add_new_line=False)
    og_artists = _get_og_artists(og_artists_ws)
    cq_artists = _get_cq_artists(cq_artists_ws)
    og_specialLists = _get_og_specialLists(og_specialLists_ws)
    cq_specialLists = _get_cq_specialLists(cq_specialLists_ws)

    return descriptions, metronomes, items, tags, og_artists, cq_artists, og_specialLists, cq_specialLists