import pygame
# Import the classes, see Classes.py for more info.
from Classes import Selection, Player, Character, Attack

# SUBROUTINES:

# Miscellaneous:

# Draws a list of rects of matching colour.
def drawGroup(rects, colour):
    for rect in rects:
        pygame.draw.rect(screen, colour, rect)

# Resets player states.
def setStates():
    Player1.resetPos(WIDTH/2 - 300)
    Player2.resetPos(WIDTH/2 + 300 - Player2.getWidth())
    Player1.resetHealth()
    Player2.resetHealth()

# Visuals:

# MAIN MENU
def mainMenu(events):
    toReturn = 0     #The value that the mainMenu subroutine will return
    selected = MainMenu.getSelected()

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                MainMenu.changeSelected(-1)
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                MainMenu.changeSelected(1)
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                toReturn = selected

    # Anchor X and Y positions for the buttons
    BUTTONY = HEIGHT*(2/3)
    BUTTONX = WIDTH/4 - 50

    # fill the screen with black to wipe away anything from last frame
    screen.fill("black")

    # Button Highlighter Rect:
    highlighted = pygame.Rect(BUTTONX-210 + 200*selected, BUTTONY-10, 120, 120)

    # Each Button Rect:
    playButton = pygame.Rect(BUTTONX, BUTTONY , 100, 100)
    trainButton = pygame.Rect(BUTTONX + 200, BUTTONY, 100, 100)
    infoButton = pygame.Rect(BUTTONX + 400, BUTTONY, 100, 100)
    quitButton = pygame.Rect(BUTTONX + 600, BUTTONY, 100, 100)

    # Drawing each button:
    pygame.draw.rect(screen, "Blue", highlighted) #Draws highlighted first to draw other buttons on top of it.
    
    pygame.draw.rect(screen, "White", playButton)
    pygame.draw.rect(screen, "White", trainButton)
    pygame.draw.rect(screen, "White", infoButton)
    pygame.draw.rect(screen, "White", quitButton)

    # Loading and drawing the title image:
    title = pygame.image.load("./Assets/Screens/TitleScreen/TusslTim.png")
    title = pygame.transform.scale(title, (640, 360))
    screen.blit(title, (WIDTH/2 - 320, HEIGHT/6))

    # Loading the button images:
    playButtonImg = pygame.image.load("./Assets/Screens/TitleScreen/playButton.png")
    playButtonImg = pygame.transform.scale(playButtonImg, (100, 100))
    trainButtonImg = pygame.image.load("./Assets/Screens/TitleScreen/imgButton.png")
    trainButtonImg = pygame.transform.scale(trainButtonImg, (100, 100))
    infoButtonImg = pygame.image.load("./Assets/Screens/TitleScreen/infoButton.png")
    infoButtonImg = pygame.transform.scale(infoButtonImg, (100, 100))
    quitButtonImg = pygame.image.load("./Assets/Screens/TitleScreen/quitButton.png")
    quitButtonImg = pygame.transform.scale(quitButtonImg, (100,100))

    # Drawing the button images:
    screen.blit(playButtonImg, (BUTTONX, BUTTONY))
    screen.blit(trainButtonImg, (BUTTONX + 200, BUTTONY))
    screen.blit(infoButtonImg, (BUTTONX + 400, BUTTONY))
    screen.blit(quitButtonImg, (BUTTONX + 600, BUTTONY))

    # Returns the option that the player has selected (if not selected, then returns 0)
    return toReturn

