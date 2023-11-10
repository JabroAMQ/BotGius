from Code.Gamemodes.SpecialLists.specialList import SpecialList

class SpecialList_Controller:
    """Controller to encapsule the SpecialList Logic from the rest of the application."""

    def __init__(self, special_lists : list[tuple[str, str, str, str, str, str, str]]) -> None:
        """
        Constructor of the SpecialList class.\n
        Requires as argument the list with the SpecialLists information (the one retrieved from the sheet).
        """
        self.special_lists = {special_list[0]: SpecialList(*special_list) for special_list in special_lists}

    def get_special_lists(self) -> str:
        """Return a list with all the special lists."""
        return list(self.special_lists.values())
    
    def info_special_lists(self) -> list[str]:
        """
        Return a list with all the special lists stored in the special lists catalog.\n
        The list is sorted by the special list's names and contains strings with compressed information from the special lists.
        """
        special_lists : list[str] = [str(special_list)+'\n' for special_list in self.special_lists.values()]
        return sorted(special_lists, key=str.lower)