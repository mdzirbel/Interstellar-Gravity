import sys, pygame
pygame.init()
from random import randint
import math

size = width, height = 1300, 750

gameboardTop = 50
gameboardBottom = 50
gameboardLeft = 50
gameboardRight = 50
gameboardWidth = (size[0] - gameboardLeft - gameboardRight) # The width of the black box itself
gameboardHeight = (size[1] - gameboardTop - gameboardBottom)

statusReportBox = 0, size[1] - gameboardBottom, 150, gameboardBottom # x pos of top left, y pos of top left, x width, y width

# starRadius = 10
# planetRadius = 6
# blackHoleRadius = 8
# antiGravityRadius = 7
# goldilocksRadius = 13

radii = {"star":10, "planet":6, "black hole":8, "anti gravity":7, "goldilocks":13}

bodies = []

gravity = 10
baseSpeed = 3
speed = baseSpeed # Speed will be changed by pausing and such but baseSpeed will be the same

bodyCooldown = 0

goldilocksZone = 150

statusReportFont = pygame.font.Font(None, 20)
statusTextHeight = 13

numTracers = 3
tracerSpeed = 10 # This is the number of times it runs the movebodies function (it controls the forloop within numbodies) when finding tracer thingies

starMass = 3
planetMass = 1/300000
blackHoleMass = 20
antiGravityMass = -9
goldilocksMass = 10

initvelx = 0.0
initvely = 0.0

black = 0, 0, 0
green = 0, 255, 0
red = 255, 0, 0
blue = 0, 0, 255
gray = 190, 190, 190
yellow = 255, 255, 0
star = 255, 255, 0
brown = 102, 51, 0
white = 255, 255, 255
silver = 192, 192, 192
purple = 128, 0, 128
orange = 255, 69, 0

leftButton = False
rightButton = False

buttonFont = pygame.font.Font(None, 40)
redXText = buttonFont.render("X", True, red)
pauseText = buttonFont.render("ll", True, red)
inputText = buttonFont.render("=", True, red)
buttonList = [] # Don't change this unless you remember why you wrote this comment
buttons = [] # This can be changed whenever it will actually mean something
buttonSize = 35, 35 # x, y

leftMouse = False
rightMouse = False

leftBody = False
rightBody = False

bodyCount = [0, 0, 0, 0, 0] # Stars, Planets, Black Holes, Anti Gravity, Goldilocks

startPlanet = 1

clock = pygame.time.Clock()

screen = pygame.display.set_mode(size)

def drawScreen():
    screen.fill(gray)

    pygame.draw.rect(screen, yellow, (0*buttonSize[0], 0, buttonSize[0], buttonSize[1]))
    pygame.draw.rect(screen, brown, (1*buttonSize[0], 0, buttonSize[0], buttonSize[1]))
    pygame.draw.rect(screen, black, (2*buttonSize[0], 0, buttonSize[0], buttonSize[1]))
    pygame.draw.rect(screen, purple, (3*buttonSize[0], 0, buttonSize[0], buttonSize[1]))
    pygame.draw.rect(screen, orange, (4*buttonSize[0], 0, buttonSize[0], buttonSize[1]))

    pygame.draw.rect(screen, white, (size[0] - buttonSize[0], 0*buttonSize[1], buttonSize[0], buttonSize[1]-1)) # Draws white box for X
    screen.blit(redXText, (size[0] - buttonSize[0] + 9, 5 + 0*buttonSize[1]))                                    # Draws X in white box

    pygame.draw.rect(screen, white, (size[0] - buttonSize[0], 1*buttonSize[1], buttonSize[0], buttonSize[1]-1)) # Draws white box for ll
    screen.blit(pauseText, (size[0] - buttonSize[0] + 9, 5 + 1*buttonSize[1]))

    pygame.draw.rect(screen, white, (size[0] - buttonSize[0], 2*buttonSize[1], buttonSize[0], buttonSize[1]-1)) # Draws white box for X
    screen.blit(inputText, (size[0] - buttonSize[0] + 10, 1 + 2*buttonSize[1])) 

    pygame.draw.rect(screen, black, (gameboardLeft, gameboardTop, gameboardWidth, gameboardHeight))

drawScreen()

class body:
    def __init__(self, bodyType, mass, velx, vely, posx, posy):
        self.type = bodyType
        self.mass = mass
        self.velx = velx
        self.vely = vely
        self.posx = posx
        self.posy = posy

def inBlackBox(x, y):
    if x <= gameboardLeft + gameboardWidth and x >= gameboardLeft and y <= gameboardTop + gameboardHeight and y >= gameboardTop:
        return True
    else:
        return False

