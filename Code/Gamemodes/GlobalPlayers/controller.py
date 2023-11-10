from Code.Gamemodes.GlobalPlayers.global_players import GlobalPlayer

class GlobalPlayer_Controller:
    """Controller to encapsule the Global Player Logic from the rest of the application."""

    def __init__(self, global_players : list[tuple[str, str, str, str, str]]) -> None:
        """
        Constructor of the Global Players class.\n
        Requires as argument the list with the Global Players information (the one retrieved from the global player's sheet).
        """
        self.global_players = {global_player[0]: GlobalPlayer(*global_player) for global_player in global_players}

    def get_global_players(self) -> list[GlobalPlayer]:
        """Return a list with all the global players."""
        return list(self.global_players.values())
    
    def info_global_players(self) -> list[str]:
        """
        Return a list with all the global players stored in the global players catalog.\n
        The list is sorted by the global player's names and contains strings with compressed information from the global players.
        """
        global_players : list[str] = [str(global_player) for global_player in self.global_players.values()]
        return sorted(global_players, key=str.lower)