# CHARACTER SELECT 
def charSelect(events, p1ready, p2ready, mode):
    # Initialising variables
    toReturn = 0
    p1Selected = SelectPlayer1.getSelected()
    p2Selected = SelectPlayer2.getSelected()
    BUTTONX = WIDTH/2 - 75
    BUTTONY = (1/10)*HEIGHT

    #Fill the screen with black to wipe away everything from the last frame
    screen.fill("Black")

    for event in events:
        if event.type == pygame.KEYDOWN:            
            
            if mode == "play":                                   #ALL 'PLAYER 2' INPUTS, MUST COME BEFORE PLAYER 1 FOR PRACTICE MODE SEQUENCING TO WORK
                # Player 2 buttons:
                if event.key == pygame.K_RETURN:
                    p2ready = True
                if event.key == pygame.K_BACKSPACE and p2ready:     
                    p2ready = False
                if event.key == pygame.K_UP and not p2ready:
                    SelectPlayer2.changeSelected(-1)
                if event.key == pygame.K_DOWN and not p2ready:
                    SelectPlayer2.changeSelected(1)
            
            elif mode == "practice" and p1ready:                                                    # The mode is practice, so player 1 selects the character for player 2
                if event.key == pygame.K_SPACE:                  # P2 readies 
                    p2ready = True
                if event.key == pygame.K_ESCAPE and p2ready:     # P2 unreadies
                    p2ready = False
                if event.key == pygame.K_w and not p2ready:
                    SelectPlayer2.changeSelected(-1)
                if event.key == pygame.K_s and not p2ready:
                    SelectPlayer2.changeSelected(1)

            # Player 1 buttons:            
            if event.key == pygame.K_ESCAPE and not p1ready:     # Returns the players to the main menu.
                toReturn = 2
            if event.key == pygame.K_SPACE:                  # P1 readies 
                p1ready = True
            if event.key == pygame.K_ESCAPE and p1ready:     # P1 unreadies
                p1ready = False
            if event.key == pygame.K_w and not p1ready:
                SelectPlayer1.changeSelected(-1)
            if event.key == pygame.K_s and not p1ready:
                SelectPlayer1.changeSelected(1)
            

                
            

    # Highlight Rects:
    highlight1 = pygame.Rect(BUTTONX - 5, BUTTONY + (p1Selected-1)*HEIGHT/4 - 5, 80, 160)
    highlight2 = pygame.Rect(BUTTONX + 75, BUTTONY + (p2Selected-1)*HEIGHT/4 - 5, 80, 160)

    # Button Rects:
    button1 = pygame.Rect(BUTTONX, BUTTONY, 150, 150)
    button2 = pygame.Rect(BUTTONX, BUTTONY + HEIGHT/4, 150, 150)
    button3 = pygame.Rect(BUTTONX, BUTTONY + 2*HEIGHT/4, 150, 150)

    # Background Rects for player sprites:
    back1 = pygame.Rect(BUTTONX - 400, HEIGHT/10, 300, 500)
    back2 = pygame.Rect(BUTTONX + 250, HEIGHT/10, 300, 500)

    # Loading Images
    placeholder1 = pygame.image.load("./Assets/PlaceHolders/PlaceHolder1.png")
    placeholder2 = pygame.image.load("./Assets/PlaceHolders/PlaceHolder2.png")
    placeholder3 = pygame.image.load("./Assets/PlaceHolders/PlaceHolder3.png")
    readyImg = pygame.image.load("./Assets/Screens/CharacterScreen/Ready.png")

    # Drawing all Images and Rects:
    pygame.draw.rect(screen, "Red", highlight1)
    pygame.draw.rect(screen, "Blue", highlight2)
    
    whiteRects = (button1, button2, button3, back1, back2)
    drawGroup(whiteRects, "White")

    screen.blit(placeholder1, (BUTTONX, BUTTONY))
    screen.blit(placeholder2, (BUTTONX, BUTTONY + HEIGHT/4))
    screen.blit(placeholder3, (BUTTONX, BUTTONY + 2*HEIGHT/4))
    
    # Displays character ready signs depending on the readied player.
    if p1ready:
        screen.blit(readyImg, (BUTTONX - 400, 8*HEIGHT/10))

    if p2ready:
        screen.blit(readyImg, (BUTTONX + 250, 8*HEIGHT/10))

    # Displays a character in the appropriate character box based on the currently selected character.
    if p1Selected == 1:
        screen.blit(placeholder1, (BUTTONX - 400, HEIGHT/10))   
    elif p1Selected == 2:
        screen.blit(placeholder2, (BUTTONX - 400, HEIGHT/10))
    else:
        screen.blit(placeholder3, (BUTTONX - 400, HEIGHT/10))
    
    if p2Selected == 1:
        screen.blit(placeholder1, (BUTTONX + 250, HEIGHT/10))
    elif p2Selected == 2:
        screen.blit(placeholder2, (BUTTONX + 250, HEIGHT/10))
    else:
        screen.blit(placeholder3, (BUTTONX + 250, HEIGHT/10))

    # Setting up the value toReturn if both players have selected
    if p1ready and p2ready:
        toReturn = 1

    return p1ready, p2ready, toReturn

