def to_chunks(initial_list : list[str], limit : int = 2000) -> list[str]:
    """
    Given a raw list where each list's element is an object, this is, if Artist list then each element of the list is an artist,
    join together the elements of the list to create "discord messages", this is, creates sublists the closest to len `limit` without
    exceeding it.

    Return:
    ----------
    A new list of strings, each of them being a sublist converted to string by joining the subelements with a 'new line' so that the new list can be
    interpreted as the content of the messages to send to Discord with the optimal lenght.
    """
    def get_optimal_msg_size(lst : list[str], limit : int) -> tuple[list[str], list[str]]:
        """Auxiliar function to extract the next "message" (element of the final list) given the not yet processed part of the `initial_list`"""
        for i in range(len(lst)):
            if len(' '.join(lst[:i+1])) > limit:
                return lst[:i], lst[i:]
        return lst, None

    answer = []
    left = initial_list
    while True:
        optimal, left = get_optimal_msg_size(left, limit)
        answer += ['\n'.join(optimal)]
        if not left:
            break
    return answer