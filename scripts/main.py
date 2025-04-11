
# Name: Maximilian McDiarmid
# Finishing Date (this script): April 11th, 2025
# Description: 

# MAIN TOOD LIST:

# ranged enemies
# bows only work in the current room
# status effects

import random
# the library that I use for ANSI escape codes, which allows me to write colored text in the terminal
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

# ------------------------------------------------------
# ======================================================
# VARIABLES
# ======================================================
# ------------------------------------------------------

# game config ============

versionString = "v0.1"
debugMode = True
skipIntro = True # skip the lore text

# player stuff ------
startingInventory = ["Health Potion", "Sword","Swiftness Potion","Ironskin Potion","Strength Potion"]
defaultHealth = 20
# --------

# general stuff ---------
screenWidth = 100 # needs to be even numbers!
screenHeight = 20 # needs to be even numbers!
# ---------------------------------

# dungeon stuff ---------------------------------
dungeonRoomCount = 10
finalFloorIndex = 10
# ---------------------------------

# item data ---------------------------------
itemTypes = ["Sword", "Spear", "Scimitar", "Glaive", "Bow", "Crossbow", "Hellbow", "Bomb", "Fire Bomb", "Health Potion", "Superior Potion", "Bone", "Mushroom", "Book of Piercing", "Book of Flames", "Chaos Bow", "Wildflower", "Cave Root","Fire Potion","Strength Potion","Swiftness Potion","Strange Berries","Windbloom","Strange Brew","Ironskin Potion"]
itemDamage = [4, 3, 3, 2, 2, 3, 3, 6, 4, -4, -10, 0, -2, 2, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0]
specialType = [0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 2, 3, 4, 6, 4, 6, 5] # weapons: 0 is nothing, 1 is fire, 2 is fire resistance, 3 is strength, 4 is speed, 5 is ironskin, 6 is random effect
itemReach = [1, 3, 1, 4, 8, 6, 5, 4, 6, 0, 0, 0, 0, 10, 10, 10, 0, 0, 9, 4, 14, 3, 4, 10, 3]
itemArea = [0, 0, 1, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # melee: how many tiles the attack extends perpindicular to the attack direction, ranged: same thing but every direction
canEquipItem = [True, True, True, True, True, True, True, True, True, False, False, False, False, True, True, True, False, False, False, False, False, False, False, False, False]
isConsumable = [False, False, False, False, False, False, False, True, True, True, True, False, True, False, False, False, False, False, True, True, True, True, True, True, True]
itemHitChance = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 40, 100, 100, 100, 100, 100, 100, 100, 100, 100] # out of 100
isItemRanged = [False, False, False, False, True, True, True, True, True, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False]

ingredients = ["Mushroom","Bone","Cave Root","Wildflower","Windbloom","Strange Berries"]
weapons = ["Sword", "Spear", "Scimitar", "Glaive", "Bow", "Crossbow", "Hellbow", "Bomb", "Fire Bomb", "Book of Piercing", "Book of Flames", "Chaos Bow","Health Potion","Superior Potion","Fire Potion","Strength Potion","Swiftness Potion","Strange Brew","Ironskin Potion"]

# data for crafting recipes
craftingRecipes = ["Mushroom,Cave Root", "Mushroom,Wildflower",  "Bone,Cave Root",   "Windbloom,Wildflower",   "Strange Berries,Strange Berries",  "Bone,Wildflower"]
craftingResults = ["Health Potion",      "Fire Potion",          "Ironskin Potion",  "Swiftness Potion",       "Strange Brew",                     "Strength Potion"]

# --------------------------------------------

# things that can show up in a dungeon
# fake exits are second exits that lead to special places
# cauldrons allow you to craft potions using ingredients
featureTypes = ["Door", "Chest", "Exit", "Flame", "Note", "Fake Exit", "Cauldron"]

# fire resistance, damage, ironskin, speed
statusEffectTimers = [0, 0, 0, 0]

# enemy data ------------------------

# enemies to add
# S - spearman
# a - archer
# l - longbowman (flaming arrows)
# b - bomb thrower
# w - witch
# e - explosive rat (suicide enemy)
# R - rat king (secret boss)

enemyCharacters = ["d", "H", "s", "u", "r", "f", "g", "N"]
enemyNames = ["Dummy", "Horse", "Swordsman", "Undead", "Rat", "Fire Rat", "Ghost", "Necromancer"]
enemyMoveSpeed = [0, 0, 1, 1, 1, 1, 1, 1]
enemyDamage = [0, 0, 5, 3, 1, 1, 8, 8]
enemyMaxHealth = [999, 15, 10, 8, 5, 5, 6, 80]
enemyAbility = [0, 0, 0, 0, 0, 1, 2, 5] # 1: spawn fire trail, 2: go through walls, 3: summon rats, 4: summon undead, 5: necromancer (summon undead and spawn fire)
enemyRange = [0, 0, 0, 0, 0, 0, 0, 0] # WIP
# ------------------------

# enemy spawning data ------------------------
# basically the dungeon is divided into quarters, each with a different set of enemies
enemyTable1 = ["Rat", "Fire Rat"]
enemyTable2 = ["Rat", "Fire Rat", "Swordsman"]
enemyTable3 = ["Rat", "Fire Rat", "Ghost"]
enemyTable4 = ["Undead", "Ghost", "Swordsman"]
#  ------------------------

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

# variable that determines the boss's attack
bossCounter = 0
# --------------

eventMessages = []

