def BruteForce_guess_numder(target: int , roster: list) -> list:
    if((type(target)!=int)or(type(roster)!=list)):return 'Incorrect input data type'
    if((not target)or(not roster)): return 'Incorrect input data type'
    for i in range(len(roster)):
        if target == roster[i]:
            return [target,i]


def Binary_guess_numder(target: int, roster: list) -> list:
    if((type(target)!=int)or(type(roster)!=list)):return 'Incorrect input data type'
    if((not target)or(not roster)):
        return "Incorrect input data type"
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