# INFO SCREEN
def charInfo(events, level):
    # Logic Variables
    toReturn = 0
    charSelected = CharInfoLvl1.getSelected()
    attackSelected = CharInfoLvl2.getSelected()

    # GUI Positioning Constants
    CHARBUTX = WIDTH/36
    CHARBUTY = HEIGHT/20
    CHARBUTWIDTH = 5*WIDTH/36
    CHARBUTHEIGHT = 5*HEIGHT/20
    ATKBUTX = 7*WIDTH/36
    ATKBUTY = HEIGHT/20
    ATKBUTWIDTH = 5*WIDTH/36
    ATKBUTHEIGHT = 3*HEIGHT/20
    TEXTBOXX = 14*WIDTH/36
    TEXTBOXY = HEIGHT/20
    TEXTBOXWIDTH = WIDTH/2
    TEXTBOXHEIGHT = 9*HEIGHT/10

    for event in events:
        if event.type == pygame.KEYDOWN:
                # Player 1 buttons:
            if level == 1:          
                if event.key == pygame.K_ESCAPE:              # Exit the character info screen
                    toReturn = 1
                if event.key == pygame.K_SPACE:               # Move to the attack list
                    level = 2
                if event.key == pygame.K_w and not p1ready:
                    CharInfoLvl1.changeSelected(-1)
                if event.key == pygame.K_s and not p1ready:
                    CharInfoLvl1.changeSelected(1)
            else:
                if event.key == pygame.K_ESCAPE:              # Return to the character list
                    level = 1
                    CharInfoLvl2.setSelected(1)
                if event.key == pygame.K_w and not p1ready:
                    CharInfoLvl2.changeSelected(-1)
                if event.key == pygame.K_s and not p1ready:
                    CharInfoLvl2.changeSelected(1)

    # Display
    
    # Fill the screen with black to wipe away everything from the last frame
    screen.fill("Black")
    
    # Create all Rects:
    
    # Highlights:
    charHigh = pygame.Rect(CHARBUTX - 5, CHARBUTY + (3*(charSelected-1))*HEIGHT/10 - 5, CHARBUTWIDTH + 10, CHARBUTHEIGHT + 10)
    atkHigh = pygame.Rect(ATKBUTX - 5, ATKBUTY + (attackSelected-1)*HEIGHT/5 - 5, ATKBUTWIDTH + 10, ATKBUTHEIGHT + 10)

    # Char Buttons:
    charBut1 = pygame.Rect(CHARBUTX, CHARBUTY, CHARBUTWIDTH, CHARBUTHEIGHT)
    charBut2 = pygame.Rect(CHARBUTX, CHARBUTY + 3*HEIGHT/10, CHARBUTWIDTH, CHARBUTHEIGHT)
    charBut3 = pygame.Rect(CHARBUTX, CHARBUTY + 3*HEIGHT/5, CHARBUTWIDTH, CHARBUTHEIGHT)

    # Attack Buttons:
    atkBut1 = pygame.Rect(ATKBUTX, ATKBUTY, ATKBUTWIDTH, ATKBUTHEIGHT)
    atkBut2 = pygame.Rect(ATKBUTX, ATKBUTY + HEIGHT/5, ATKBUTWIDTH, ATKBUTHEIGHT)
    atkBut3 = pygame.Rect(ATKBUTX, ATKBUTY + 2*HEIGHT/5, ATKBUTWIDTH, ATKBUTHEIGHT)
    atkBut4 = pygame.Rect(ATKBUTX, ATKBUTY + 3*HEIGHT/5, ATKBUTWIDTH, ATKBUTHEIGHT)

    # Text Box:
    textBox = pygame.Rect(TEXTBOXX, TEXTBOXY, TEXTBOXWIDTH, TEXTBOXHEIGHT)

    # Placeholders:
    placeholder1 = pygame.image.load("./Assets/PlaceHolders/PlaceHolder1.png")
    placeholder2 = pygame.image.load("./Assets/PlaceHolders/PlaceHolder2.png")
    placeholder3 = pygame.image.load("./Assets/PlaceHolders/PlaceHolder3.png")
    placeholder4 = pygame.image.load("./Assets/PlaceHolders/PlaceHolder4.png")
    placeholder4 = pygame.transform.scale(placeholder4, (100, 100))

    # Draw the highlighter rects
    pygame.draw.rect(screen, "blue", charHigh)
    if level != 1:
        pygame.draw.rect(screen, "blue", atkHigh)

    allRects = (charBut1, charBut2, charBut3, atkBut1, atkBut2, atkBut3, atkBut4, textBox) #Draws all the static white rects  
    for rect in allRects:
        pygame.draw.rect(screen, "white", rect)
    
    # Draw Images
    screen.blit(placeholder1, (CHARBUTX, CHARBUTY))
    screen.blit(placeholder2, (CHARBUTX, CHARBUTY + 3*HEIGHT/10))
    screen.blit(placeholder3, (CHARBUTX, CHARBUTY + 3*HEIGHT/5))
    
    screen.blit(placeholder1, (ATKBUTX, ATKBUTY))
    screen.blit(placeholder2, (ATKBUTX, ATKBUTY + HEIGHT/5))
    screen.blit(placeholder3, (ATKBUTX, ATKBUTY + 2*HEIGHT/5))
    screen.blit(placeholder4, (ATKBUTX, ATKBUTY + 3*HEIGHT/5))

    # Display in text box depending on charSelect and attackSelect
    if charSelected == 1:
        screen.blit(placeholder1, (TEXTBOXX, TEXTBOXY))
        if attackSelected == 1:
            screen.blit(placeholder1, (TEXTBOXX + 200, TEXTBOXY))
        elif attackSelected == 2:
            screen.blit(placeholder2, (TEXTBOXX + 200, TEXTBOXY))
        elif attackSelected == 3:
            screen.blit(placeholder3, (TEXTBOXX + 200, TEXTBOXY))
        elif attackSelected == 4:
            screen.blit(placeholder4, (TEXTBOXX + 200, TEXTBOXY))
    
    elif charSelected == 2:
        screen.blit(placeholder2, (TEXTBOXX, TEXTBOXY))
        if attackSelected == 1:
            screen.blit(placeholder1, (TEXTBOXX + 200, TEXTBOXY))
        elif attackSelected == 2:
            screen.blit(placeholder2, (TEXTBOXX + 200, TEXTBOXY))
        elif attackSelected == 3:
            screen.blit(placeholder3, (TEXTBOXX + 200, TEXTBOXY))
        elif attackSelected == 4:
            screen.blit(placeholder4, (TEXTBOXX + 200, TEXTBOXY))

    else:
        screen.blit(placeholder3, (TEXTBOXX, TEXTBOXY))
        if attackSelected == 1:
            screen.blit(placeholder1, (TEXTBOXX + 200, TEXTBOXY))
        elif attackSelected == 2:
            screen.blit(placeholder2, (TEXTBOXX + 200, TEXTBOXY))
        elif attackSelected == 3:
            screen.blit(placeholder3, (TEXTBOXX + 200, TEXTBOXY))
        elif attackSelected == 4:
            screen.blit(placeholder4, (TEXTBOXX + 200, TEXTBOXY))

    return toReturn, level 