# these show up on the right side of the screen, always
tooltips = ["w -- move up", 
            "s -- move down", 
            "a -- move left", 
            "d -- move right", 
            "",
            "x num1, num2 -- attack num1 units right and num2 units up", 
            "",
            "e num -- equip item # num from inventory", 
            "",
            "r -- start new game", 
            "",
            "c num1, num2 -- craft num1 + num2 (requires a cauldron beside you)"]

# every other player turn is a "bonus turn", where no other creatures can do anything
# RIGHT NOW THIS FEATURE IS TURNED OFF
isBonusTurn = False
areTipsActive = True

# ------------------------------------------------------
# ======================================================
# FUNCTIONS
# ======================================================
# ------------------------------------------------------

# ====================================
# DEBUG
# ====================================

# as the lists get longer, this function allows me to see what indices I missed
def debugItemData():
    print("")

    print("Item names: " + str(len(itemTypes)))
    print("Item damages: " + str(len(itemDamage)))
    print("Item reaches: " + str(len(itemReach)))
    print("Item abilities: " + str(len(specialType)))
    print("Item areas: " + str(len(itemArea)))
    print("Can equip: " + str(len(canEquipItem)))
    print("Is consumable: " + str(len(isConsumable)))
    print("Hit chance: " + str(len(itemHitChance)))
    print("Is ranged: " + str(len(isItemRanged)))

    print("")

    # don't run the game until everything looks good
    input("")

# ====================================
# COMBAT / MOVEMENT
# ====================================

# ALSO HANDLES FIRE, may want to rename function
def refreshEnemyData():
    # killing any enemies with 0 or negative health
    startingLength = len(enemyType)
    for i in range(0, startingLength):
        j = startingLength - i - 1

        if (enemyHealth[j] <= 0):
            enemyX.pop(j)
            enemyY.pop(j)
            enemyType.pop(j)
            enemyHealth.pop(j)

# move every enemy on the screen
def moveAllEnemies():
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

def damagePlayer(value, damageType):
    global playerHealth

    if (value > 0):
        if (damageType == "Fire"):
            if (statusEffectTimers[0] <= 0):
                playerHealth -= value
                # doesn't tell you why you took damage, but that's okay they'll figure it out
                recordEvent("Took " + str(value) + " damage.")
            else:
                # make sure the player knows that the lack of damage isn't a bug
                recordEvent("Blocked " + str(value) + " damage.")
        else:
            if (statusEffectTimers[2] <= 0):
                playerHealth -= value
                recordEvent("Took " + str(value) + " damage.")
            else:
                recordEvent("Blocked " + str(value) + " damage.")
    else:
        # healing items just use negative damage values
        # there's nothing to limit you from taking one
        playerHealth -= value

    if (playerHealth > defaultHealth):
        playerHealth = defaultHealth

def tryMove(x, y, xChange, yChange, ability):
    # ability 2 enemie ignore walls
    if (ability == 2):
        if (getFeatureType(x + xChange, y + yChange) == "Chest" or getFeatureType(x + xChange, y + yChange) == "Exit" or getEnemyCharacter(x + xChange, y + yChange) != "no enemy" or (x + xChange == playerX and y + yChange == playerY)):
            return False
        else:
            return True
    else:
        if (isWall(x + xChange, y + yChange) or getFeatureType(x + xChange, y + yChange) == "Chest" or getFeatureType(x + xChange, y + yChange) == "Exit" or getEnemyCharacter(x + xChange, y + yChange) != "no enemy" or (x + xChange == playerX and y + yChange == playerY)):
            return False
        else:
            return True

# move an enemy, use different rules based on how that enemy type moves
def moveEnemy(index):
    global enemyX
    global enemyY

    global bossCounter

    xChange = 0
    yChange = 0

    # damaging the player
    # this is done first, so enemies can't move and attack at the same time
    if (isAdjacent(enemyX[index], enemyY[index], playerX, playerY)):
        damagePlayer(enemyDamage[enemyType[index]],"Attack")
        return

    dir = getDirectionToPlayer(enemyX[index], enemyY[index], False)

    if (dir == 0):
        xChange = -1
    elif (dir == 1):
        xChange = 1
    elif (dir == 2):
        yChange = -1
    elif (dir == 3):
        yChange = 1

    if (enemyAbility[enemyType[index]] == 5):
        bossCounter += 1

        if (bossCounter == 12 and not isWall(enemyX[index] - xChange, enemyY[index] - yChange) and getEnemyCharacter(enemyX[index] - xChange, enemyY[index] - yChange) == "no enemy"):
            # spawn unded enemy
            spawnEnemy(enemyX[index] - xChange, enemyY[index] - yChange, "Undead")
            bossCounter = 1
            return
        elif(bossCounter == 6):
            for i in range(1, 8):
                spawnFlame(enemyX[index] + xChange * i, enemyY[index] + yChange * i)
            return
        elif(bossCounter % 2 == 0):
            return

    # temporary code to allow dummys and horses (not moving enemies) to work
    # basically skip the rest of the function if the move speed is 0
    if (enemyMoveSpeed[enemyType[index]] == 0):
        return
    
    # the tryMove() function checks whether an obstacle is in the way of the attempted move
    # it takes in the enemy ability, bc ability 2 enemies ignore walls
    if (tryMove(enemyX[index], enemyY[index], xChange, yChange, enemyAbility[enemyType[index]])):
        enemyX[index] += xChange
        enemyY[index] += yChange

    # ability 1 enemies spawn fire trails behind them as they walk
    if (enemyAbility[enemyType[index]] == 1):
        spawnFlame(enemyX[index] - xChange, enemyY[index] - yChange)

