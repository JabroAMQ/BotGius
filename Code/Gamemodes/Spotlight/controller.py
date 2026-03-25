from Code.Gamemodes.Spotlight.classes import Male_Artist, Male_VA, Female_Artist, Female_VA, Group, Composer, Franchise

class Spotlight_Controller:
    """Controller to encapsule the Spotlight Logic from the rest of the application."""

    def __init__(self, spotlight_dict: dict[str, list[tuple[str, str]]]) -> None:
        """
        Constructor of the Spotlight Controller class.\n
        Requires as argument the dictionary with the Spotlight information (the one retrieved from the spotlight's sheet).
        """
        self.spotlight_dict = spotlight_dict

        self.males_artists = {
            male_artist[0]: Male_Artist(*male_artist)
            for male_artist in self.spotlight_dict['male_artists']
        }

        self.males_vas = {
            male_va[0]: Male_VA(*male_va)
            for male_va in self.spotlight_dict['male_vas']
        }

        self.females_artists = {
            female_artist[0]: Female_Artist(*female_artist)
            for female_artist in self.spotlight_dict['female_artists']
        }

        self.females_vas = {
            female_va[0]: Female_VA(*female_va)
            for female_va in self.spotlight_dict['female_vas']
        }

        self.groups = {
            group[0]: Group(*group)
            for group in self.spotlight_dict['groups']
        }

        self.composers = {
            composer[0]: Composer(*composer)
            for composer in self.spotlight_dict['composers']
        }

        self.franchises = {
            franchise[0]: Franchise(*franchise)
            for franchise in self.spotlight_dict['franchises']
        }


    def get_all_male_artists(self) -> list[Male_Artist]:
        """Return a list with all the Male Artists."""
        return list(self.males_artists.values())

    def get_all_male_VAs(self) -> list[Male_VA]:
        """Return a list with all the Male Voice Actors."""
        return list(self.males_vas.values())

    def get_all_female_artists(self) -> list[Female_Artist]:
        """Return a list with all the Female Artists."""
        return list(self.females_artists.values())

    def get_all_female_VAs(self) -> list[Female_VA]:
        """Return a list with all the Female Voice Actors."""
        return list(self.females_vas.values())

    def get_all_composers(self) -> list[Composer]:
        """Return a list with all the Composers."""
        return list(self.composers.values())
    
    def get_all_groups(self) -> list[Group]:
        """Return a list with all the Groups."""
        return list(self.groups.values())
    
    def get_all_franchises(self) -> list[Franchise]:
        """Return a list with all the Franchises."""
        return list(self.franchises.values())


    def info_male_artists(self) -> list[str]:
        """
        Return a list with all the male artists stored in the spotlight catalog.\n
        The list is sorted by the artist's names and contains strings with compressed information from the artists.
        """
        male_artists: list[str] = [
            str(male_artist)
            for male_artist in self.get_all_male_artists()
        ]
        return sorted(male_artists, key=str.lower)
    
    def info_male_VAs(self) -> list[str]:
        """
        Return a list with all the male voice actors stored in the spotlight catalog.\n
        The list is sorted by the voice actor's names and contains strings with compressed information from the voice actors.
        """
        male_VAs: list[str] = [
            str(male_VA)
            for male_VA in self.get_all_male_VAs()
        ]
        return sorted(male_VAs, key=str.lower)

    def info_female_artists(self) -> list[str]:
        """
        Return a list with all the female artists stored in the spotlight catalog.\n
        The list is sorted by the artist's names and contains strings with compressed information from the artists.
        """
        female_artists: list[str] = [
            str(female_artist)
            for female_artist in self.get_all_female_artists()
        ]
        return sorted(female_artists, key=str.lower)
    
    def info_female_VAs(self) -> list[str]:
        """
        Return a list with all the female voice actors stored in the spotlight catalog.\n
        The list is sorted by the voice actor's names and contains strings with compressed information from the voice actors.
        """
        female_VAs: list[str] = [
            str(female_VA)
            for female_VA in self.get_all_female_VAs()
        ]
        return sorted(female_VAs, key=str.lower)
    
    def info_groups(self) -> list[str]:
        """
        Return a list with all the groups stored in the spotlight catalog.\n
        The list is sorted by the group names and contains strings with compressed information from the groups.
        """
        groups: list[str] = [
            str(group)
            for group in self.get_all_groups()
        ]
        return sorted(groups, key=str.lower)
    
    def info_composers(self) -> list[str]:
        """
        Return a list with all the composers stored in the spotlight catalog.\n
        The list is sorted by the composer names and contains strings with compressed information from the composers.
        """
        composers: list[str] = [
            str(composer)
            for composer in self.get_all_composers()
        ]
        return sorted(composers, key=str.lower)
    
    def info_franchises(self) -> list[str]:
        """
        Return a list with all the franchises stored in the spotlight catalog.\n
        The list is sorted by the franchise names and contains strings with compressed information from the franchises.
        """
        franchises: list[str] = [
            str(franchise)
            for franchise in self.get_all_franchises()
        ]
        return sorted(franchises, key=str.lower)