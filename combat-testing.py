# ==================================================================
# ==================================================================
# ==================================================================
# ALL OF THIS IS DEPRECATED CODE 
# ==================================================================
# ==================================================================
# ==================================================================



import random

# game logic, without the dungeon generation

# game config ============

# needs to be even numbers!
screenWidth = 100
screenHeight = 20

itemTypes = ["Health Potion", "Sword", "Spear", "Spellbook", "The Doomscroll"]
itemReach = ["0", "1", "3", "4", "5"]
itemDamage = ["0", "3", "2", "1", "5"]
canEquipItem = [False, True, True, True, True]

# s is skeleton, g is ghost
enemyCharacters = ["s", "g"]
enemyDamage = [4, 6]
enemyMaxHealth = [2, 12]

# ============

inventory = []

playerX = 0
playerY = 0

# always start the game with 10 health
playerHealth = 10
score = 0

# enemy data
enemyX = []
enemyY = []
enemyType = []
enemyHealth = []

# hazards
flameX = []
flameY = []
flameTimer = []

# every other player turn is a "bonus turn", where no other creatures can do anything
isBonusTurn = False

# ALSO HANDLES FIRE, may want to rename function
def refreshEnemyData():
    for i in range(0, len(enemyX)):
        if (enemyHealth[i] <= 0):
            enemyX.pop(i)
            enemyY.pop(i)
            enemyType.pop(i)
            enemyHealth.pop(i)

    for i in range(0, len(flameTimer)):
        if (flameTimer[i] <= 0):
            flameTimer.pop(i)
            flameX.pop(i)
            flameY.pop(i)
            break
        flameTimer[i] -= 1

# move every enemy on the screen
def moveAllEnemies():
    refreshEnemyData()

    for i in range(0, len(enemyX)):
        moveEnemy(i)

# in this game the convention is:
# -1 = no direction
# 0 = left
# 1 = right
# 2 = down
# 3 = up

# this function is used by enemies to go towards the player
def getDirectionToPlayer(currentX, currentY, avoidWalls):
    rawDirection = -1

    randomVal = random.randint(1, 10)

    if (randomVal > 5):
        if (currentX > playerX):
            rawDirection = 0
        elif (currentX < playerX):
            rawDirection = 1
        elif (currentY > playerY):
            rawDirection = 2
        elif (currentY < playerY):
            rawDirection = 3
    else:
        if (currentY > playerY):
            rawDirection = 2
        elif (currentY < playerY):
            rawDirection = 3
        elif (currentX > playerX):
            rawDirection = 0
        elif (currentX < playerX):
            rawDirection = 1

    return rawDirection

def damagePlayer(value):
    global playerHealth

    playerHealth -= value

def isAdjacent(x1, y1, x2, y2):
    if ((abs(x1-x2) == 1 and abs(y1-y2) == 0) or (abs(x1-x2) == 0 and abs(y1-y2) == 1)):
        return True
    else:
        return False

# move an enemy, use different rules based on how that enemy type moves
def moveEnemy(index):
    global enemyX
    global enemyY

    xChange = 0
    yChange = 0

    dir = getDirectionToPlayer(enemyX[index], enemyY[index], False)

    if (dir == 0):
        xChange = -1
    elif (dir == 1):
        xChange = 1
    elif (dir == 2):
        yChange = -1
    elif (dir == 3):
        yChange = 1

    if (isAdjacent(playerX, playerY, enemyX[index], enemyY[index])):
        damagePlayer(enemyDamage[enemyType[index]])
        return
    
    # skeleton
    if (enemyType[index] == 0):
        if (tryMove(enemyX[index], enemyY[index], xChange, yChange)):
            enemyX[index] += xChange
            enemyY[index] += yChange
    # ghost
    if (enemyType[index] == 1):
        if (tryMove(enemyX[index], enemyY[index], xChange, yChange)):
            enemyX[index] += xChange
            enemyY[index] += yChange
        else:
            # if there's a wall in the way, ghosts just move one more space
            enemyX[index] += xChange * 2
            enemyY[index] += yChange * 2

def tryMove(x, y, xChange, yChange):
    return True

# move the player to a new position, while not allowing them to go through walls
def movePlayer(newX, newY):
    global playerX
    playerX = newX

    global playerY
    playerY = newY