# move the player to a new position, while not allowing them to go through walls
def movePlayer(newX, newY):
    # skip if there's a wall in the way
    # 999 IQ collision detection
    if (isWall(newX, newY) or getEnemyCharacter(newX, newY) != "no enemy"):
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

# msg is the command string
def attack(msg):
    dir = -1
    isMelee = False

    heldWeapon = getEquippedWeapon()

    attackRange = 0
    attackDamage = 0

    attackRange = itemReach[findItemIndex(heldWeapon)]
    attackDamage = itemDamage[findItemIndex(heldWeapon)]

    if (statusEffectTimers[1] > 0):
        attackDamage *= 2

    attackRange = int(attackRange)
    attackDamage = int(attackDamage)

    # if holding a ranged weapon, the attack command will look like a2,1
    # if melee, it will look like al, ar, au, ad
    if (isNumber(getCharacter(msg, 0))):
        isMelee = False

        commaIndex = str(msg).find(",")

        hitX = playerX + int(substring(msg, 0, commaIndex))
        hitY = playerY - int(substring(msg, commaIndex + 1, len(msg) - commaIndex - 1))

        if (abs(hitX - playerX) > attackRange or abs(hitY - playerY) > attackRange):
            return
    else:
        isMelee = True

        hitX = playerX
        hitY = playerY

        if (getCharacter(msg, 0) == "a"):
            dir = 0
        elif (getCharacter(msg, 0) == "d"):
            dir = 1
        elif (getCharacter(msg, 0) == "s"):
            dir = 3
        if (getCharacter(msg, 0) == "w"):
            dir = 2

    if (heldWeapon == "None"):
        return
    
    # sometimes a hit can fail, depending on the accuracy of the weapon
    if (random.randint(0, 100) > itemHitChance[findItemIndex(heldWeapon)]):
        return

    if (isMelee):
        # melee logic
        for i in range(0, attackRange):
            if (dir == 0):
                hitX -= 1
            elif (dir == 1):
                hitX += 1
            elif (dir == 2):
                hitY -= 1
            elif (dir == 3):
                hitY += 1

            for j in range(-itemArea[findItemIndex(heldWeapon)], itemArea[findItemIndex(heldWeapon)] + 1):

                xMod = 0
                yMod = 0
                if (dir == 0 or dir == 1):
                    yMod = j
                else:
                    xMod = j
                
                if (getElementInList(hitX + xMod, hitY + yMod, enemyX, enemyY) != -1):
                    enemyHealth[getElementInList(hitX + xMod, hitY + yMod, enemyX, enemyY)] -= attackDamage
                    recordEvent("Hit " + enemyNames[enemyType[getElementInList(hitX + xMod, hitY + yMod, enemyX, enemyY)]] + " for " + str(attackDamage) + " damage.")
                if (specialType[findItemIndex(heldWeapon)] == 1 and not isWall(hitX + j, hitY + i)):
                    spawnFlame(hitX + xMod, hitY + yMod)
    else:
        # ranged logic
        for i in range(-itemArea[findItemIndex(heldWeapon)], itemArea[findItemIndex(heldWeapon)] + 1):
            for j in range(-itemArea[findItemIndex(heldWeapon)], itemArea[findItemIndex(heldWeapon)] + 1):

                if (getElementInList(hitX + j, hitY + i, enemyX, enemyY) != -1):
                    enemyHealth[getElementInList(hitX + j, hitY + i, enemyX, enemyY)] -= attackDamage
                    recordEvent("Hit " + enemyNames[enemyType[getElementInList(hitX + j, hitY + i, enemyX, enemyY)]] + " for " + str(attackDamage) + " damage.")
                if (specialType[findItemIndex(heldWeapon)] == 1 and not isWall(hitX + j, hitY + i)):
                    spawnFlame(hitX + j, hitY + i)

    if (isConsumable[findItemIndex(heldWeapon)]):
        inventory.pop(findItemIndexInInventory(heldWeapon))

# ====================================
# WORLD:
# ====================================

def refreshTemporaryHazards():
    # looping through all features and destroying temporary ones that have run out of time
    startingLength = len(featureType)
    for i in range(0, startingLength):
        j = startingLength - i - 1

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
        elif (featureTimer[j] > 0):
            featureTimer[j] -= 1

# intersecting two lines that are axis-aligned
# the HORIZONTAL LINE IS FIRST, VERTICAL SECOND
def lineInterSection(x1, y1, l1, x2, y2, l2):
    if (y1 < y2 + l2 and y1 > y2 - l2 and x1 + l1 > x2 and x1 - l1 < x2):
        return True
    else:
        return False

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
    elif(lineInterSection(x2, y2+h2, w2, x1-w1, y1, h1)):
        return True
    elif(lineInterSection(x2, y2-h2, w2, x1+w1, y1, h1)):
        return True
    elif(lineInterSection(x1, y1+h1, w1, x2-w2, y2, h2)):
        return True
    elif(lineInterSection(x1, y1-h1, w1, x2+w2, y2, h2)):
        return True
    else: 
        return False

# is the point (x2, y2) inside the box defined by the other variables
def isInsideBox(x1, y1, w1, h1, x2, y2):
    if (x2 > x1 - w1 and x2 < x1 + w1 and y2 > y1 - h1 and y2 < y1 + h1):
        return True
    else:
        return False
    
def isInsideDungeon(x, y):
    if (len(roomCenterX) == 0):
        return True

    for i in range(0, len(roomCenterX)):
        if (isInsideBox(roomCenterX[i], roomCenterY[i], roomWidth[i], roomHeight[i], x, y)):
            return True
        
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

