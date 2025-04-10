import random

# ------------------------------------------------------
# ======================================================
# INFO
# ======================================================
# ------------------------------------------------------

# MAIN TOOD LIST:

# re-do UI to show only: health, floor #, equipped item, # of health pots
# add the view command to see enemy hp
# proper loot system
# add inventory command to see inventory
# add important events on the bottom of the screen

# ------------------------------------------------------
# ======================================================
# VARIABLES
# ======================================================
# ------------------------------------------------------

# game config ============

# PLAYER ------
startingInventory = ["Health Potion", "Sword", "The Doomscroll"]
defaultHealth = 10
# --------

# skip the lore text
skipIntro = True

# needs to be even numbers!
screenWidth = 100
screenHeight = 20

# generation settings
dungeonRoomCount = 5
finalFloorIndex = 1

# item data

# item descriptions:
# health potion - what it says
# sword - basic weapon, short range, decent damage
# spear - longer range, less damage
# spellbook - double range, very little damage
# doomscroll - OP spellbook (5dmg per tile), spawns fire

# WIP:
# dagger - same range as sword, less damage, you get two uses per turn (1 use takes no turns)
# bow - allows you to shoot any tile within a radius, requires you to have arrows
# crossbow - less range, more damage
# arrow - ammo for ranged weapons

itemTypes = ["Health Potion", "Sword", "Spear", "Spellbook", "The Doomscroll"]
itemReach = ["0", "1", "3", "4", "5"]
itemDamage = ["0", "3", "2", "1", "5"]
canEquipItem = [False, True, True, True, True]

featureTypes = ["Door", "Chest", "Exit", "Flame"]

# enemy data
# s is skeleton, g is ghost
enemyCharacters = ["s", "g"]
enemyDamage = [4, 6]
enemyMaxHealth = [2, 12]

# ============

inventory = []

playerX = 0
playerY = 0

# always start the game with 10 health
playerHealth = 0
score = 0
floorNumber = 0

# dungeon layout -----------

gameMode = 0

# room data
roomCenterX = []
roomCenterY = []
roomWidth = []
roomHeight = []

# feature data

# i could have 2 sets of lists, one for permanent features and one for temporary ones
# but that's 7 lists, vs. the four I have here
# so what I'm doing is permanent features have a timer value of -1 and temporary ones have an actual value

# THE EXIT IS A FEATURE TOO BTW
featureX = []
featureY = []
featureType = []
featureTimer = []
# ----------

# enemies -----------
enemyX = []
enemyY = []
enemyType = []
enemyHealth = []
# --------------

# every other player turn is a "bonus turn", where no other creatures can do anything
isBonusTurn = False

# ------------------------------------------------------
# ======================================================
# FUNCTIONS
# ======================================================
# ------------------------------------------------------

# function that writes out the UI that you see on the top of the screen
def getUICharacter(index):
    inventoryString = "  Inventory:   "
    for i in inventory:
        inventoryString += i + ", "

    if (index < len("Health: ___")):
        return getCharacter("Health: " + formatNumber(playerHealth, 3), index)
    elif (index < len("Health: ___") + len(" Score: ___")):
        return getCharacter(" Score: " + formatNumber(floorNumber, 3), index - len("Health: ___"))
    elif(index < len(inventoryString) + len(" Score: ___") + len("Health: ___")):
        return getCharacter(inventoryString, index - len(" Score: ___") - len("Health: ___"))
    else:
        return " "

# ====================================
# COMBAT / MOVEMENT
# ====================================