# checking if a box defined with center (x1, y1) and extends w1 on the x and h1 on the y axis,
# intersects with a box defined with center (x2, y2) and extends w2 on the x and h2 on the y axis
def boxIntersection(x1, y1, w1, h1, x2, y2, w2, h2):
    if (x1 - w1 >= x2 - w2 and x1 - w1 <= x2 + w2 and y1 - h1 >= y2 - h2 and y1 - h1 <= y2 + h2):
        return True
    elif (x1 + w1 >= x2 - w2 and x1 + w1 <= x2 + w2 and y1 - h1 >= y2 - h2 and y1 - h1 <= y2 + h2):
        return True
    elif (x1 - w1 >= x2 - w2 and x1 - w1 <= x2 + w2 and y1 + h1 >= y2 - h2 and y1 + h1 <= y2 + h2):
        return True
    elif (x1 + w1 >= x2 - w2 and x1 + w1 <= x2 + w2 and y1 + h1 >= y2 - h2 and y1 + h1 <= y2 + h2):
        return 
    elif (x2 - w2 >= x1 - w1 and x2 - w2 <= x1 + w1 and y2 - h2 >= y1 - h1 and y2 - h2 <= y1 + h1):
        return True
    elif (x2 + w2 >= x1 - w1 and x2 + w2 <= x1 + w1 and y2 - h2 >= y1 - h1 and y2 - h2 <= y1 + h1):
        return True
    elif (x2 - w2 >= x1 - w1 and x2 - w2 <= x1 + w1 and y2 + h2 >= y1 - h1 and y2 + h2 <= y1 + h1):
        return True
    elif (x2 + w2 >= x1 - w1 and x2 + w2 <= x1 + w1 and y2 + h2 >= y1 - h1 and y2 + h2 <= y1 + h1):
        return True
    else: 
        return False

# used for searching through door and chest arrays to find if a given coordinate has one
# used to be multiple functions (isDoor, isChest) but it's the same logic anyways
def isElementInList(x, y, xList, yList):
    for i in range(0, len(xList)):
        if (x == xList[i] and y == yList[i]):
            return True
        
    return False

def getElementInList(x, y, xList, yList):
    for i in range(0, len(xList)):
        if (x == xList[i] and y == yList[i]):
            return i
        
    return -1

def getEnemyCharacter(x, y):
    for i in range(0, len(enemyX)):
        if (enemyX[i] == x and enemyY[i] == y):
            return enemyCharacters[enemyType[i]]
        
    return "no enemy"

# called when you start a new game, resets all the player's stats to default values
def resetPlayerValues():
    global playerHealth
    global score
    global inventory
    
    # always start the game with 10 health
    playerHealth = 10
    score = 0
    inventory = []

# gets the character, as a string, at a given index in an input string
# (that doesn't sound confusing at all)
# basically using a string like a list and grabbing one item
def getCharacter(string, index):
    counter = 0

    for i in string:
        if (counter == index):
            return i
        counter += 1

# taking a number like 1, 
# and formatting it to look like 001 (num of zeros is a parameter) for style points
def formatNumber(string, charCount):
    string = str(string)

    for i in range(0, charCount - len(string)):
        string = "0" + string

    return string

# function that writes out the UI that you see on the top of the screen
def getUICharacter(index):
    inventoryString = "  Inventory: "
    for i in inventory:
        inventoryString += i + ", "

    if (index < len("Health: ___")):
        return getCharacter("Health: " + formatNumber(playerHealth, 3), index)
    elif (index < len("Health: ___") + len(" Score: ___")):
        return getCharacter(" Score: " + formatNumber(score, 3), index - len("Health: ___"))
    elif(index < len(inventoryString) + len(" Score: ___") + len("Health: ___")):
        return getCharacter(inventoryString, index - len(" Score: ___") - len("Health: ___"))
    else:
        return " "

def startNewGame():
    resetPlayerValues()

    # give the player their starting inventory
    inventory.append(itemTypes[0])
    inventory.append(itemTypes[1])
    inventory.append(itemTypes[2])
    inventory.append(itemTypes[3])
    inventory.append(itemTypes[4])

    # spawn a ghost
    enemyType.append(1)
    enemyX.append(screenWidth/2 + 5)
    enemyY.append(screenHeight/2)
    enemyHealth.append(enemyMaxHealth[1])
    
    movePlayer(screenWidth/2, screenHeight/2)

def drawScreen():
    # spacing, for neatness
    print("")
    print("")

    # drawing the world
    currentLine = ""
    for i in range(screenHeight):
        for j in range(screenWidth):
            if (playerX == j and playerY == i):
                currentLine += "&"
            elif (i == 0):
                # drawing UI
                currentLine += str(getUICharacter(j))
            elif (getEnemyCharacter(j, i) != "no enemy"):
                currentLine += getEnemyCharacter(j, i)
            elif (isElementInList(j, i, flameX, flameY)):
                currentLine += "!"
            else:
                currentLine += "."
        print(currentLine)
        currentLine = ""

def addItemToInventory(index):
    inventory.append(itemTypes[index])