def clearGlobalLists():
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

    global eventMessages
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

    eventMessages = []

    # generate the dungeon for the first time, and save the coordinates of all rooms
def generateDungeon():
    clearGlobalLists()

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
        if (random.randint(0, 10) > 3 and i > 0):
            spawnChest(currentX, currentY)
            if (random.randint(0, 10) > 5):
                spawnCauldron(currentX, currentY-1)

        # spawning enemies
        if (random.randint(0, 10) > 5):
            spawnEnemyFromCurrentTable(currentX, currentY + 1)

        prevWidth = width
        prevHeight = height

    # since the exit is a feature, we just append its location to all the feature lists
    if (getFeatureType(roomCenterX[len(roomCenterX)-1], roomCenterY[len(roomCenterY)-1]) != "None"):
        removeFeature(roomCenterX[len(roomCenterX)-1], roomCenterY[len(roomCenterY)-1])

    featureX.append(roomCenterX[len(roomCenterX)-1])
    featureY.append(roomCenterY[len(roomCenterY)-1])
    featureType.append("Exit")
    featureTimer.append(-1)

    movePlayer(roomCenterX[0], roomCenterY[0])

def spawnEnemyFromCurrentTable(x, y):
    currentTable = 0

    if (floorNumber < round(finalFloorIndex/4)):
        currentTable = 0
    elif (floorNumber < round(finalFloorIndex/2)):
        currentTable = 1
    elif (floorNumber < round(finalFloorIndex/4*3)):
        currentTable = 2
    elif (floorNumber < round(finalFloorIndex)):
        currentTable = 3

    spawnEnemyFromTable(x, y, currentTable)

def spawnEnemy(x, y, name):
    enemyType.append(getIndexInList(name, enemyNames))
    enemyX.append(x)
    enemyY.append(y)
    enemyHealth.append(enemyMaxHealth[getIndexInList(name, enemyNames)])

# the final floor is hardcoded
def generateFinalDungeon():
    clearGlobalLists()

    roomCenterX.append(screenWidth/2)
    roomCenterY.append(screenHeight/2)
    roomWidth.append(12)
    roomHeight.append(4)

    # spawn the final boss
    spawnEnemy(roomCenterX[0], roomCenterY[0], 7)

    # player is on the left edge of the room
    movePlayer(roomCenterX[0] - roomWidth[0] + 1, roomCenterY[0])

    # no need to do anything with the exit, resetting the feature lists deletes it

def generateStartingFloor():
    clearGlobalLists()

    # since the exit is a feature, we just append its location to all the feature lists
    featureX.append(screenWidth/2)
    featureY.append(screenHeight/2)
    featureType.append("Exit")
    featureTimer.append(-1)

    # a horse and a training dummy spawn at the starting level
    # the dummy allows you to test weapon damage
    spawnEnemy(screenWidth/2 + 1, screenHeight/2 - 2, "Dummy")
    spawnEnemy(screenWidth/2 - 12, screenHeight/2 + 2, "Horse")

    spawnCauldron(screenWidth/2 - 2, screenHeight/2 - 2)

    spawnNote(screenWidth/2 - 1, screenHeight/2 - 1, "Many descend, few return.")

    movePlayer(screenWidth/2 - 4, screenHeight/2)

def spawnEnemyFromTable(x, y, tableIndex):
    if (tableIndex == 0):
        spawnEnemy(x, y, enemyTable1[random.randint(0, len(enemyTable1) - 1)])
    elif (tableIndex == 1):
        spawnEnemy(x, y, enemyTable2[random.randint(0, len(enemyTable2) - 1)])
    elif (tableIndex == 2):
        spawnEnemy(x, y, enemyTable3[random.randint(0, len(enemyTable3) - 1)])
    else:
        spawnEnemy(x, y, enemyTable4[random.randint(0, len(enemyTable4) - 1)])

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
def spawnCauldron(x, y):
    featureType.append("Cauldron")
    featureX.append(x)
    featureY.append(y)
    featureTimer.append(-1)
def spawnDoor(x, y):
    featureType.append("Door")
    featureX.append(x)
    featureY.append(y)
    featureTimer.append(-1)
def spawnNote(x, y, msg):
    featureType.append("Note: " + msg)
    featureX.append(x)
    featureY.append(y)
    featureTimer.append(-1)

def isNote(x, y):
    if (len(getFeatureType(x, y)) > 4):
        if (substring(getFeatureType(x, y), 0, 4) == "Note"):
            return True
    return False

def isNextToFeature(x, y, type):
    for i in range(0, len(featureType)):
        if (featureType[i] == type):
            if (isAdjacent(x, y, featureX[i], featureY[i])):
                return True
    
    return False


def getFeatureType(x, y):
    if (getElementInList(x, y, featureX, featureY) != -1):
        return featureType[getElementInList(x, y, featureX, featureY)]
    else:
        return "None"
    
def removeFeature(x, y):
    featureIndex = getElementInList(x, y, featureX, featureY)
    featureX.pop(featureIndex)
    featureY.pop(featureIndex)
    featureType.pop(featureIndex)
    featureTimer.pop(featureIndex)

# ====================================
# INVENTORY:
# ====================================

