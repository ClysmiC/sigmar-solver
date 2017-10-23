from PIL import Image


# Coordinates for hex grids are tricky. My favorite way to represent them is below:
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

blank = 0
air = 1
fire = 2
salt = 3
water = 4
vitae = 5
earth = 6
mors = 7
quicksilver = 8
lead = 9
tin = 10
iron = 11
copper = 12
silver = 13
gold = 14

elements = ["blank", "air", "fire", "salt", "water", "vitae", "earth", "mors", "quicksilver", "lead", "tin", "iron", "copper", "silver", "gold"]
initialCounts = [36, 8, 8, 4, 8, 4, 8, 4, 5, 1, 1, 1, 1, 1, 1]

def elementName(element):
    if element is None:
        return "None"
    
    return elements[element]

def exitWithError(error):
    print(error)
    exit()

def solve():

    colors = []

    # board = [[None] * 10] * 10
    board = [ \
              [vitae, blank, blank, mors, blank, blank, None, None, None, None, None], \
              [blank, mors, blank, tin, fire, fire, air, None, None, None, None], \
              [blank, blank, iron, quicksilver, blank, water, quicksilver, blank, None, None, None], \
              [blank, blank, air, earth, blank, fire, salt, blank, blank, None, None], \
              [salt, vitae, water, air, earth, air, quicksilver, water, blank, blank, None], \
              [blank, earth, water, earth, water, gold, water, air, earth, water, silver], \
              [None, blank, quicksilver, blank, blank, water, vitae, blank, fire, blank, blank], \
              [None, None, quicksilver, fire, copper, earth, lead, earth, blank, air, blank], \
              [None, None, None, blank, blank, salt, salt, air, fire, air, fire], \
              [None, None, None, None, blank, mors, blank, blank, mors, fire, blank], \
              [None, None, None, None, None, earth, blank, blank, blank, vitae, blank] \
            ]

    verifyInput(board)

    activeTiles = []

    topLeft = (810, 200)
    middle = (980, 485)
    bottomRight = (1140, 770)

    wSample1 = (middle[0] - topLeft[0]) / 2.5
    wSample2 = (bottomRight[0] - middle[0]) / 2.5
    wSample3 = (bottomRight[0] - topLeft[0]) / 5

    hSample1 = (middle[1] - topLeft[1]) / 5
    hSample2 = (bottomRight[1] - middle[1]) / 5
    hSample3 = (bottomRight[1] - topLeft[1]) / 10

    # (x, y) in screen-space needed to traverse one x or y step in grid-space
    xStep = ((wSample1 + wSample2 + wSample3) / 3 , 0)
    yStep = (-xStep[0] / 2, -(hSample1 + hSample2 + hSample3) / 3)

    print("x step = " + str(xStep))
    print("y step = " + str(yStep))

    for x in range(0, 10):
        for y in range(0, 10):
            if abs(x - y) >= 5:
                continue

    img = Image.open("input.png")
    color = img.getpixel((810, 200))

    print(color)


def verifyInput(board):
    counts = [0] * (gold + 1)
    
    for x in range(0, 11):
        for y in range(0, 11):

            tile = board[x][y]
            
            tileExists = tile is not None
            tileShouldExist = abs(x - y) <= 5
            
            if tileExists != tileShouldExist:
                exitWithError("Error, tile at " + str((x, y)) + " should " + ("" if tileShouldExist else "not ") + " exist. Found: " + str(elementName(tile)))

            if tileExists:
                counts[tile] += 1


    for i in range(len(elements)):
        if counts[i] != initialCounts[i]:
            exitWithError("Expected " + str(initialCounts[i]) + " " + elementName(i) + " tiles, found " + str(counts[i]))
            

solve()