# ALSO HANDLES FIRE, may want to rename function
def refreshEnemyData():
    # killing any enemies with 0 or negative health
    for i in range(0, len(enemyX)):
        if (enemyHealth[i] <= 0):
            enemyX.pop(i)
            enemyY.pop(i)
            enemyType.pop(i)
            enemyHealth.pop(i)

    # looping through all features and destroying temporary ones that have run out of time
    for i in range(0, len(featureType) + 1):
        j = len(featureType) - 1 - i
        
        # doesn't matter what type of feature it is, 
        # as long as it has a positive or zero value for its timer
        # keep in mind -1 is for permanent features
        if (featureTimer[j] == 0):
            # THIS COULD POSSIBLY CAUSE OTHER FEATURES TO GET MESSED UP BECAUSE THE INDICES SHIFT,
            # BE CAREFUL
            featureTimer.pop(j)
            featureX.pop(j)
            featureY.pop(j)
            featureType.pop(j)
        else:
            featureTimer[j] -= 1

# move every enemy on the screen
def moveAllEnemies():
    refreshEnemyData()

    for i in range(0, len(enemyX)):
        moveEnemy(i)

# in this game the convention is:
# -1 = no direction
# 0 = left
# 1 = right
# 2 = down (actually up since y-axis is reversed)
# 3 = up (actually down since y-axis is reversed)

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

    if (rawDirection == 0 and (isWall(currentX - 1, currentY) and avoidWalls)):
        if (currentY > playerY):
            rawDirection = 2
        else:
            rawDirection = 3
    if (rawDirection == 1 and (isWall(currentX + 1, currentY) and avoidWalls)):
        if (currentY > playerY):
            rawDirection = 2
        else:
            rawDirection = 3
    if (rawDirection == 2 and (isWall(currentX, currentY - 1) and avoidWalls)):
        if (currentX > playerX):
            rawDirection = 0
        else:
            rawDirection = 1
    if (rawDirection == 3 and (isWall(currentX, currentY + 1) and avoidWalls)):
        if (currentX > playerX):
            rawDirection = 0
        else:
            rawDirection = 1

    return rawDirection

def damagePlayer(value):
    global playerHealth

    playerHealth -= value

def tryMove(x, y, xChange, yChange):
    if (isWall(x + xChange, y + yChange) or getFeatureType(x + xChange, y + yChange) == "Door" or getFeatureType(x + xChange, y + yChange) == "Chest" or getFeatureType(x + xChange, y + yChange) == "Exit"):
        return False
    else:
        return True

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

    if (enemyX[index] == playerX and enemyY[index] == playerY):
        if (not isWall(enemyX[index] - xChange, enemyY[index] - yChange)):
            enemyX[index] -= xChange
            enemyY[index] -= yChange
            damagePlayer(enemyDamage[enemyType[index]])
        else:
            enemyX[index] -= xChange * 2
            enemyY[index] -= yChange * 2
            damagePlayer(enemyDamage[enemyType[index]])

# move the player to a new position, while not allowing them to go through walls
def movePlayer(newX, newY):
    # skip if there's a wall in the way
    # 999 IQ collision detection
    if (isWall(newX, newY)):
        return
    
    global playerX
    playerX = newX

    global playerY
    playerY = newY

def getEnemyCharacter(x, y):
    for i in range(0, len(enemyX)):
        if (enemyX[i] == x and enemyY[i] == y):
            return enemyCharacters[enemyType[i]]
        
    return "no enemy"

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

# ====================================
# WORLD
# ====================================

# intersecting two lines that are axis-aligned
# the HORIZONTAL LINE IS FIRST, VERTICAL SECOND
# def lineInterSection(x1, y1, l1, x2, y2, l2)

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

# checking if a room that extends w on the x and h on the y axis can be placed at location (x, y)
def isValidRoomLocation(w, h, x, y):
    if (x - w <= 0 or x + w >= screenWidth or y - h <= 0 or y + h >= screenHeight):
        return False

    # loop through all the rooms and see if the new room intersects or not
    for i in range(0, len(roomCenterX)):
        if (boxIntersection(x, y, w, h, roomCenterX[i], roomCenterY[i], roomWidth[i], roomHeight[i])):
            return False
        
    return True

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

