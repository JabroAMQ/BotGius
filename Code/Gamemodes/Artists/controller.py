from Code.Gamemodes.Artists.og_artist import OG_Artist
from Code.Gamemodes.Artists.cq_artist import CQ_Artist

class Artist_Controller:
    """Controller to encapsule the Artist Logic from the rest of the application."""

    def __init__(
        self,
        og_artists: list[tuple[str, str, str, str, str, str]],
        cq_artists: list[tuple[str, str, str, str]]
    ) -> None:
        """
        Constructor of the Artist class.\n
        Requires as argument the lists with the Artists information (the ones retrieved from the sheet).
        """
        self.og_artists = {
            og_artist[0]: OG_Artist(*og_artist)
            for og_artist in og_artists
        }
        self.cq_artists = {
            cq_artist[0]: CQ_Artist(*cq_artist)
            for cq_artist in cq_artists
        }


    def get_artists(self) -> list[OG_Artist]:
        """Return a list with all the artists."""
        return list(self.og_artists.values())
    
    def info_artists(self) -> list[str]:
        """
        Return a list with all the artists stored in the artists catalog.\n
        The list is sorted by the artist's names and contains strings with compressed information from the artists.
        """
        artists: list[str] = [
            str(artist)+'\n'
            for artist in self.og_artists.values()
        ]
        return sorted(artists, key=str.lower)