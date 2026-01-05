import keyboard
import time

pressCount = 0
isKeyPressed = False

def waitForKeyPress():
    while True:  # making a loop
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('q'):  # if key 'q' is pressed 
                return 'q'
            else:
                return ""
        except:
            break  # if user pressed a key other than the given key the loop will break

def pressKey():
    if (not isKeyPressed):
        isKeyPressed = True
        pressCount += 1

def main():
    global pressCount
    global isKeyPressed

    if (not isKeyPressed):
        while(waitForKeyPress() == ""):
            ## wait
            pressCount = pressCount
            isKeyPressed = False
        isKeyPressed = True
        pressCount += 1
        print(pressCount)
    else:
        while(waitForKeyPress() != ""):
            ## wait
            pressCount = pressCount
            isKeyPressed = True
        isKeyPressed = False

while (1 == 1):
    main()
    time.sleep(0.1)