def drawBodies(surface, bodies): #mass, xpos, ypos):
    pygame.draw.rect(screen, black, (gameboardLeft, gameboardTop, gameboardWidth, gameboardHeight))
    for body in bodies:
        if inBlackBox(body.posx, body.posy):
            if body.type == "star":
                pygame.draw.circle(surface, yellow, (int(body.posx), int(body.posy)), radii["star"], 0)
            elif body.type == "planet":
                pygame.draw.circle(surface, brown, (int(body.posx), int(body.posy)), radii["planet"], 0)
            elif body.type == "black hole":
                pygame.draw.circle(surface, silver, (int(body.posx), int(body.posy)), radii["black hole"], 1) # The 1 is for not filled in
            elif body.type == "anti gravity":
                pygame.draw.circle(surface, purple, (int(body.posx), int(body.posy)), radii["anti gravity"], 0)
            elif body.type == "goldilocks":
                pygame.draw.circle(surface, orange, (int(body.posx), int(body.posy)), radii["goldilocks"], 0)
                pygame.draw.circle(surface, orange, (int(body.posx), int(body.posy)), goldilocksZone, 1) # Creates a circle where the goldilocksZone is

def moveBodies(bodies, bodyCount, speed, radii, goldilocksZone):
    for a in range(0, speed): # Tells the function to do this speed times
        for i in range(0, len(bodies)):
            bodies[i].accelx = 0
            bodies[i].accely = 0
            for j in range(0, len(bodies)): 
                if i != j:
                    if bodies[i].type == "planet": # Only move planets
                        sepy = bodies[j].posy - bodies[i].posy # Sep is short for separation
                        sepx = bodies[j].posx - bodies[i].posx # Sep is short for separation
                        if bodies[i].type != "delete" and bodies[j].type != "delete" and abs(sepx) + abs(sepy) <= radii[bodies[i].type] + radii[bodies[j].type]:
                            if bodies[i].type == "planet":
                                bodies[i].type = "delete" # if they are too close it gets them ready for deletion
                            if bodies[j].type == "planet":
                                bodies[j].type = "delete"
                        elif bodies[i].posx < -3000 or bodies[i].posx > 5000 or bodies[i].posy < -4000 or bodies[i].posy > 4000:
                            bodies[i].type = "delete"
                            # print("Body is out of this world")
                        elif bodies[j].type == "goldilocks":
                            if (sepx**2+sepy**2)**(1/2) < goldilocksZone:
                                k = -gravity*(bodies[j].mass)/(math.sqrt(sepx * sepx + sepy * sepy) ** 3) # Sep is short for separation
                                bodies[i].accelx = bodies[i].accelx + sepx * k
                                bodies[i].accely = bodies[i].accely + sepy * k
                            elif (sepx**2+sepy**2)**(1/2) > goldilocksZone:
                                k = gravity*(bodies[j].mass)/(math.sqrt(sepx * sepx + sepy * sepy) ** 3) # Sep is short for separation
                                bodies[i].accelx = bodies[i].accelx + sepx * k
                                bodies[i].accely = bodies[i].accely + sepy * k
                        else:
                            k = gravity*(bodies[j].mass)/(math.sqrt(sepx * sepx + sepy * sepy) ** 3) # Sep is short for separation
                            bodies[i].accelx = bodies[i].accelx + sepx * k
                            bodies[i].accely = bodies[i].accely + sepy * k

        for i in range(0, len(bodies)):
            bodies[i].velx = bodies[i].velx + bodies[i].accelx
            bodies[i].vely = bodies[i].vely + bodies[i].accely

        for i in range(0, len(bodies)):
            bodies[i].posx = bodies[i].posx + bodies[i].velx
            bodies[i].posy = bodies[i].posy + bodies[i].vely

        i = 0
        while i < len(bodies):
            if bodies[i].type == "delete":
                bodies.remove(bodies[i])
                bodyCount[1] = bodyCount[1] - 1
            i += 1

    return bodies, bodyCount

def expectedRoute(bodies, bodyCount, speed, tracerSpeed):
    the = 2

def clearScreen(baseSpeed):
    bodies = []
    drawScreen()
    bodyCount = [0, 0, 0, 0, 0]
    speed = baseSpeed
    return bodies, bodyCount, speed

def pausePlay(speed, baseSpeed):
    if speed == 0:
        speed = baseSpeed
        # print("Speed changed to baseSpeed: " + str(speed))
    elif speed > 0:
        # print(str(speed))
        speed = 0
    return speed

