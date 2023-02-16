import random
import time
from collections import deque


improved = False


def generateNonCollapsedBoard():
    """
    Generate a sudoku board where no cell is collapsed.
    This means every cell still has an equal 1/9 chance to be every possible number.
    """
    return [[i for i in range(1, 10)]]*81


def getCell(cells):
    if improved:
        return getCellImproved(cells)
    else:
        return getCellNormal(cells)


def getCellNormal(cells):
    """
    Retrieve a random cell that is not collapsed.
    """
    x, y = -1, -1
    cell = [0]
    while len(cell) == 1:
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        cell = cells[x + 9*y].copy()
    return cell, (x, y)


def getCellImproved(cells):
    """
    Retrieve a random cell that is not collapsed out of the most un-collapsed cells
    """
    # highest is an array of tuples, where each tuple contains (x, y, value)
    highest = [(-1, -1, 0)]
    for x in range(0, 9):
        for y in range(0, 9):
            value = evaluate(x, y, cells)
            if value > highest[0][2]:
                highest = [(x, y, value)]
            elif value == highest[0][2]:
                highest.append((x, y, value))

    # Make sure to still pick a random cell out of all equal highest value cells
    index = random.randint(0, len(highest)-1)
    x, y, value = highest[index]
    cell = cells[x + 9 * y].copy()
    return cell, (x, y)


def evaluate(x, y, cells):
    """
    Evaluate the informational value of the cell at position (x,y).
    """
    # The more possible states for this cell, the higher its informational value is.
    return len(cells[x + 9 * y])


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
normal = []
better = []
iterations = 250
timer_start = time.perf_counter()
for i in range(0, iterations):
    board.setup()
    normal.append(sum([1 for i in board.cells if i]))
    # drawBoard(board.cells)
timer_end = time.perf_counter()
n_timer = timer_end - timer_start

improved = True
timer_start = time.perf_counter()
for i in range(0, iterations):
    board.setup()
    better.append(sum([1 for i in board.cells if i]))
    # drawBoard(board.cells)
timer_end = time.perf_counter()
b_timer = timer_end - timer_start

print('Performance:')
print('Normal: ' + str(sum(normal)/iterations) + ' (' + str(iterations) + ' runs, ' + str(n_timer) + ' s)')
print('Better: ' + str(sum(better)/iterations) + ' (' + str(iterations) + ' runs, ' + str(b_timer) + ' s)')