# BATTLE SCREEN
def battleScreen(events, surface):    
    
    #Preparing variables
    toReturn = 0
    healths1 = Player1.getHealth()
    healths2 = Player2.getHealth()
    health1 = healths1[0]
    health2 = healths2[0]
    maxHealth1 = healths1[1]
    maxHealth2 = healths2[1]
    lives1 = Player1.getLives()
    lives2 = Player2.getLives()

    # Allow player to return to main menu.
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                # Allows only a single player to interact with the pause tile.
                if event.key == pygame.K_ESCAPE: 
                    option = pauseTile(1)  # Player 1
                else:
                    option = pauseTile(2)  # Player 2
                toReturn = option - 1

    if health1 == 0:
        Player1.loseLife()
        if Player1.getLives() != 0:
            setStates()
        else:
            winSequence(2)
            toReturn = 2

    elif health2 == 0:
        Player2.loseLife()
        if Player2.getLives() != 0:
            setStates()
        else:
            winSequence(1)
            toReturn = 2
    
    ratio1 = health1/maxHealth1
    ratio2 = health2/maxHealth2

    # Background:
    surface.fill("black")
    groundRect = pygame.Rect(0, 4*HEIGHT/5, WIDTH, 6*HEIGHT/7)
    pygame.draw.rect(surface, "White", groundRect)

    # Player actions:
    Player1.action(1, Player2)
    Player2.action(2, Player1)
    Player1.draw(surface, "green")
    Player2.draw(surface, "blue")

    # UI:

    # Loading Images:

    fullLife = pygame.image.load("./Assets/Screens/BattleScreen/FullLife.png")
    voidLife = pygame.image.load("./Assets/Screens/BattleScreen/VoidLife.png")
    fullLife = pygame.transform.scale(fullLife, (WIDTH/36, WIDTH/36))
    voidLife = pygame.transform.scale(voidLife, (WIDTH/36, WIDTH/36))

    # Health bars:
    backbar1 = pygame.Rect(WIDTH/12, HEIGHT/36, WIDTH/4, HEIGHT/36)
    backbar2 = pygame.Rect(2*WIDTH/3, HEIGHT/36, WIDTH/4, HEIGHT/36)
    healthbar1 = pygame.Rect(WIDTH/12, HEIGHT/36, WIDTH/4*ratio1, HEIGHT/36)
    healthbar2 = pygame.Rect(2*WIDTH/3, HEIGHT/36, WIDTH/4*ratio2, HEIGHT/36)
    drawGroup((backbar1, backbar2), "red")
    drawGroup((healthbar1, healthbar2), "yellow")

    # Life counter:

    if lives1 == 2:
        screen.blit(fullLife, (WIDTH/12, HEIGHT/18))
        screen.blit(fullLife, (WIDTH/9, HEIGHT/18))
    elif lives1 == 1:
        screen.blit(fullLife, (WIDTH/12, HEIGHT/18))
        screen.blit(voidLife, (WIDTH/9, HEIGHT/18))
    else:
        screen.blit(voidLife, (WIDTH/12, HEIGHT/18))
        screen.blit(voidLife, (WIDTH/9, HEIGHT/18))
    
    if lives2 == 2:
        screen.blit(fullLife, (31*WIDTH/36, HEIGHT/18))
        screen.blit(fullLife, (8*WIDTH/9, HEIGHT/18))
    elif lives2 == 1:
        screen.blit(voidLife, (31*WIDTH/36, HEIGHT/18))
        screen.blit(fullLife, (8*WIDTH/9, HEIGHT/18))
    else:
        screen.blit(voidLife, (31*WIDTH/36, HEIGHT/18))
        screen.blit(voidLife, (8*WIDTH/9, HEIGHT/18))
    
    return toReturn