def variableEditor(gravity, speed, size):
    inputType = input("What type of change do you want to make? ")
    inputNumber = input("What number do you want to set this to? ")
    
    if inputType == "gravity":
        gravity = float(inputNumber)
    elif inputType == "speed":
        speed = int(inputNumber)
    elif inputType == "size[0]" or inputType == "size0":
        size = int(inputNumber), size[1]
        drawScreen()
    elif inputType == "size[1]" or inputType == "size1":
        size[1] = int(inputNumber)
        drawScreen()

    else:
        print("please enter a variable name and then a number.")
        print("allowed variable names are: gravity, speed, size[0], size[1]")
 
    return gravity, speed, size

def functionButtons(buttonSize, event, functionButtonList, bodies, bodyCount, speed, baseSpeed, gravity, size):
    for button in functionButtonList:
        if event.pos[0] <= size[0] \
        and event.pos[0] >= size[0] - buttonSize[0] \
        and event.pos[1] <= button["buttonNumber"] * buttonSize[1] + buttonSize[1] \
        and event.pos[1] >= button["buttonNumber"] * buttonSize[1]:

            if button["type"] == "clear screen":
                bodies, bodyCount, speed = clearScreen(baseSpeed)
            elif button["type"] == "pause play":
                speed = pausePlay(speed, baseSpeed)
            elif button["type"] == "input":
                gravity, speed, size = variableEditor(gravity, speed, size)

    return bodies, bodyCount, speed, gravity, size

def buttonPressSpot(buttonSize, event, buttonList, leftBody, rightBody, leftMouse, rightMouse, bodies, leftButton, rightButton):
    for button in buttonList:
        if event.pos[0] <= button["buttonNumber"] * buttonSize[0] + buttonSize[0] \
        and event.pos[0] >= button["buttonNumber"] * buttonSize[0] \
        and event.pos[1] <= buttonSize[1] \
        and event.pos[1] >= 0:
            if leftMouse == True:
                    leftBody = button["type"]
                    leftButton = button["color"]
            elif rightMouse == True:
                    rightBody = button["type"]
                    rightButton = button["color"]

    return bodies, leftBody, rightBody, bodyCount, leftButton, rightButton

def functionButtonSetup():
    functionButtonList = []

    button0 = {}
    button0["type"] = "clear screen"
    button0["buttonNumber"] = 0
    functionButtonList.append(button0)

    button1 = {}
    button1["type"] = "pause play"
    button1["buttonNumber"] = 1
    functionButtonList.append(button1)

    button2 = {}
    button2["type"] = "input"
    button2["buttonNumber"] = 2
    functionButtonList.append(button2)

    button3 = {}
    button3["type"] = "gravity field"
    button3["buttonNumber"] = 3
    functionButtonList.append(button3)

    return functionButtonList

def buttonSetup(buttons, event, buttonSize, leftBody, rightBody):
    buttonList = []

    button0 = {}
    button0["type"] = "star"
    button0["buttonNumber"] = 0
    button0["color"] = yellow
    buttonList.append(button0)

    button1 = {}
    button1["type"] = "planet"
    button1["buttonNumber"] = 1
    button1["color"] = brown
    buttonList.append(button1)

    button2 = {}
    button2["type"] = "black hole"
    button2["buttonNumber"] = 2
    button2["color"] = black
    buttonList.append(button2)

    button3 = {}
    button3["type"] = "anti gravity"
    button3["buttonNumber"] = 3
    button3["color"] = purple
    buttonList.append(button3)

    button4 = {}
    button4["type"] = "goldilocks"
    button4["buttonNumber"] = 4
    button4["color"] = orange
    buttonList.append(button4)

    return buttonList, leftBody, rightBody

