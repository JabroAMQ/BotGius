from Code.Gamemodes.GlobalPlayers.global_players import GlobalPlayer

class GlobalPlayer_Controller:
    """Controller to encapsule the Global Player Logic from the rest of the application."""

    def __init__(self, all_global_players: list[tuple[str, str, str, str, str]], active_global_players: list[tuple[str, str, str, str, str]]) -> None:
        """
        Constructor of the Global Players class.\n
        Requires as argument the lists with the Global Players information (the ones retrieved from the global player's sheet).
        """
        self.all_global_players = {
            global_player[0]: GlobalPlayer(*global_player)
            for global_player in all_global_players
        }

        self.active_global_players = {
            global_player[0]: GlobalPlayer(*global_player)
            for global_player in active_global_players
        }


    def get_all_global_players(self) -> list[GlobalPlayer]:
        """Return a list with all the global players."""
        return list(self.all_global_players.values())

    def get_active_global_players(self) -> list[GlobalPlayer]:
        """Return a list with all the active global players."""
        return list(self.active_global_players.values())


    def info_all_global_players(self) -> list[str]:
        """
        Return a list with all the global players stored in the global players catalog.\n
        The list is sorted by the global player's names and contains strings with compressed information from the global players.
        """
        global_players: list[str] = [
            str(global_player)
            for global_player in self.all_global_players.values()
        ]
        return sorted(global_players, key=str.lower)
    
    def info_active_global_players(self) -> list[str]:
        """
        Return a list with all the active global players stored in the global players catalog.\n
        The list is sorted by the global player's names and contains strings with compressed information from the global players.
        """
        global_players: list[str] = [
            str(global_player)
            for global_player in self.active_global_players.values()
        ]
        return sorted(global_players, key=str.lower)