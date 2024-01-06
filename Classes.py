import pygame

HEIGHT = 720
WIDTH = 1280
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Classes

# Acts as a reusable way to make selections in a menu.
class Selection():
    selected = 0

    def __init__(self, myUpper, myLower):
        self.selected = 1
        self.upperLimit = myUpper
        self.lowerLimit = myLower

    # Changes the 'selected' value by increments. Increments must be 1 or -1
    def changeSelected(self, increment):
        if increment == 1:
            # Make sure that the selected is not about to go above the upper limit
            if self.selected < self.upperLimit:
                self.selected += increment

        elif increment == -1:                
            # Make sure that the selected is not about to go below the lower limit
            if self.selected > self.lowerLimit:
                self.selected += increment
        
        else:
            print("ERROR - INVALID INCREMENT")
    
    # Returns the value of 'selected'
    def getSelected(self):
        return self.selected
    
    # Sets a new value for 'selected'
    def setSelected(self, mySelected):
        self.selected = mySelected

# The class that dictates all of the players' actions in battle
class Player():
    maxhealth = 0
    health = 0
    lives = 0
    atkcooldown = 0
    xPos = 0
    yPos = 0
    velY = 0
    velX = 0
    isJumping = False
    rect = None
    atk1 = None
    atk2 = None
    atk3 = None
    atk4 = None
    GRAVITY = 0
    SPEED = 0
    GROUND = 0

    def __init__(self, setXPos): 
        # Set beginning values
        self.maxHealth = 100
        self.health = self.maxHealth
        self.atkcooldown = 0            # Cool for attacks, every 60 = 1 second cooldown.
        self.knockDecay = 1.0
        self.dmgDecay = 1.0
        self.lives = 2
        self.velY = 0
        self.velX = 0
        self.GRAVITY = 2
        self.SPEED = 10        
        self.GROUND = 4*HEIGHT/5
        self.HEIGHT = 100
        self.WIDTH = 100
        # Variable beginning values
        self.rect = pygame.Rect(self.xPos, self.yPos, self.WIDTH, self.HEIGHT)  
        self.xPos = setXPos
        self.yPos = self.GROUND
        self.facing = 1

    # Loads character information
    def loadInfo(self, allInfo):
        # Splitting the loaded info into segments
        Gattacks = allInfo[0]
        Jattacks = allInfo[1]
        size = allInfo[2]
        maxHealth = allInfo[3]
        speed = allInfo[4]
        # Grounded attacks
        self.atk1 = Gattacks[0]
        self.atk2 = Gattacks[1]
        self.atk3 = Gattacks[2]
        self.atk4 = Gattacks[3]
        # Jumping attacks
        self.jatk1 = Jattacks[0]
        self.jatk2 = Jattacks[1]
        self.jatk3 = Jattacks[2]
        self.jatk4 = Jattacks[3]
        # Dimensions and other properties        
        self.maxHealth = maxHealth
        self.health = maxHealth
        self.WIDTH = size[0]
        self.HEIGHT = size[1]
        self.GROUND = 4*HEIGHT/5 - size[1]
        self.SPEED = speed
        self.yPos = self.GROUND

    # Gets the width of the player's character
    def getWidth(self):
        return self.WIDTH

    # Lets the player move and jump.
    def move(self, direction): 
        speed = self.SPEED  # The speed at which the player will move
        dy = self.GRAVITY   # The rate at which the velocity will decrease.

        # Horizontal movement
        if direction == "L":                    
                    self.velX = -speed

        elif direction == "R":
            if self.rect.right + speed < WIDTH:
                    self.velX = speed

        # Jumping
        elif direction == "J" and not self.isJumping:  # Begins jump loop
            self.isJumping = True
            self.velY = -40

        if direction not in ("L", "R") and not self.isJumping:   # Stop horizontal movement if not moving left or right abd
            self.velX = 0

        if self.isJumping:
            self.velY = self.velY + dy              # Change velocity based on dy
            if (self.yPos + self.velY) <= self.GROUND:              # Change y position based on velocity
                self.yPos = self.yPos + self.velY
            else:           # Break out of the jump loop
                self.isJumping = False
                self.velY = 0
                self.yPos = self.GROUND
        
        if self.rect.right + self.velX > WIDTH:      # If the next movement hits the wall, allow player to stick to the wall but move no further.
            self.xPos = WIDTH - self.rect.width
        elif self.rect.left + self.velX < 0:         # Same reasoning as previous two lines
            self.xPos = 0
        else:
            self.xPos += self.velX

        self.rect.update(self.xPos, self.yPos, self.WIDTH, self.HEIGHT)
        
    # Draws the player
    def draw(self, surface, colour):
        pygame.draw.rect(surface, colour, self.rect)

    # Returns the player's health
    def getHealth(self):
        return self.health, self.maxHealth

    # Sets the position of the player and ceases any velocity
    def resetPos(self, newX):
        self.xPos = newX
        self.yPos = self.GROUND
        self.velX = 0
        self.velY = 0

    # Resets the player's health
    def resetHealth(self):
        self.health = self.maxHealth
    
    # Resets the player's lives
    def resetLives(self):
        self.lives = 2

    # Returns the player's lives
    def getLives(self):
        return self.lives
    
    # Decrements the player's lives
    def loseLife(self):
        self.lives = self.lives - 1

    # Causes the player to take damage, as well as be knocked back.
    def takeHit(self, damage, knockback):
        if self.health - damage > 0:             # Ensure that health doesn't fall into negative values.
            self.health = self.health - damage*self.dmgDecay
        else:
            self.health = 0            

        # Forces the enemy to jump at a certain velocity to simulate a knockback.
        self.isJumping = True
        self.velX = knockback[0]*-self.facing*self.knockDecay   # facing knocks back in the correct direction. It must be negative as it it knocked BACK from where the other player is.
        self.velY = -knockback[1]*self.knockDecay
        self.knockDecay *= 0.9
        self.dmgDecay *= 0.7

    # Takes information about an attack and produces a hurtbox to damage the enemy player.
    def attack(self, attackInfo, target):

        hitRect = pygame.Rect(self.rect.centerx + attackInfo.offset[0]*self.facing, self.rect.centery + attackInfo.offset[1], attackInfo.size[0], attackInfo.size[1])

        if self.facing == -1:
            hitRect.x -= hitRect.width

        if hitRect.colliderect(target.rect):
            target.takeHit(attackInfo.damage, attackInfo.knockback)

        pygame.draw.rect(screen, "red", hitRect)

    # Takes inputs and allows for any appropriate reaction.
    def action(self, player, target):
        
        # Set the player's direction:
        if self.xPos < target.xPos:
            self.facing = 1
        else:
            self.facing = -1

        key = pygame.key.get_pressed()
        self.move(None)
        currentAtk = None

        if self.atkcooldown > 0:           #Acts as a timer for attacks to cool down, decrementing by 1 per frame. 
            self.atkcooldown -= 1

        if player == 1:
            if not self.isJumping:
                if self.knockDecay < 1.0:
                    self.knockDecay = 1.0
                    self.dmgDecay = 1.0
                
                # Movements
                if key[pygame.K_a]:
                    self.move("L")
                if key[pygame.K_d]:
                    self.move("R")
                if key[pygame.K_w]:
                    self.move("J")
                
                # Grounded Attacks
                if key[pygame.K_c] and self.atkcooldown == 0:
                    self.attack(self.atk1, target)
                    currentAtk = self.atk1

                if key[pygame.K_f] and self.atkcooldown == 0:
                    self.attack(self.atk2, target)
                    currentAtk = self.atk2

                if key[pygame.K_g] and self.atkcooldown == 0:
                    self.attack(self.atk3, target)
                    currentAtk = self.atk3

                if key[pygame.K_n] and self.atkcooldown == 0:
                    self.attack(self.atk4, target)
                    currentAtk = self.atk4

                # Airborne Attacks
            elif self.isJumping and self.atkcooldown == 0 and self.knockDecay == 1.0: # If the knockDecay is 1 then they're not being knocked back.
                if key[pygame.K_c]:
                    self.attack(self.jatk1, target)
                    currentAtk = self.jatk1

                if key[pygame.K_f]:
                    self.attack(self.jatk2, target)
                    currentAtk = self.jatk2
                
                if key[pygame.K_g]:
                    self.attack(self.jatk3, target)
                    currentAtk = self.jatk3

                if key[pygame.K_n]:
                    self.attack(self.jatk4, target)
                    currentAtk = self.jatk4
       
        elif player == 2:
            if not self.isJumping:
                if self.knockDecay < 1.0:
                    self.knockDecay = 1.0
                    self.dmgDecay = 1.0
                
                # Movements
                if key[pygame.K_LEFT]:
                    self.move("L")
                if key[pygame.K_RIGHT]:
                    self.move("R")
                if key[pygame.K_UP]:
                    self.move("J")
                
                # Grounded Attacks
                if key[pygame.K_k] and self.atkcooldown == 0:
                    self.attack(self.atk1, target)
                    currentAtk = self.atk1

                if key[pygame.K_o] and self.atkcooldown == 0:
                    self.attack(self.atk2, target)
                    currentAtk = self.atk2

                if key[pygame.K_p] and self.atkcooldown == 0:
                    self.attack(self.atk3, target)
                    currentAtk = self.atk3

                if key[pygame.K_LEFTBRACKET] and self.atkcooldown == 0:
                    self.attack(self.atk4, target)
                    currentAtk = self.atk4

                # Airborne attacks
            elif self.isJumping and self.atkcooldown == 0 and self.knockDecay == 1.0: # If the knockDecay is 1 then they're not being knocked back. 
                if key[pygame.K_k]:
                    self.attack(self.jatk1, target)
                    currentAtk = self.jatk1

                if key[pygame.K_o]:
                    self.attack(self.jatk2, target)
                    currentAtk = self.jatk2

                if key[pygame.K_p]:
                    self.attack(self.jatk3, target)
                    currentAtk = self.jatk3

                if key[pygame.K_LEFTBRACKET]:
                    self.attack(self.jatk4, target)
                    currentAtk = self.jatk4

        if currentAtk is not None:
            self.atkcooldown = currentAtk.cooldown
            if currentAtk.hasMove:
                self.velX = currentAtk.dVel[0] * self.facing
                self.velY = currentAtk.dVel[1]

# This is a class vaguely imitating a record, however since it does need to manipulate data it is encapsulated.
class Character():
    attacks = ()
    jAttacks = ()
    width = 0
    height = 0
    health = 0
    speed = 0

    def __init__(self, attacks, jAttacks, width, height, health, speed):
        self.attacks = attacks
        self.jAttacks = jAttacks
        self.width = width
        self.height = height
        self.health = health
        self.speed = speed

    def getInfo(self):
        size = (self.width, self.height)
        allInfo = (self.attacks), (self.jAttacks), size, self.health, self.speed
        return allInfo

# This is a class imitating record, therefore I'm not using encapsulation for it.
class Attack():
    damage = 0
    cooldown = 0
    knockback = ()  
    offset = ()     # Offset from the player's center position
    size = ()       # Dimensions of the rect generated
    hasMove = False # Dictates whether the attack will move the player
    dVel = ()       # New velocity added to the player

    def __init__(self, newDamage, newCooldown, newKnockback, newDVel, newOffset, newSize, newHasMove):
        self.damage = newDamage
        self.cooldown = newCooldown
        self.knockback = newKnockback
        self.offset = newOffset
        self.size = newSize
        self.hasMove = newHasMove
        self.dVel = newDVel