# checking all rooms and their dimensions to figure out if there's a wall at a given point (x, y)
def isWall(x, y):
    if (isElementInList(x, y, featureX, featureY)):
        return False
    
    for i in range(0, len(roomCenterX)):
        if ((x == roomCenterX[i] - roomWidth[i] or x == roomCenterX[i] + roomWidth[i]) and (y <= roomCenterY[i] + roomHeight[i] and y >= roomCenterY[i] - roomHeight[i])):
            return True
        elif ((y == roomCenterY[i] - roomHeight[i] or y == roomCenterY[i] + roomHeight[i]) and (x <= roomCenterX[i] + roomWidth[i] and x >= roomCenterX[i] - roomWidth[i])):
            return True
    return False

    # generate the dungeon for the first time, and save the coordinates of all rooms
def generateDungeon():
    # global refs for lists/variables ---------
    global roomCenterX
    global roomCenterY
    global roomWidth
    global roomHeight

    global featureX
    global featureY
    global featureType
    global featureTimer

    global enemyX
    global enemyY
    global enemyType
    global enemyHealth
    # --------------

    # reset every list involved in the world
    roomCenterX = []
    roomCenterY = []

    roomWidth = []
    roomHeight = []

    featureTimer = []
    featureX = []
    featureY = []
    featureType = []

    enemyX = []
    enemyY = []
    enemyType = []
    enemyHealth = []

    currentX = screenWidth/2
    currentY = screenHeight/2

    prevWidth = 0
    prevHeight = 0

    for i in range(0, dungeonRoomCount):
        # how far the room extends in every direction
        # rooms can be anywhere from 5x5 to 11x11 (yes, 2 and 5 give this range)
        width = random.randint(2,5)
        height = random.randint(2,5)
        
        roomDir = random.randint(0, 3)

        if (roomDir == 0 and isValidRoomLocation(width, height, currentX - width - prevWidth - 1, currentY)):
            currentX -= width + prevWidth
        elif (roomDir == 1 and isValidRoomLocation(width, height, currentX + width + prevWidth + 1, currentY)):
            currentX += width + prevWidth
        elif (roomDir == 2 and isValidRoomLocation(width, height, currentX, currentY - height - prevHeight - 1)):
            currentY -= height + prevHeight
        elif (roomDir == 3 and isValidRoomLocation(width, height, currentX, currentY + height + prevHeight + 1)):
            currentY += height + prevHeight
        else: 
            continue

        if (i != 0):
            if (roomDir == 0):
                spawnDoor(currentX + width, currentY)
            elif (roomDir == 1):
                spawnDoor(currentX - width, currentY)
            elif (roomDir == 2):
                spawnDoor(currentX, currentY + height)
            elif (roomDir == 3):
                spawnDoor(currentX, currentY - height)

        roomWidth.append(width)
        roomHeight.append(height)

        roomCenterX.append(currentX)
        roomCenterY.append(currentY)

        # spawning chests
        # if (random.randint(0, 10) > 7 and i < dungeonRoomCount - 1 and i > 0):
            # spawnChest(currentX, currentY)

        prevWidth = width
        prevHeight = height

    # since the exit is a feature, we just append its location to all the feature lists
    featureX.append(roomCenterX[len(roomCenterX)-1])
    featureY.append(roomCenterY[len(roomCenterY)-1])

    featureType.append("Exit")
    featureTimer.append(-1)

    enemyType.append(1)
    enemyX.append(roomCenterX[len(roomCenterX)-1] + 1)
    enemyY.append(roomCenterY[len(roomCenterY)-1])
    enemyHealth.append(enemyMaxHealth[1])

# the final floor is hardcoded
def generateFinalDungeon():
    # global refs for lists/variables ---------
    global roomCenterX
    global roomCenterY
    global roomWidth
    global roomHeight

    global featureX
    global featureY
    global featureType
    global featureTimer

    global enemyX
    global enemyY
    global enemyType
    global enemyHealth
    # --------------

    # reset every list involved in the world
    roomCenterX = []
    roomCenterY = []

    roomWidth = []
    roomHeight = []

    featureTimer = []
    featureX = []
    featureY = []
    featureType = []

    enemyX = []
    enemyY = []
    enemyType = []
    enemyHealth = []

    roomCenterX.append(screenWidth/2)
    roomCenterY.append(screenHeight/2)
    roomWidth.append(12)
    roomHeight.append(4)

    # player goes in the center of the room, for now
    movePlayer(screenWidth/2, screenHeight/2)

    # no need to do anything with the exit, resetting the feature lists deletes it

