

def bruteforce_guess_number(target: int , roster: list) -> list | None:
    """
        Поиск числа перебором.
        Args:
            target: Число для поиска
            roster: Список чисел
        Returns:
            [число, позиция] или None
        """
    if (type(target)!=int)or(type(roster)!=list):return None
    if (not target) or (not roster): return None
    for i in range(len(roster)):
        if target == roster[i]:
            return [target,i+1]
    return None


def binary_guess_number(target: int, roster: list) -> list | None:
    """
        Поиск числа бинарным методом.
        Args:
            target: Число для поиска
            roster: Список чисел
        Returns:
            [число, попытки] или None
        """
    if (type(target)!=int) or (type(roster)!=list) :return None
    if (not target) or (not roster) : return None
    roster.sort()
    i,k = 0,0
    while (i != target) or (len(roster) != 1):
        if target < roster[len(roster)//2]:
            roster = roster[:(len(roster)//2)]
            i = roster[0]
        else:
            roster = roster[(len(roster)//2):]
            i = roster[len(roster)-1]
        k+=1
    return [i,k]