def tryCraft(userInput):
    userInput = userInput.strip()

    # first, split the user input into a bunch of indices
    itemIndices = []

    lastCommaIndex = 0

    for i in range(0, len(userInput)):
        if (userInput[i] == ","):
            itemIndices.append(substring(userInput, lastCommaIndex, i - lastCommaIndex))
            lastCommaIndex = i

    # make sure to get the last argument as well
    itemIndices.append(str(substring(userInput, lastCommaIndex + 1, len(userInput) - 1- lastCommaIndex)))

    recipeString = ""

    for i in range(0, len(itemIndices)):
        recipeString += inventory[int(itemIndices[i]) - 1]
        if (i < len(itemIndices) - 1):
            recipeString += ","
    
    for i in range(0, len(craftingRecipes)):
        if (craftingRecipes[i] == recipeString):
            # remove all items from the inventory
            removeItemsFromInventory(itemIndices)

            # add the crafted item
            addItemToInventory(getIndexInList(craftingResults[i], itemTypes))

            # tell the user they made an item
            recordEvent("Crafted a " + craftingResults[i] + ".")

            return

    recordEvent("Tried to craft something, and failed.")

def recordEvent(eventName):
    eventMessages.append(eventName)

def addItemFormatting(itemName):
    itemIndex = findItemIndex(itemName)

    if (specialType[itemIndex] == 1):
        # fire-spawning weapons become magenta
        return str(Fore.MAGENTA) + itemName + str(Style.RESET_ALL)
    elif (specialType[itemIndex] > 1):
        # all potions (except healing ones) become blue
        return str(Fore.BLUE) + itemName + str(Style.RESET_ALL)
    elif (itemDamage[itemIndex] < 0):
        # healing items become red
        return str(Fore.RED) + itemName + str(Style.RESET_ALL)
    elif (itemInList(itemName, weapons)):
        # weapons are yellow
        return str(Fore.YELLOW) + itemName + str(Style.RESET_ALL)
    else:
        # anything else (really just potion ingredients) is green
        return str(Fore.GREEN) + itemName + str(Style.RESET_ALL)
    
    # not using white for items, for now, because it's harder to read

# called when the player opens a chest, adds the loot from the chest to the inventory
def addLoot():
    # first, give the player a random ingredient
    itemName = ingredients[random.randint(0, len(ingredients)-1)]
    inventory.append(itemName)
    recordEvent("Picked up a " + itemName + ".")

    # then, try and give them a weapon
    # if they have the weapon already, give them another ingredient
    itemName = weapons[random.randint(0, len(weapons)-1)]
    if (itemInList(itemName, inventory)):
        itemName = ingredients[random.randint(0, len(ingredients)-1)]

    inventory.append(itemName)
    recordEvent("Picked up a " + itemName + ".")

def addItemToInventory(index):
    inventory.append(itemTypes[index])

def removeItemsFromInventory(indexList):
    # looping through all features and destroying temporary ones that have run out of time
    startingLength = len(inventory)
    for i in range(0, startingLength):
        j = startingLength - i

        # doesn't matter what type of feature it is, 
        # as long as it has a positive or zero value for its timer
        # keep in mind -1 is for permanent features
        if (itemInList(str(j), indexList)):
            # THIS COULD POSSIBLY CAUSE OTHER FEATURES TO GET MESSED UP BECAUSE THE INDICES SHIFT,
            # BE CAREFUL
            inventory.pop(j-1)
            indexList.pop(getIndexInList(str(j), indexList))

def findItemIndex(itemName):
    for i in range(0, len(itemTypes)):
        if (itemTypes[i] == itemName):
            return i
    
    return -1

def findItemIndexInInventory(itemName):
    for i in range(0, len(inventory)):
        if (inventory[i] == itemName):
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
    # health potion's are not equipped, they are just used
    if (itemDamage[findItemIndex(inventory[oldIndex])] < 0):
        damagePlayer(itemDamage[findItemIndex(inventory[oldIndex])], "Health")
        recordEvent("Healed " + str(itemDamage[findItemIndex(inventory[oldIndex])] * -1) + " health.")
        if (isConsumable[findItemIndex(inventory[oldIndex])]):
            inventory.pop(oldIndex)
        return
    # fire resistance
    elif (specialType[findItemIndex(inventory[oldIndex])] == 2):
        recordEvent("Drank " + inventory[oldIndex] + ".")
        statusEffectTimers[0] = itemReach[findItemIndex(inventory[oldIndex])]

        if (isConsumable[findItemIndex(inventory[oldIndex])]):
            inventory.pop(oldIndex)
        return
    # strength
    elif (specialType[findItemIndex(inventory[oldIndex])] == 3):
        recordEvent("Drank " + inventory[oldIndex] + ".")
        statusEffectTimers[1] = itemReach[findItemIndex(inventory[oldIndex])]

        if (isConsumable[findItemIndex(inventory[oldIndex])]):
            inventory.pop(oldIndex)
        return
    # speed
    elif (specialType[findItemIndex(inventory[oldIndex])] == 4):
        recordEvent("Drank " + inventory[oldIndex] + ".")
        statusEffectTimers[3] = itemReach[findItemIndex(inventory[oldIndex])]

        if (isConsumable[findItemIndex(inventory[oldIndex])]):
            inventory.pop(oldIndex)
        return
    # ironskin
    elif (specialType[findItemIndex(inventory[oldIndex])] == 5):
        recordEvent("Drank " + inventory[oldIndex] + ".")
        statusEffectTimers[2] = itemReach[findItemIndex(inventory[oldIndex])]

        if (isConsumable[findItemIndex(inventory[oldIndex])]):
            inventory.pop(oldIndex)
        return
    # random effect
    elif (specialType[findItemIndex(inventory[oldIndex])] == 6):
        recordEvent("Drank " + inventory[oldIndex] + ".")
        statusEffectTimers[random.randint(0, len(statusEffectTimers)-1)] = itemReach[findItemIndex(inventory[oldIndex])]

        if (isConsumable[findItemIndex(inventory[oldIndex])]):
            inventory.pop(oldIndex)
        return
    
    recordEvent("Equipped " + inventory[oldIndex] + ".")

    inventory.insert(0, inventory[oldIndex])
    inventory.pop(oldIndex + 1)

