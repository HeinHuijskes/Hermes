import random
from collections import deque


def generateNonCollapsedBoard():
    """
    Generate a sudoku board where no cell is collapsed.
    This means every cell still has an equal 1/9 chance to be every possible number.
    """
    return [[i for i in range(1, 10)]]*81


def getCell(cells):
    """
    Retrieve a random cell that is not collapsed.
    """
    x, y = -1, -1
    cell = [0]
    while len(cell) == 1:
        # For a more difficult board generation, instead of picking random points every time, find out what values of
        # x and y would generate the most information. This would then lead to fewer values being known overall.
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        cell = cells[x + 9*y].copy()
    return cell, (x, y)


def waveCollapse(cells):
    """
    Collapse one cell and changes it's surrounding cells accordingly.
    This function should only be called when there are still non-collapsed cells left!
    """
    cell, (x, y) = getCell(cells)
    # collapse the found cell
    cell = [cell[random.randint(0, len(cell)-1)]]
    cells[x + 9 * y] = cell

    queue = deque()
    queue.append((x, y))
    visited = [False]*81
    visited[x + 9 * y] = True
    propagateBfs(cells, queue, visited)

    return x, y


def propagateBfs(cells, queue, visited):
    """
    Propagate new collapses using (for some reason recursive) BFS.
    The graph is represented by the cells, the queue consists of changed cells that are not propagated yet.
    """
    if not queue:
        return

    v = queue.popleft()
    (v_x, v_y) = v
    value = cells[v_x + 9*v_y][0]

    adjacent = adjacencyList(v)
    for x, y in adjacent:
        cell = cells[x + 9 * y].copy()

        if len(cell) > 1 and not visited[x + 9*y]:
            visited[x + 9 * y] = True
            if value in cell:
                cell.remove(value)

            cells[x + 9 * y] = cell
            # For now, only take into account cells that are now naturally fully collapsed. This creates easy puzzles,
            # so in the future a smarter evaluation function could be used here to check other collapse conditions.
            if len(cell) == 1:
                queue.append((x, y))

    propagateBfs(cells, queue, visited)


def adjacencyList(v):
    """
    Generate a list of indices for cells that are affected by change in node v.
    """
    (x, y) = v
    adjacent = [(i, y) for i in range(0, 9) if i != x]
    adjacent.extend([(x, j) for j in range(0, 9) if j != y])
    q_x, q_y = x - x % 3, y - y % 3
    adjacent.extend([(q_x+i, q_y+j) for i in range(0, 3) if i != x for j in range(0, 3) if j != y])
    return adjacent


def isCollapsed(cells):
    """
    Checks if all cells have been collapsed.
    """
    for cell in cells:
        if len(cell) > 1:
            return False
    return True


def drawCollapseBoard(cells):
    """
    Draw the not collapsed board states alongside the collapsed ones.
    """
    pass


def drawBoard(cells):
    solid = '|---|---|---|---|---|---|---|---|---|'
    # '|- -|- -|- -|- -|- -|- -|- -|- -|- -|'
    separator = '| - | - | - | - | - | - | - | - | - |'
    print(solid)
    resultString = '|'
    for i, cell in enumerate(cells):
        if not cell:
            resultString += '   '
        else:
            resultString += ' ' + str(cell[0]) + ' '
        if i % 3 == 2:
            resultString += '|'
        else:
            resultString += ' '

        if i % 9 == 8:
            print(resultString)
            resultString = '|'
            if i % 27 == 26:
                print(solid)
            else:
                print(separator)
    print()


class Board:
    def __init__(self):
        self.cells = None

    def setup(self):
        cells = generateNonCollapsedBoard()
        newBoard = [None]*81
        collapsed = False
        while not collapsed:
            (x, y) = waveCollapse(cells)
            collapsed = isCollapsed(cells)
            newBoard[x + 9 * y] = cells[x + 9 * y]
            # drawBoard(newBoard)
        self.cells = newBoard


board = Board()
board.setup()
drawBoard(board.cells)
