from Code.Gamemodes.SpecialLists.og_specialList import OG_SpecialList
from Code.Gamemodes.SpecialLists.cq_specialList import CQ_SpecialList

class SpecialList_Controller:
    """Controller to encapsule the SpecialList Logic from the rest of the application."""

    def __init__(
        self,
        og_special_lists: list[tuple[str, str, str, str, str, str]],
        cq_special_lists: list[tuple[str, str, str, str, str]]
    ) -> None:
        """
        Constructor of the SpecialList class.\n
        Requires as argument the lists with the Special Lists information (the ones retrieved from the sheet).
        """
        self.og_special_lists = {
            og_special_list[0]: OG_SpecialList(*og_special_list)
            for og_special_list in og_special_lists
        }
        self.cq_special_lists = {
            cq_special_list[0]: CQ_SpecialList(*cq_special_list)
            for cq_special_list in cq_special_lists
        }

    def get_special_lists(self) -> str:
        """Return a list with all the special lists."""
        return list(self.og_special_lists.values())
    
    def info_special_lists(self) -> list[str]:
        """
        Return a list with all the special lists stored in the special lists catalog.\n
        The list is sorted by the special list's names and contains strings with compressed information from the special lists.
        """
        special_lists: list[str] = [
            str(special_list)+'\n'
            for special_list in self.og_special_lists.values()
        ]
        return sorted(special_lists, key=str.lower)