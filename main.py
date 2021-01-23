import numpy as np

bomb = "\U0001F4A3"
flag = "\U0001F6A9"

print("MineSweeper game!")
print("─"*77)
print("To play:")
print((" "*8)+"Type the letter and number of the cell you want to show")
print("To flag:")
print((" "*8)+"Type 'flag' and then the letter and number of the cell you want to "+flag)
print("To win:")
print((" "*7)+"Try not to hit any "+bomb)
print("─"*77)
print()

state = "lobby"

print("Select settings: ")
print((" "*17)+"a) 5x5")
print((" "*17)+"b) 10x10")
print((" "*17)+"c) 20x20")

lobbySelection = ""

def lobbyCheck():
  global lobbySelection
  lobbySelection = input("Input the corresponding letter for your table(a,b,c): ")
  if (lobbySelection in "abc") or (lobbySelection in "ABC"):
    if lobbySelection == "a" or lobbySelection == "b" or lobbySelection == "c" or lobbySelection == "A" or lobbySelection == "B" or lobbySelection == "C":
      print("Your selection: Setting "+lobbySelection)
      return lobbySelection
    else:
      print("Please enter a valid selection")
      lobbyCheck()
  else:
    print("Please enter a valid selection")
    lobbyCheck()

lobbyCheck()
lobbySelection = lobbySelection.upper()

state = "setup"

tableSize = 0

if lobbySelection == "A":
  tableSize = 5
elif lobbySelection == "B":
  tableSize = 10
elif lobbySelection == "C":
  tableSize = 20

nums = np.random.binomial(n=1, p=0.15, size=[tableSize**2])
nums = np.reshape(nums,(int(tableSize),int(tableSize)))

grid = np.empty((int(tableSize),int(tableSize)),dtype=str)

bombCount = 0
for i in range(len(grid)):
  for j in range(len(grid[i])):
    count = 0
    if nums[i][j] == 1:
      count = "*"
      bombCount += 1
    else:
      for k in list([-1,0,1]):
        for l in list([-1,0,1]):
          if i+k < tableSize and j+l < tableSize and i+k >= 0 and j+l >= 0:
            if nums[i+k][j+l] == 1:
              count += 1
    grid[i][j] = str(count)

flagN = bombCount

emptyGrid = np.full((int(tableSize),int(tableSize)), ['█'])

def printGrd(grid):
  s = len(str(tableSize))
  print(" "*(s+1)+"│ "+"  ".join([chr(65+i) for i in range(tableSize)]))
  print("─"*(s+1)+"┼─"+"─"*((tableSize*3)-2))
  for i in range(len(grid)):
    if i > 8 : 
      s = len(str(tableSize))-1
    print(str(i+1)+" "*(s)+"│ "+"  ".join(grid[i]))

print("─"*77)
print("Flags: "+str(flagN))
print()
print("Bomb count: "+str(bombCount))
print()
printGrd(emptyGrid)

def clearEmpty(i,j):
  global grid
  global emptyGrid
  emptyGrid[i][j] = " "
  for k in list([-1,0,1]):
    for l in list([-1,0,1]):
      if i+k < tableSize and j+l < tableSize and i+k >= 0 and j+l >= 0:
        if grid[i+k][j+l] == "0":
          if emptyGrid[i+k][j+l] != " ":
            clearEmpty(i+k,j+l)
        else:
          emptyGrid[i+k][j+l] = grid[i+k][j+l]

def cellSelection():
  global flagN
  selection = input("Cell name: ")
  isFlag = False;
  if selection.startswith("flag"):
    isFlag = True
    selection = selection[5:]
  if selection[0].upper().isalpha():
    col = ord(selection[0].upper()) - 65
    if selection[1:].isnumeric():
      row = int(selection[1:])-1
      if col>=0 and col<tableSize and row>=0 and row<tableSize:
        if isFlag:
          flagN -= 1
        return ((col,row),isFlag)
      else:
        return cellSelection()
    else:
      return cellSelection()
  else:
    return cellSelection()

while state != "ended":
  print("─"*77)
  lost = False
  (col,row),isFlag = cellSelection()

  if isFlag:
    emptyGrid[row][col] = flag
  else:
    if grid[row][col] == '0':
      if emptyGrid[row][col] == flag:
          flagN += 1
      clearEmpty(row,col)
    else:
      if grid[row][col] == "*":
        state = "ended"
        lost = True
        emptyGrid[row][col] = bomb
      else:
        if emptyGrid[row][col] == flag:
          flagN += 1
        emptyGrid[row][col] = grid[row][col]
  print()
  print("Remaining Flags: "+str(flagN))
  print()
  printGrd(emptyGrid)

  solved = True
  for i in range(tableSize):
    for j in range(tableSize):
      if grid[i][j] == "*":
        if emptyGrid[i][j] != flag:
          solved = False
      else:
        if grid[i][j] != "*" and emptyGrid[i][j] == flag:
          solved = False
  if solved:
    state = "ended"
    print()
    print("You found all the bombs!")
  if lost:
    print()
    print("You lost!")

print("Game ended")