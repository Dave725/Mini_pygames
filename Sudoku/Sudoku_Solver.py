
def find_empty (bo):
    for i in range(9):
        for j in range(9):
            if bo[i][j] == 0:
                return i, j
    return None

def valid (bo, num, pos):
    # check rows
    for j in range(9):
        if bo[pos[0]][j] == num and j != pos[1]:
            return False

    # check column
    for i in range(9):
        if bo[i] [pos[1]] == num and i != pos[0]:
            return False

    # check box
    xbox = pos[0] // 3
    ybox = pos[1] // 3
    for i in range(xbox * 3, xbox * 3 + 3):
        for j in range(ybox * 3, ybox * 3 + 3):
            if bo[i][j] == num:
                return False

    return True

def solve (bd):
    find = find_empty(bd)
    # set base case
    if not find:
        return True
    else:
        i, j = find_empty(bd)
    # iterate and insert number
    for n in range(1, 10):
        if valid(bd, n, (i, j)):
            bd[i][j] = n
            if solve(bd):
                return bd
            bd[i][j] = 0
    return False