# Win Sequence
def winSequence(winner):
    time = pygame.time.get_ticks()
    # Waits for 2 seconds to pass (each second is 1000 milliseconds)
    while pygame.time.get_ticks() - time < 2000:
        # Loads a win image depending on the winner (winner = 1 if player 1 won, 2 for player 2)
        if winner == 1:
            winImg = pygame.image.load("./Assets/Screens/BattleScreen/Victory1.png")
        else:
            winImg = pygame.image.load("./Assets/Screens/BattleScreen/Victory2.png")

        # Displays win image
        screen.blit(winImg, (WIDTH/2 - winImg.get_width()/2, HEIGHT/18))
        pygame.display.flip()

# Pause Tile
def pauseTile(player):
    runPause = True
    pauseSelect = Selection(4, 1) # Selection object for 4 options
    pauseImg = pygame.image.load("./Assets/Screens/BattleScreen/PauseTile.png")
    pauseImg = pygame.transform.scale(pauseImg, (WIDTH/3, WIDTH/3))
    pauseWidth = pauseImg.get_width()

    while runPause:
        events = pygame.event.get()
        clock.tick(60)
        screen.blit(pauseImg, (WIDTH/2 - pauseWidth/2, HEIGHT/18))
        selected = pauseSelect.getSelected() 

        highlighted = pygame.Rect(WIDTH/2 - pauseWidth/2+pauseWidth/16, HEIGHT/18 + pauseWidth/10 + (selected-1)*pauseWidth*9/40, pauseWidth/8, pauseWidth/8)
        pygame.draw.rect(screen, "green", highlighted)

        for event in events:
            if event.type == pygame.KEYDOWN: 
                if player == 1:
                    if event.key == pygame.K_w:
                        pauseSelect.changeSelected(-1)
                    elif event.key == pygame.K_s:
                        pauseSelect.changeSelected(1)
                    elif event.key == pygame.K_SPACE:
                        runPause = False

                elif player == 2:
                    if event.key == pygame.K_UP:
                        pauseSelect.changeSelected(-1)
                    elif event.key == pygame.K_DOWN:
                        pauseSelect.changeSelected(1)
                    elif event.key == pygame.K_RETURN:
                        runPause = False
        
        pygame.display.flip()
    
    return selected