# ====================================
# UTILITY
# ====================================

def itemInList(item, list):
    counter = 0
    for i in list:
        if (item == i):
            return True
        counter += 1

    return False

def getIndexInList(item, list):
    counter = 0
    for i in list:
        if (item == i):
            return counter
        counter += 1

    return -1

def substring(string, startIndex, length):
    returnString = ""
    counter = 0

    for i in string:
        if (counter >= startIndex and counter < startIndex + length):
            returnString += i
        counter += 1

    return returnString

# boolean function for figuring out if a string represents a number
def isNumber(string):
    # get rid of whitespace
    string = string.replace(" ","")

    if (len(string) == 0):
        return False

    counter = 0
    
    for i in string:
        if (i == "1" or i == "2" or i == "3" or i == "4" or i == "5" or i == "6" or i == "7" or i == "8" or i == "9" or i == "0" or (i == "-" and counter == 0)):
            # do nothing, this character is fine
            continue
        else:
            return False
        counter += 1
    
    return True

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

def indent():
    for i in range(0, 30):
        print("")

def drawScreen():
    # spacing, for neatness
    indent()

    drawUpperUI()

    # drawing the world
    currentLine = ""
    for i in range(screenHeight):
        for j in range(screenWidth):
            if (playerX == j and playerY == i):
                currentLine += str(Fore.CYAN) + "&" + str(Style.RESET_ALL)
            elif (getEnemyCharacter(j, i) != "no enemy"):
                currentLine += str(Fore.RED) + getEnemyCharacter(j, i) + str(Style.RESET_ALL)
            elif (isNote(j, i)):
                currentLine += str(Fore.CYAN) + "~" + str(Style.RESET_ALL)
            elif (getFeatureType(j, i) == "Cauldron"):
                currentLine += str(Fore.GREEN) + "ö" + str(Style.RESET_ALL)
            elif (isWall(j, i)):
                currentLine += "#"
            elif (getFeatureType(j, i) == "Door"):
                currentLine += str(Fore.YELLOW) + "◘" + str(Style.RESET_ALL)
            elif (getFeatureType(j, i) == "Exit"):
                currentLine += str(Fore.BLUE) + "↓" + str(Style.RESET_ALL)
            elif (getFeatureType(j, i) == "Fake Exit"):
                # for now, these have the same character as the normal exit
                currentLine += str(Fore.BLUE) + "↓" + str(Style.RESET_ALL)
            elif (getFeatureType(j, i) == "Chest"):
                currentLine += str(Fore.GREEN) + "◙" + str(Style.RESET_ALL)
            elif (getFeatureType(j, i) == "Flame" and isInsideDungeon(j, i)):
                currentLine += str(Fore.MAGENTA) + "!" + str(Style.RESET_ALL)
            else:
                if (isInsideDungeon(j, i)):
                        currentLine += str(Style.DIM) + "." + str(Style.RESET_ALL)
                else:
                    currentLine += str(Style.DIM) + "#" + str(Style.RESET_ALL)

        if (i < len(tooltips) and areTipsActive):
            currentLine += "  " + tooltips[i]
        
        print(currentLine)
        currentLine = ""

    drawLowerUI()

def blankScreen():
    # spacing, for neatness
    indent()

    defaultCharacter = "."

    currentLine = ""
    for i in range(screenHeight):
        for j in range(screenWidth):
            currentLine += defaultCharacter
                
        print(currentLine)
        currentLine = ""

def fullscreenMessage(msg, showContinueMessage, showUI, colorName):
    msg = str(msg)

    # spacing, for neatness
    indent()

    if (showUI):
        drawUpperUI()

    defaultCharacter = "."
    textColor = str(Fore.CYAN)

    if (colorName == "red"):
        textColor = str(Fore.RED)
    elif (colorName == "blue"):
        textColor = str(Fore.BLUE)
    elif (colorName == "cyan"):
        textColor = str(Fore.CYAN)
    elif (colorName == "green"):
        textColor = str(Fore.GREEN)
    elif (colorName == "magenta"):
        textColor = str(Fore.MAGENTA)
    elif (colorName == "yellow"):
        textColor = str(Fore.YELLOW)

    currentLine = ""
    for i in range(screenHeight):
        for j in range(screenWidth):
            if (i == screenHeight/2):
                startingIndex = screenWidth / 2 - round(len(msg)/2)
                if (j >= startingIndex and j < startingIndex + round(len(msg))):
                    currentLine += textColor + getCharacter(msg, j - startingIndex) + str(Style.RESET_ALL)
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

    if (showUI):
        drawLowerUI()

def getHealthUIColor():
    if (statusEffectTimers[2] > 0):
        return str(Fore.CYAN)
    elif (statusEffectTimers[0] > 0):
        return str(Fore.YELLOW)
    else:
        return str(Fore.RED)

def addDamageFormatting(string):
    if (statusEffectTimers[1] > 0):
        return str(Fore.RED) + str(int(string) * 2) + str(Style.RESET_ALL)
    else:
        return str(string)