# i can probably condense these 3 functions
def spawnFlame(x, y):
    featureType.append("Flame")
    featureX.append(x)
    featureY.append(y)
    # 3 turns until the flame dissapears
    featureTimer.append(3)
def spawnChest(x, y):
    featureType.append("Chest")
    featureX.append(x)
    featureY.append(y)
    featureTimer.append(-1)
def spawnDoor(x, y):
    featureType.append("Door")
    featureX.append(x)
    featureY.append(y)
    featureTimer.append(-1)

def getFeatureType(x, y):
    if (getElementInList(x, y, featureX, featureY) != -1):
        return featureType[getElementInList(x, y, featureX, featureY)]
    else:
        return "None"

# ====================================
# INVENTORY
# ====================================

def addItemToInventory(index):
    inventory.append(itemTypes[index])

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

# given an item, perform a default action
# usually this just equips the item (as is the case for weapons)
def useItem(itemName, index):
    if (itemName == "Health Potion"):
        inventory.pop(index)
        # negative value, bc negative damage is health
        damagePlayer(-3)
    else:
        equipItem(index)

# ====================================
# UTILITY
# ====================================

# are two points next to each other? 
# diagonal doesn't count!
def isAdjacent(x1, y1, x2, y2):
    if ((abs(x1-x2) == 1 and abs(y1-y2) == 0) or (abs(x1-x2) == 0 and abs(y1-y2) == 1)):
        return True
    else:
        return False

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

# ====================================
# SCREEN
# ====================================

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
            elif (isWall(j, i)):
                currentLine += "#"
            elif (getFeatureType(j, i) == "Door"):
                currentLine += "◘"
            elif (getFeatureType(j, i) == "Exit"):
                currentLine += "↓"
            elif (getFeatureType(j, i) == "Chest"):
                currentLine += "◙"
            elif (getFeatureType(j, i) == "Flame"):
                currentLine += "!"
            elif (i == 0):
                # drawing UI
                currentLine += str(getUICharacter(j))
            elif (getEnemyCharacter(j, i) != "no enemy"):
                currentLine += getEnemyCharacter(j, i)
            else:
                currentLine += "."
        print(currentLine)
        currentLine = ""

def blankScreen():
    # spacing, for neatness
    print("")
    print("")

    defaultCharacter = "."

    currentLine = ""
    for i in range(screenHeight):
        for j in range(screenWidth):
            currentLine += defaultCharacter
                
        print(currentLine)
        currentLine = ""

def fullscreenMessage(msg, showContinueMessage):
    msg = str(msg)

    # spacing, for neatness
    print("")
    print("")

    defaultCharacter = "."

    currentLine = ""
    for i in range(screenHeight):
        for j in range(screenWidth):
            if (i == screenHeight/2):
                startingIndex = screenWidth / 2 - round(len(msg)/2)
                if (j >= startingIndex and j < startingIndex + round(len(msg))):
                    currentLine += getCharacter(msg, j - startingIndex)
                else:
                    currentLine += defaultCharacter
            elif (i == screenHeight/2-2):
                startingIndex = screenWidth / 2 - round(len("======================")/2)
                if (j >= startingIndex and j < startingIndex + round(len("======================"))):
                    currentLine += getCharacter("======================", j - startingIndex)
                else:
                    currentLine += defaultCharacter
            elif (i == screenHeight/2+2):
                startingIndex = screenWidth / 2 - round(len("======================")/2)
                if (j >= startingIndex and j < startingIndex + round(len("======================"))):
                    currentLine += getCharacter("======================", j - startingIndex)
                else:
                    currentLine += defaultCharacter
            elif (i == screenHeight/2+6 and showContinueMessage):
                startingIndex = screenWidth / 2 - round(len("(press ENTER to continue)")/2)
                if (j >= startingIndex and j < startingIndex + round(len("(press ENTER to continue)"))):
                    currentLine += getCharacter("(press ENTER to continue)", j - startingIndex)
                else:
                    currentLine += defaultCharacter
            else:
                currentLine += defaultCharacter
                
        print(currentLine)
        currentLine = ""