def attack(dir):
    heldWeapon = getEquippedWeapon()

    if (heldWeapon == "None"):
        return

    hitX = playerX
    hitY = playerY

    attackRange = 0
    attackDamage = 0

    attackRange = itemReach[findItemIndex(heldWeapon)]
    attackDamage = itemDamage[findItemIndex(heldWeapon)]

    attackRange = int(attackRange)
    attackDamage = int(attackDamage)

    for i in range(0, attackRange):
        if (dir == 0):
            hitX -= 1
        elif (dir == 1):
            hitX += 1
        elif (dir == 2):
            hitY -= 1
        elif (dir == 3):
            hitY += 1

        if (getElementInList(hitX, hitY, enemyX, enemyY) != -1):
            enemyHealth[getElementInList(hitX, hitY, enemyX, enemyY)] -= attackDamage
        if (heldWeapon == "The Doomscroll"):
            spawnFlame(hitX, hitY)

def spawnFlame(x, y):
    flameX.append(x)
    flameY.append(y)
    flameTimer.append(3)

def findItemIndex(itemName):
    for i in range(0, len(itemTypes)):
        if (itemTypes[i] == itemName):
            return i
    
    return -1


def getEquippedWeapon():
    for i in range(0, len(inventory)):
        if (canEquipItem[findItemIndex(inventory[i])]):
            return inventory[i]
        
    return "None"

# move item to index 0 of inventory
# useful, bc when selecting a weapon the game goes through the indices and picks on in order
def equipItem(oldIndex):
    inventory.insert(0, inventory[oldIndex])
    inventory.pop(oldIndex + 1)

def useItem(itemName, index):
    if (itemName == "Health Potion"):
        inventory.pop(index)
        damagePlayer(-3)
    else:
        equipItem(index)

def promptUserForAction():
    action = input("")
    # y axis is reversed, keep in mind

    # player movement ----
    # you can wait just by hitting enter btw!
    if (action == "u"):
        movePlayer(playerX, playerY - 1)
    elif (action == "d"):
        movePlayer(playerX, playerY + 1)
        
    elif (action == "l"):
        movePlayer(playerX - 1, playerY)
    elif (action == "r"):
        movePlayer(playerX + 1, playerY)
    # --------

    # equip/use an item
    elif (getCharacter(action, 0) == "e"):
        for i in range(0, len(inventory)):
            if (int(getCharacter(action, 1)) == i):
                useItem(inventory[i], i)
                return

    # attacking (left, right, down, up)
    elif (action == "al"):
        attack(0)
    elif (action == "ar"):
        attack(1)
    elif (action == "au"):
        attack(2)
    elif (action == "ad"):
        attack(3)

    # restarting the game
    elif (action == "x"):
        startNewGame()

    # fire damages player
    if (isElementInList(playerX, playerY, flameX, flameY)):
        damagePlayer(1)

    for i in range(0, len(enemyType)):
        if (isElementInList(enemyX[i], enemyY[i], flameX, flameY)):
            enemyHealth[i] -= 1

def drawDeathScreen():
    # spacing, for neatness
    print("")
    print("")

    # drawing the world
    currentLine = ""
    for i in range(screenHeight):
        for j in range(screenWidth):
            if (i == screenHeight/2):
                startingIndex = screenWidth / 2 - len("GAME OVER!")/2
                if (j >= startingIndex and j < startingIndex + len("GAME OVER!")):
                    currentLine += getCharacter("GAME OVER!", j - startingIndex)
                else:
                    currentLine += "."
            elif (i == screenHeight/2-1):
                startingIndex = screenWidth / 2 - len("======================")/2
                if (j >= startingIndex and j < startingIndex + len("======================")):
                    currentLine += getCharacter("======================", j - startingIndex)
                else:
                    currentLine += "."
            elif (i == screenHeight/2+1):
                startingIndex = screenWidth / 2 - len("======================")/2
                if (j >= startingIndex and j < startingIndex + len("======================")):
                    currentLine += getCharacter("======================", j - startingIndex)
                else:
                    currentLine += "."
            else:
                currentLine += "."
                
        print(currentLine)
        currentLine = ""

# called when the player dies
def gameOver():
    drawDeathScreen()

# the function that is called every "turn"
def runGameLogic():
    global isBonusTurn

    if (playerHealth <=0):
        gameOver()
        return

    promptUserForAction()

    # only allow creatures to move if it's not the player's bonus turn
    if (not isBonusTurn):
        moveAllEnemies()
        isBonusTurn = True
    else:
        refreshEnemyData()
        isBonusTurn = False

    drawScreen()

    runGameLogic()

startNewGame()
drawScreen()
runGameLogic()