# draw the stuff that shows up above the game worldd
# right now, thats some basic stats and events
def drawUpperUI():
    # player stats ---------------------------
    lineString = ""
    for i in range(0, screenWidth):
        lineString += "-"
    print(lineString)

    print("Health: " + str(getHealthUIColor()) + formatNumber(playerHealth, 3) + str(Style.RESET_ALL) + "     Floor Number: " + str(Fore.BLUE) + formatNumber(floorNumber, 3) + str(Style.RESET_ALL) + "     Equipped Item: " + str(addItemFormatting(getEquippedWeapon())) + " (dmg: " + str(addDamageFormatting(itemDamage[getIndexInList(getEquippedWeapon(), itemTypes)])) + ")")

    drawDivider()
    # ---------------------------

    # event messages ---------------
    eventString = str(Fore.CYAN)
    global eventMessages

    for i in eventMessages:
        eventString += i + " "

    eventString += str(Style.RESET_ALL)
    print(eventString)
    eventMessages = []

    drawDivider()
    # ---------------------------

# draw the stuff that shows up under the game world
# right now, that's the inventory
def drawLowerUI():
    # the lower UI (inventory) ---------------------------
    drawDivider()

    print("Inventory:")
    
    # the inventory is made up of 4 columns, each with a number and an item
    numColumns = 4
    columnWidth = int(screenWidth/4)

    indexCounter = 1
    columnCounter = 0
    inventoryString = ""
    stringNoFormatting = ""

    for i in inventory:
        if (columnCounter < numColumns - 1):
            inventoryString = addBlankSpace(inventoryString, int(columnWidth) * int(columnCounter) - len(stringNoFormatting))
            inventoryString += str(indexCounter) + ". "
            inventoryString += addItemFormatting(i) + " "

            stringNoFormatting = addBlankSpace(stringNoFormatting, int(columnWidth) * int(columnCounter) - len(stringNoFormatting))
            stringNoFormatting += str(indexCounter) + ". "
            stringNoFormatting += i + " "

            columnCounter += 1
        else:
            inventoryString = addBlankSpace(inventoryString, int(columnWidth) * int(columnCounter) - len(stringNoFormatting))
            inventoryString += str(indexCounter) + ". "
            inventoryString += addItemFormatting(i) + " "

            stringNoFormatting = addBlankSpace(stringNoFormatting, int(columnWidth) * int(columnCounter) - len(stringNoFormatting))
            stringNoFormatting += str(indexCounter) + ". "
            stringNoFormatting += i + " "
            
            print(inventoryString)

            columnCounter = 0

            inventoryString = ""
            stringNoFormatting = ""
        
        indexCounter += 1

    if (len(inventoryString) > 0):
        print(inventoryString)

    drawDivider()
    # ---------------------------

def addBlankSpace(inputString, spaceCount):
    for i in range(0, spaceCount):
        inputString += " "

    return inputString

# draws a dividing line (UI)
def drawDivider():
    lineString = ""
    for i in range(0, screenWidth):
        lineString += "-"
    print(lineString)

# ====================================
# GAME LOGIC
# ====================================

# go through the intro text, should only happen upon booting the game for the first time
def runIntro():
    fullscreenMessage("FakeVoxel presents", True, False, "magenta")
    input("")
    fullscreenMessage("PYROGUE" + " (" + versionString + ")", True, False, "magenta")
    input("")

    # exposition
    fullscreenMessage("   First, the war.   ", True, False, "cyan")
    input("")
    fullscreenMessage("   Then, the siege.   ", True, False, "cyan")
    input("")

    fullscreenMessage("   We held up for almost a month.   ", True, False, "cyan")
    input("")
    fullscreenMessage("   But we couldn't wait forever.   ", True, False, "cyan")
    input("")
    fullscreenMessage("   They wanted the king, those were their terms.   ", True, False, "cyan")
    input("")
    fullscreenMessage("   Well they got what they wanted.   ", True, False, "cyan")
    input("")

    fullscreenMessage("   Rumor has it they killed him, and buried him here.   ", True, False, "cyan")
    input("")
    fullscreenMessage("   Still wearing the crown.   ", True, False, "cyan")
    input("")
    fullscreenMessage("   ...   ", True, False, "cyan")
    input("")
    fullscreenMessage("   My crown.   ", True, False, "cyan")
    input("")

    blankScreen()
    input("")

def selectGameMode():
    global gameMode

    fullscreenMessage("   Type the desired game mode and hit enter: 'normal', 'endless'   ", False, False, "cyan")
    gameModeInput = input("")

    if (gameModeInput == "normal"):
        gameMode = 0
    elif (gameModeInput == "endless"):
        gameMode = 1
    else:
        gameMode = 0

    # showing the user what gamemode they picked
    if (gameMode == 0):
        fullscreenMessage("   Normal mode selected. Good luck, traveller.   ", True, False, "green")
    else:
        fullscreenMessage("   Endless mode selected. Good luck, traveller.  ", True, False, "green")
    
    input("")

def invalidCommand():
    # the player inputted a command that isn't valid
    recordEvent("That's not a valid command, no time passes.")
    drawScreen()
    promptUserForAction()

