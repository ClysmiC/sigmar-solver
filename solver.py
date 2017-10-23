from PIL import Image
from enum import IntEnum


# Coordinates for hex grids are tricky. A convenient way to represent them is below:
#
# Y
#  \
#   \
#    \______ X
#  (0, 0)

# In Sigmar's garden, the corner tiles have the following coordinates:
#
#   (5, 10)  ________ (10, 10)
#           /        \
#          /          \
#  (0, 5) /            \ (10, 5)
#         \            /
#          \          /
#           \________/
#      (0, 0)       (5, 0)

# I number the neighbors of a hex as follows:
#
#          
#     5   / \   0
#        /   \
#    4  |     |  1
#       |     |
#        \   /
#     3   \ /  2

class Tile(IntEnum):
    BLANK = 0
    AIR = 1
    FIRE = 2
    SALT = 3
    WATER = 4
    VITAE = 5
    EARTH = 6
    MORS = 7
    QUICKSILVER = 8
    LEAD = 9
    TIN = 10
    IRON = 11
    COPPER = 12
    SILVER = 13
    GOLD = 14
    
class GameState:
    def __init__(self, board, currentMetal=Tile.LEAD):
        self.board = board
        self.currentMetal = currentMetal

elements = ["BLANK", "AIR", "FIRE", "SALT", "WATER", "VITAE", "EARTH", "MORS", "QUICKSILVER", "LEAD", "TIN", "IRON", "COPPER", "SILVER", "GOLD"]
initialCounts = [36, 8, 8, 4, 8, 4, 8, 4, 5, 1, 1, 1, 1, 1, 1]

def tileAt(xy, board):
    if xy[0] < 0 or xy[0] > 10 or xy[1] < 0 or xy [1] > 10:
        return None
    else:
        return board[xy[1]][xy[0]]
    
def isBlankOrNone(xy, board):
    return not isElement(xy, board)

def isElement(xy, board):
    tile = tileAt(xy, board)
    return tile is not None and tile > Tile.BLANK

def isMetal(xy, board):
    return tileAt(xy, board) >= Tile.LEAD

def isMetalThatIsntCurrent(xy, state):
    board = state.board
    
    if isMetal(xy, board):
        return tileAt(xy, board) != state.currentMetal

    return False

def tileName(tile):
    if tile is None:
        return "None"
    
    return elements[tile]

def exitWithError(error):
    print(error)
    exit()

def solve():

    # colors = []
    # board = [[None] * 11] * 11

    # TODO: replace hard-coded board with mechanism to read board in from the screen
    board = [ \
              [Tile.VITAE, Tile.BLANK, Tile.BLANK, Tile.MORS, Tile.BLANK, Tile.BLANK, None, None, None, None, None], \
              [Tile.BLANK, Tile.MORS, Tile.BLANK, Tile.TIN, Tile.FIRE, Tile.FIRE, Tile.AIR, None, None, None, None], \
              [Tile.BLANK, Tile.BLANK, Tile.IRON, Tile.QUICKSILVER, Tile.BLANK, Tile.WATER, Tile.QUICKSILVER, Tile.BLANK, None, None, None], \
              [Tile.BLANK, Tile.BLANK, Tile.AIR, Tile.EARTH, Tile.BLANK, Tile.FIRE, Tile.SALT, Tile.BLANK, Tile.BLANK, None, None], \
              [Tile.SALT, Tile.VITAE, Tile.WATER, Tile.AIR, Tile.EARTH, Tile.AIR, Tile.QUICKSILVER, Tile.WATER, Tile.BLANK, Tile.BLANK, None], \
              [Tile.BLANK, Tile.EARTH, Tile.WATER, Tile.EARTH, Tile.WATER, Tile.GOLD, Tile.WATER, Tile.AIR, Tile.EARTH, Tile.WATER, Tile.SILVER], \
              [None, Tile.BLANK, Tile.QUICKSILVER, Tile.BLANK, Tile.BLANK, Tile.WATER, Tile.VITAE, Tile.BLANK, Tile.FIRE, Tile.BLANK, Tile.BLANK], \
              [None, None, Tile.QUICKSILVER, Tile.FIRE, Tile.COPPER, Tile.EARTH, Tile.LEAD, Tile.EARTH, Tile.BLANK, Tile.AIR, Tile.BLANK], \
              [None, None, None, Tile.BLANK, Tile.BLANK, Tile.SALT, Tile.SALT, Tile.AIR, Tile.FIRE, Tile.AIR, Tile.FIRE], \
              [None, None, None, None, Tile.BLANK, Tile.MORS, Tile.BLANK, Tile.BLANK, Tile.MORS, Tile.FIRE, Tile.BLANK], \
              [None, None, None, None, None, Tile.EARTH, Tile.BLANK, Tile.BLANK, Tile.BLANK, Tile.VITAE, Tile.BLANK] \
            ]

    verifyInput(board)

    state = GameState(board)

    activeTiles = []

    for y in range(len(board)):
        for x in range(len(board[y])):

            if isElement((x, y), board) and isActive((x, y), state):
                activeTiles.append((x, y))

    print(activeTiles)


def verifyInput(board):

    if len(board) != 11:
        exitWithError("Wrong board height: " + str(len(board)))

    for i in range(len(board)):
        if len(board[i]) != 11:
            exitWithError("Wrong board with in row " + str(i) + ": " + str(len(board[i])))

    counts = [0] * (len(Tile) + 1)
    
    for y in range(0, 11):
        for x in range(0, 11):

            tile = tileAt((x, y), board)
            
            tileExists = tile is not None
            tileShouldExist = abs(x - y) <= 5
            
            if tileExists != tileShouldExist:
                exitWithError("Error, tile at " + str((x, y)) + " should " + ("" if tileShouldExist else "not ") + " exist. Found: " + str(tileName(tile)))

            if tileExists:
                counts[tile] += 1


    for i in range(len(elements)):
        if counts[i] != initialCounts[i]:
            exitWithError("Expected " + str(initialCounts[i]) + " " + tileName(i) + " tiles, found " + str(counts[i]))


def getNeighborCoords(xy, board):
    neighbors = []
    neighbors.append((xy[0] + 1, xy[1] + 1))
    neighbors.append((xy[0] + 1, xy[1] + 0))
    neighbors.append((xy[0] + 0, xy[1] - 1))
    neighbors.append((xy[0] - 1, xy[1] - 1))
    neighbors.append((xy[0] - 1, xy[1] + 0))
    neighbors.append((xy[0] + 0, xy[1] + 1))
    return neighbors
    
def isActive(xy, state):
    board = state.board
    
    if isBlankOrNone(xy, board):
        return False
    
    if isMetalThatIsntCurrent(xy, state):
        return False

    neighbors = getNeighborCoords(xy, board)
        
    pos0Free = False
    pos1Free = False
    consecutiveFree = 0
    
    for i, n in enumerate(neighbors):
        isFree = isBlankOrNone(n, board)

        if isFree:
            consecutiveFree += 1
            
            if i == 0:
                pos0Free = True
            elif i == 1:
                pos1Free = True
                
        else:
            consecutiveFree = 0

        if consecutiveFree == 3:
            return True

    if consecutiveFree == 1 and pos0Free and pos1Free:
        return True

    if consecutiveFree == 2 and pos0Free:
        return True
        
    return False
            

solve()