# ====================================
# GAME LOGIC
# ====================================

# go through the intro text, should only happen upon booting the game for the first time
def runIntro():
    fullscreenMessage("FakeVoxel presents", True)
    input("")
    fullscreenMessage("PYROGUE", True)
    input("")

    # exposition
    fullscreenMessage("   First, the war.   ", True)
    input("")
    fullscreenMessage("   Then, the siege.   ", True)
    input("")

    fullscreenMessage("   We held up for almost a month.   ", True)
    input("")
    fullscreenMessage("   But we couldn't wait forever.   ", True)
    input("")
    fullscreenMessage("   They wanted the king, those were their terms.   ", True)
    input("")
    fullscreenMessage("   Well they got what they wanted.   ", True)
    input("")

    fullscreenMessage("   Rumor has it they killed him, and buried him here.   ", True)
    input("")
    fullscreenMessage("   Still wearing the crown.   ", True)
    input("")
    fullscreenMessage("   ...   ", True)
    input("")
    fullscreenMessage("   My crown.   ", True)
    input("")

    blankScreen()
    input("")

def selectGameMode():
    global gameMode

    fullscreenMessage("   Type the desired game mode and hit enter: 'normal', 'endless'   ", False)
    gameModeInput = input("")

    if (gameModeInput == "normal"):
        gameMode = 0
    elif (gameModeInput == "endless"):
        gameMode = 1
    else:
        gameMode = 0

    # showing the user what gamemode they picked
    if (gameMode == 0):
        fullscreenMessage("   Normal mode selected.   ", True)
    else:
        fullscreenMessage("   Endless mode selected.   ", True)
    
    input("")

    fullscreenMessage("   Good luck, traveller.   ", True)
    input("")

    blankScreen()
    input("")

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
        useItem(inventory[int(getCharacter(action, 1))], int(getCharacter(action, 1)))
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
    if (getFeatureType(playerX, playerY) == "Flame"):
        damagePlayer(1)

    for i in range(0, len(enemyType)):
        if (getFeatureType(enemyX[i], enemyY[i]) == "Flame"):
            enemyHealth[i] -= 1

# called when you start a new game, resets all the player's stats to default values
def resetPlayerValues():
    global playerHealth
    global floorNumber
    global score
    global inventory
    
    # always start the game with 10 health
    playerHealth = defaultHealth
    floorNumber = 0
    score = 0
    inventory = []

    # give the player their starting inventory
    for i in startingInventory:
        inventory.append(i)

# complete restart
def startNewGame():
    resetPlayerValues()
    generateDungeon()

    movePlayer(roomCenterX[0], roomCenterY[0])

# called when the player steps over an exit
def nextFloor():
    global floorNumber
    floorNumber = floorNumber + 1

    # if playing on normal mode, the final floor needs to spawn
    if (floorNumber == finalFloorIndex and gameMode == 0):
        generateFinalDungeon()
    else:
        # for normal floors, just generate a random dungeon
        generateDungeon()
        movePlayer(roomCenterX[0], roomCenterY[0])

# called when the player dies
def gameOver():
    fullscreenMessage("GAME OVER", True)

# main logic function, calls itself
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

    if (getFeatureType(playerX, playerY) == "Exit"):
        nextFloor()

    drawScreen()

    runGameLogic()

# the only bit of code that isn't in a function lol
if (not skipIntro):
    runIntro()

selectGameMode()

startNewGame()
drawScreen()

# calling this starts the main game loop
runGameLogic()