def promptUserForAction():
    action = input("")
    # y axis is reversed, keep in mind

    global areTipsActive

    # player movement ----
    # you can wait just by hitting enter btw!
    if (action == "w"):
        movePlayer(playerX, playerY - 1)
    elif (action == "s"):
        movePlayer(playerX, playerY + 1)
        
    elif (action == "a"):
        movePlayer(playerX - 1, playerY)
    elif (action == "d"):
        movePlayer(playerX + 1, playerY)
    # --------

    # equip/use an item
    elif (getCharacter(action, 0) == "e"):
        if (isNumber(action.replace(" ","").replace("e", ""))):
            equipItem(int(action.replace(" ","").replace("e", "")) - 1)
        else:
            invalidCommand()

    # attacking (left, right, down, up)
    elif(getCharacter(action, 0) == "x"):
        if (len(action) < 2):
            invalidCommand()
        else:
            attack(action.replace("x","").replace(" ",""))

    # attempting to craft an item
    elif (getCharacter(action, 0) == "c"):
        if (isNextToFeature(playerX, playerY, "Cauldron")):
            tryCraft(action.replace("c","").replace(" ",""))
        else:
            # can't craft if not next to a cauldron
            recordEvent("You can't craft when not next to a cauldron, no time passes.")
            drawScreen()
            promptUserForAction()

    # restarting the game
    elif (action == "r"):
        startNewGame()

    # toggle tips on/off
    elif (action == "t"):
        if (areTipsActive):
            areTipsActive = False
        else:
            areTipsActive = True

        # this command doesn't take time
        drawScreen()
        promptUserForAction()

    elif (action == ""):
        recordEvent("You decide to wait.")
    else:
        invalidCommand()

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
    generateStartingFloor()

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

# called when the player dies
def gameOver():
    fullscreenMessage("   GAME OVER   ", False, True, "red")
    input("")

# called once the player is in the final room and there are no enemies
def gameWin():
    fullscreenMessage("   The necromancer and his minions fall to the ground, lifeless.   ", True, True, "cyan")
    input("")

    fullscreenMessage("   You climb down one last set of stairs, and there lies the king.   ", True, True, "cyan")
    input("")

    fullscreenMessage("   On the ground beside him, the crown.   ", True, True, "cyan")
    input("")

    fullscreenMessage("   VICTORY   ", False, True, "green")
    input("")

def roomIntro():
    # first dungeon floor
    if (floorNumber == 1):
        fullscreenMessage("   The air feels damp. You see something small scurry away.   ", True, True, "cyan")
        input("")
    elif (floorNumber == round(finalFloorIndex/4)):
        fullscreenMessage("   You hear voices down the hall. Did they station guards here?.   ", True, True, "cyan")
        input("")
    elif (floorNumber == round(finalFloorIndex/4*2)):
        fullscreenMessage("   You feel a rush of cold air against your face. A shimmering figure floats in the distance.   ", True, True, "cyan")
        input("")
    elif (floorNumber == round(finalFloorIndex/4*3)):
        fullscreenMessage("   A pile of bones shifts in the corner, and you think back to the siege.  ", True, True, "cyan")
        input("")
        fullscreenMessage("   They didn't have more soldiers. But their soldiers couldn't die.  ", True, True, "cyan")
        input("")
    elif (floorNumber == finalFloorIndex):
        fullscreenMessage("   That was how they won the war. Necromancy. And they brought a necromancer here?   ", True, True, "cyan")
        input("")

# main logic function, calls itself
# the function that is called every "turn"
def runGameLogic():
    global isBonusTurn

    # check if the game is over (player died, or won) before handling any logic
    if (playerHealth <=0):
        gameOver()
        return
    if (floorNumber == finalFloorIndex and len(enemyType) == 0):
        gameWin()
        return

    # get the player to type a command, and perform whatever logic that does
    # this function handles all that
    promptUserForAction()

    # only allow creatures to move and potions to deplete if it's not the player's bonus turn
    # bonus turns happen every other turn, while the player has the swiftness effect
    if (not isBonusTurn):
        # killing any dead enemies
        refreshEnemyData()
        # move the remaining ones
        moveAllEnemies()
        
        # give the player a bonus turn next turn if they have swiftness
        if (statusEffectTimers[3] > 0):
            isBonusTurn = True

        # fire only damages enemies during a not-bonus turn
        for i in range(0, len(enemyType)):
            if (getFeatureType(enemyX[i], enemyY[i]) == "Flame"):
                enemyHealth[i] -= 1

        # delete any temporary hazards that have run out of time
        refreshTemporaryHazards()

        # remove 1 from all current status effects, potions do not deplete during bonus turns
        for i in range(0, len(statusEffectTimers)):
            if (statusEffectTimers[i] > 0):
                statusEffectTimers[i] -= 1
    else:
        # killing any dead enemies
        refreshEnemyData()

        isBonusTurn = False

    # fire damages player during all turns, even bonus ones
    if (getFeatureType(playerX, playerY) == "Flame"):
        damagePlayer(1, "Fire")

    # at the very very end of the turn, do logic relating to features
    if (getFeatureType(playerX, playerY) == "Exit"):
        nextFloor()
        roomIntro()
    elif (getFeatureType(playerX, playerY) == "Chest"):
        addLoot()
        removeFeature(playerX, playerY)
    elif (len(getFeatureType(playerX, playerY)) > 4):
        if (substring(getFeatureType(playerX, playerY), 0, 4) == "Note"):
            fullscreenMessage("     There is a note that reads: " + substring(getFeatureType(playerX, playerY), 6, len(getFeatureType(playerX, playerY)) - 6) + "     ", True, True, "cyan")
            removeFeature(playerX, playerY)
            input("")

    drawScreen()

    runGameLogic()

colorama_init()

if (debugMode):
    debugItemData()

# the only bit of code that isn't in a function lol
if (not skipIntro):
    runIntro()

selectGameMode()

startNewGame()
drawScreen()

# calling this starts the main game loop
runGameLogic()