# Main Program
HEIGHT = 720
WIDTH = 1280

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Initialising variables:
running = True

# Starts the game at the main menu.
runMainMenu = True

# Initialises the rest of the states the game can be in:
runCharInfo = False
runCharSelect = False
runBattle = False

# CharSelect ready states:
p1ready = False
p2ready = False

# Instantiating objects:
MainMenu = Selection(4, 1) 
SelectPlayer1 = Selection(3, 1)
SelectPlayer2 = Selection(3, 1)
CharInfoLvl1 = Selection(3, 1)
CharInfoLvl2 = Selection(4, 1)
Player1 = Player(500)
Player2 = Player(800)

# Character Records:

# ALL ATTACKS TAKE THE FORMAT (DAMAGE, COOLDOWN, KNOCKBACK, VELOCITY, OFFSET, DIMENSIONS, MOVING)

# Ground Attacks:
char1Gatk1 = Attack(25, 10, (20, 30), (0, 0), (0, -75), (120, 150), False)
char1Gatk2 = Attack(15, 30, (10, 40), (0, 0), (0, 20), (150, 30), False)
char1Gatk3 = Attack(45, 30, (30, 20), (0, 0), (0, -100), (200, 200), False)
char1Gatk4 = Attack(15, 10, (-30, 30), (0, 0), (300, -100), (100, 200), False)
char1Gatks = (char1Gatk1, char1Gatk2, char1Gatk3, char1Gatk4)

char2Gatk1 = Attack(20, 20, (30, 30), (0, 0), (0, -100), (120, 200), False)
char2Gatk2 = Attack(10, 30, (10, 50), (0, 0), (0, 0), (200, 100), False)
char2Gatk3 = Attack(30, 70, (30, 40), (0, 0), (0, -75), (250, 150), False)
char2Gatk4 = Attack(50, 100, (20, 30), (0, 0), (-175, -200), (350, 300), False)
char2Gatks = (char2Gatk1, char2Gatk2, char2Gatk3, char2Gatk4)

char3Gatk1 = Attack(10, 40, (30, 20), (0, 0), (0, -150), (150, 300), False)
char3Gatk2 = Attack(15, 50, (10, 40), (0, 0), (0, -50), (250, 200), False)
char3Gatk3 = Attack(30, 120, (40, 50), (0, 0), (0, -150), (200, 300), False)
char3Gatk4 = Attack(5, 60, (0, 100), (0, 0), (0, 140), (500, 10), False)
char3Gatks = (char3Gatk1, char3Gatk2, char3Gatk3, char3Gatk4)

# Jumping Attacks:
char1Jatk1 = Attack(15, 10, (5, 4), (0, 0), (50, -40), (60, 75), False)
char1Jatk2 = Attack(15, 30, (5, 30), (0, 0), (0, 100), (100, 200), False)
char1Jatk3 = Attack(45, 30, (30, 20), (0, 0), (0, -100), (200, 200), False)
char1Jatk4 = Attack(15, 10, (-5, 40), (0, 0), (20, 200), (100, 200), False)
char1Jatks = (char1Jatk1, char1Jatk2, char1Jatk3, char1Jatk4)

