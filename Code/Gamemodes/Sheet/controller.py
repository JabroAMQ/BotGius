import os
import json

import dotenv
import gspread
from google.oauth2.service_account import Credentials

from Code.Gamemodes.Sheet.sheet_botgius import get_botgius_data
from Code.Gamemodes.Sheet.sheet_globalplayers import get_global_players_data

dotenv.load_dotenv()

class Sheet_Controller:
    """Controller to encapsule the Sheet data extraction Logic from the rest of the application."""
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._set_data()
        return cls._instance

    def _set_data(self) -> None:
        self.client = self._get_client()

    def _get_client(self) -> gspread.Client:
        """
        Method to retrieve the gspread client using the credentials stored in the environment variables.
        """
        credentials_info = json.loads(os.getenv('GOOGLE_SHEETS_CREDS'))
        scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
        gspread_client = gspread.authorize(credentials)
        return gspread_client


    def get_global_players(self) -> tuple[
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
        return get_global_players_data(self.client)
    

    def get_sheet_data(self) -> tuple[
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
        return get_botgius_data(self.client)