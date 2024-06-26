'''# boardTileArray[x][y] format -> stored as xy -> increments downwards
def generate(boardWidth, boardHeight):
    global boardTileArray
    boardTileArray = [[int(str(x)+str(y)) for x in range(boardWidth)] for y in range(boardHeight)]
    print(boardTileArray)

generate(8,10)

print(boardTileArray[2][6]) # Outputs 62

#----------------------------------------------------------------------------------------------------

# boardTileArray[y][x] format -> stored as yx  -> increments across
def generate(boardWidth, boardHeight):
    global boardTileArray
    boardTileArray = [[int(str(y)+str(x)) for x in range(boardWidth)] for y in range(boardHeight)]
    print(boardTileArray)

generate(8,10)

print(boardTileArray[2][6]) # Outputs 26'''

text = "R4*"
print(text[:1]) # returns player color
print(text[1:2]) # returns strength
if text[-1:] == "*": # checks if revealed
    print("revealed")