def allTheClickStuff(bodies, leftMouse, rightMouse, leftBody, rightBody, startPlanet, bodyCount, speed, baseSpeed, leftButton, rightButton, gravity, size):

    accelx = 0
    accely = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
                
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:
                leftMouse = True
                #print("leftMouse: " + str(leftMouse))
                #print("rightMouse: " + str(rightMouse))
            if event.button == 3:
                rightMouse = True
                #print("leftMouse: " + str(leftMouse))
                #print("rightMouse: " + str(rightMouse))

            buttonList, leftBody, rightBody = buttonSetup(buttons, event, buttonSize, leftBody, rightBody)
            functionButtonList = functionButtonSetup()

            bodies, leftBody, rightBody, bodyCount, leftButton, rightButton \
            = buttonPressSpot(buttonSize, event, buttonList, leftBody, rightBody, leftMouse, rightMouse, bodies, leftButton, rightButton)
            bodies, bodyCount, speed, gravity, size \
            = functionButtons(buttonSize, event, functionButtonList, bodies, bodyCount, speed, baseSpeed, gravity, size)

            if leftButton != False:
                pygame.draw.rect(screen, leftButton, (5, 40, (gameboardLeft - 10)/2, buttonSize[1]))
            if rightButton != False:
                pygame.draw.rect(screen, rightButton, (5 + (gameboardLeft - 10)/2, 40, (gameboardLeft - 10)/2, buttonSize[1]))

            if leftMouse == True and inBlackBox(event.pos[0], event.pos[1]):

                if leftBody == "star":
                    bodies.append(body(leftBody, starMass, 0, 0, event.pos[0], event.pos[1]))
                    bodyCount[0] += 1

                elif leftBody == "black hole":
                    bodies.append(body(leftBody, blackHoleMass, 0, 0, event.pos[0], event.pos[1]))
                    bodyCount[2] += 1

                elif leftBody == "anti gravity":
                    bodies.append(body(leftBody, antiGravityMass, 0, 0, event.pos[0], event.pos[1]))
                    bodyCount[3] += 1

                elif leftBody == "goldilocks":
                    bodies.append(body(leftBody, goldilocksMass, 0, 0, event.pos[0], event.pos[1]))
                    bodyCount[4] += 1

                elif leftBody == "planet":
                    startPlanet = event.pos[0], event.pos[1], "left"
                    # We dont change numPlanets here because this is changed upon planet creation, when the mouse button is released

            elif rightMouse == True and inBlackBox(event.pos[0], event.pos[1]):

                if rightBody == "star":
                    bodies.append(body(rightBody, starMass, 0, 0, event.pos[0], event.pos[1]))
                    bodyCount[0] += 1

                elif rightBody == "black hole":
                    bodies.append(body(rightBody, blackHoleMass, 0, 0, event.pos[0], event.pos[1]))
                    bodyCount[2] += 1

                elif rightBody == "anti gravity":
                    bodies.append(body(rightBody, antiGravityMass, 0, 0, event.pos[0], event.pos[1]))
                    bodyCount[3] += 1

                elif rightBody == "goldilocks":
                    bodies.append(body(rightBody, goldilocksMass, 0, 0, event.pos[0], event.pos[1]))
                    bodyCount[4] += 1

                elif rightBody == "planet":
                    startPlanet = event.pos[0], event.pos[1], "right"
                    # We dont change numPlanets here because this is changed upon planet creation, when the mouse button is released

        elif event.type == pygame.MOUSEBUTTONUP: # For making planets with velocity
            if startPlanet != 1:

                if startPlanet[2] == "left":
                    bodies.append(body(leftBody, planetMass, 0.01*(event.pos[0] - startPlanet[0]), 0.01*(event.pos[1] - startPlanet[1]), startPlanet[0], startPlanet[1]))
                    if leftBody == "planet":
                        bodyCount[1] += 1

                elif startPlanet[2] == "right":
                    bodies.append(body(rightBody, planetMass, 0.01*(event.pos[0] - startPlanet[0]), 0.01*(event.pos[1] - startPlanet[1]), startPlanet[0], startPlanet[1]))
                    if rightBody == "planet":
                        bodyCount[1] += 1

                startPlanet = 1

            #print("Setting leftMouse and rightMouse to False")
            leftMouse = False
            rightMouse = False

    return bodies, leftMouse, rightMouse, leftBody, rightBody, startPlanet, bodyCount, speed, gravity, size

def statusReport(statusReportBox):
    pygame.draw.rect(screen, gray, statusReportBox)
    screen.blit(statusReportFont.render(str(len(bodies)) + " Bodies", True, white), (3 + statusReportBox[0], 3 + 0*statusTextHeight + statusReportBox[1]))
    screen.blit(statusReportFont.render(str(bodyCount[0]) + " Stars", True, white), (3 + statusReportBox[0], 3 + 1*statusTextHeight + statusReportBox[1]))
    screen.blit(statusReportFont.render(str(bodyCount[1]) + " Planets", True, white), (3 + statusReportBox[0], 3 + 2*statusTextHeight + statusReportBox[1]))
    screen.blit(statusReportFont.render(str(bodyCount[2]) + " Black Holes", True, white), (3 + statusReportBox[0], 3 + 3*statusTextHeight + statusReportBox[1]))

while 1:

    bodies, leftMouse, rightMouse, leftBody, rightBody, startPlanet, bodyCount, speed, gravity, size \
    = allTheClickStuff(bodies, leftMouse, rightMouse, leftBody, rightBody, startPlanet, bodyCount, speed, baseSpeed, leftButton, rightButton, gravity, size)

    if speed > 0:
        bodies, bodyCount = moveBodies(bodies, bodyCount, speed, radii, goldilocksZone)

    drawBodies(screen, bodies)

    statusReport(statusReportBox)

    pygame.display.flip() # This updates the gui (does not flip)

    clock.tick(60) # Caps framerate at 60 fps