char2Jatk1 = Attack(20, 20, (30, 30), (0, 0), (0, -100), (120, 200), False)
char2Jatk2 = Attack(10, 30, (10, 50), (0, 0), (0, 0), (200, 100), False)
char2Jatk3 = Attack(30, 70, (30, 40), (0, 0), (0, -75), (250, 150), False)
char2Jatk4 = Attack(50, 100, (20, 30), (0, 0), (-175, -200), (350, 300), False)
char2Jatks = (char2Jatk1, char2Jatk2, char2Jatk3, char2Jatk4)

char3Jatk1 = Attack(10, 40, (30, 20), (0, 0), (0, -150), (150, 300), False)
char3Jatk2 = Attack(15, 50, (10, 40), (0, 0), (0, -50), (250, 200), False)
char3Jatk3 = Attack(30, 120, (40, 50), (0, 0), (0, -150), (200, 300), False)
char3Jatk4 = Attack(5, 60, (0, 100), (0, 0), (0, 140), (500, 10), False)
char3Jatks = (char3Jatk1, char3Jatk2, char3Jatk3, char3Jatk4)

# ALL CHARACTERS TAKE THE FORMAT (GROUND ATTACKS, AIR ATTACKS, WIDTH, HEIGHT, HEALTH, SPEED)
char1 = Character(char1Gatks, char1Jatks, 100, 150, 100, 20)
char2 = Character(char2Gatks, char2Jatks, 150, 200, 200, 10)
char3 = Character(char3Gatks, char3Jatks, 200, 300, 300, 5)

# Main code

while running:    
    clock.tick(60)  # Limits FPS to 60

    events = pygame.event.get()
    # Quits game if user clicks the x button.
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Menu Screen
    if runMainMenu:
        option = mainMenu(events)
        #Directing to the next screen when the main menu is exited:
        if option != 0:
            runMainMenu = False
            MainMenu.setSelected(1) # Reset selected to its original state (1) for reuse.
            if option == 1:
                runCharSelect = True
                mode = "play"
            elif option == 2:
                runCharSelect = True
                mode = "practice"
            elif option == 3:
                runCharInfo = True
                level = 1
            else:
                running = False

    # Character Select Screen     
    elif runCharSelect:
        options = charSelect(events, p1ready, p2ready, mode)
        p1ready = options[0]
        p2ready = options[1]
        result = options[2]
        if result != 0:
            runCharSelect = False

            if result == 1:                                # Result being '1' begins to prepare the battle scene.
                runBattle = True
                p1ready = False
                p2ready = False
                p1char = SelectPlayer1.getSelected()
                p2char = SelectPlayer2.getSelected()

                # Sets the players' lives in case they've run the battle sequence before now.
                Player1.resetLives()
                Player2.resetLives()
                
                # Loads certain characters based on the players' selections.
                if p1char == 1:
                    Player1.loadInfo(char1.getInfo())  # GetInfo returns a list, so it has to be broken down via this indexing.
                elif p1char == 2:
                    Player1.loadInfo(char2.getInfo())
                else:
                    Player1.loadInfo(char3.getInfo())


                if p2char == 1:
                    Player2.loadInfo(char1.getInfo())
                elif p2char == 2:
                    Player2.loadInfo(char2.getInfo())
                else:
                    Player2.loadInfo(char3.getInfo())
                
                # Sets characters to the correct position:
                Player1.resetPos(WIDTH/2 - 300)
                Player2.resetPos(WIDTH/2 + 300 - Player2.getWidth())

            elif result == 2:                                # Result being '2' returns the player to the main menu.
                runMainMenu = True 
            
            # Reset all values to their original states for reuse. This has to happen after the other conditions in order to not interfere with preparing the next screen.
            SelectPlayer1.setSelected(1)
            SelectPlayer2.setSelected(1)
            p1Ready = False
            p2Ready = False

    # Character Info Screen
    elif runCharInfo:
        options = charInfo(events, level)
        result = options[0]
        level = options[1]
        if result == 1:
            runCharInfo = False
            CharInfoLvl1.setSelected(1)
            runMainMenu = True
    
    # Battle Screen
    elif runBattle:
        option = battleScreen(events, screen)

        # Exit battle screen when the player presses escape or someone wins (see battleScreen code)
        if option == 1:
            runCharSelect = True
            runBattle = False
        elif option == 2:
            runMainMenu = True
            runBattle = False
        elif option == 3:
            pygame.quit()

    pygame.display.flip()  # Updates Screen

pygame.quit()