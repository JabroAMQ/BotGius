from Code.Gamemodes.Artists.artist import Artist

class Artist_Controller:
    """Controller to encapsule the Artist Logic from the rest of the application."""

    def __init__(self, artists: list[tuple[str, str, str, str, str, str]]) -> None:
        """
        Constructor of the Artist class.\n
        Requires as argument the list with the Artists information (the one retrieved from the sheet).
        """
        self.artists = {
            artist[0]: Artist(*artist)
            for artist in artists
        }

    def get_artists(self) -> list[Artist]:
        """Return a list with all the artists."""
        return list(self.artists.values())
    
    def info_artists(self) -> list[str]:
        """
        Return a list with all the artists stored in the artists catalog.\n
        The list is sorted by the artist's names and contains strings with compressed information from the artists.
        """
        artists: list[str] = [
            str(artist)+'\n'
            for artist in self.artists.values()
        ]
        return sorted(artists, key=str.lower)