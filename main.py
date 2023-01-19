
import pygame, sys
from pygame.locals import QUIT
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

GREEN = (50,255,0) #DEFINE ALL COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WIDTH = 480 #DIMENSIONS - PORTRAIT GAME
HEIGHT = 600
FPS = 60 #FRAMES PER SECOND- HIGH = HELPS MAKE CHARACTERS LOOK LIKE THEYRE MOVING SMOOTHLY
pygame.init() #INITIALISE PYGAME
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #CREATE SCREEN WITH CORRECT DIMENSIONS
pygame.display.set_caption("Shmup!") #PUT TEXT ON SCREEN
clock = pygame.time.Clock() #INSTALL USE OF CLOCK

font_name = pygame.font.match_font('arial') #choosing the font
def draw_text(surf, text, size, x, y):
  #surf - the surface we want the text drawn on
  #text - a string that we want to display
  #size = size of text 
  #x, y - the location
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE) # TRUE = analising font to make it more clean and curved, no blurry edges
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #INITIATING OBJECT
        self.image = pygame.transform.scale(player_img, (50, 38)) #HOW BIG CHARACTER/OBJECT IS 
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2 #MIDDLE OF SCREEN
        self.rect.bottom = HEIGHT - 10 #BOTTOM OF SCREEN, SO OBJECT WILL BE LOCATED AT BOTTOM MIDDLE OF SCREEN
        self.speedx = 0 #HOW FAST CHARACTER MOVES
        #improving collisions:
        pygame.draw.circle(self.image, RED, self.rect.center, self.radius) #THIS CODE DRAWS A RED CIRCLE ON TOP OF THE PLAYER TO ALLOW US TO ASSESS THE RADIUS IN WHCIH THE COLLISION IS GOING TO OCCUR
    def update(self):
        self.speedx = 0 #INITIATE TO ALWAYS SET SPEED TO 0
        keystate = pygame.key.get_pressed() #CHECKS EVERY KEY TO SEE IF IT WAS PRESSED OR NOT 
        if keystate[pygame.K_LEFT]: #UNLESS EITHER LEFT KEY IS PRESSED
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:#OR RIGHT KEY IS PRESSED
            self.speedx = 8
        self.rect.x += self.speedx #SETTING RECT TO MOVE AT SPECIFIED SPEED
        if self.rect.right > WIDTH: #IF GOES PAST EDGES OF SCREEN, STOPS
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
  
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #initilaise mob as an object
        self.image_orig = random.choice(meteor_images)#uses uploaded metoer image file of a random size picked from the lsit
        self.image_orig.set_colorkey(BLACK) # makes the rectangle around the object not be visible as it is black therefore transparent
        self.image = self.image_orig.copy() #keep cop of original image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100) #this makes the mobs go in different random directions down the screen, not straight down
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        #sprite animation:
        self.rot = 0 # ROT = ROTATION
        self.rot_speed = random.randrange(-8,8) # ROT_SPEED = HOW MANY DEGREES IT SHOULD CHANGE BY EVERYTIME
        self.last_update = pygame.time.get_ticks()
      #IMPROVING COLLISIONS:
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2) #THIS LINE SETS THE SCALE OF THE CIRCLE TO BE 85% THE SIZE OF THE METOER SO IT DOESNT FULLY COVER IT AS THE METEORS ARENT PERFECT CIRCLES
        #self.radius = int(self.rect.width / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
      #this draws a red circle on top of the meteor so we can see how it looks, and the radius where the collision will occur
        pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

    def rotate(self):
        now = pygame.time.get_ticks() #how long it has been since the game began, so if it is time to rotate yet
        if now - self.last_update > 50: #if the milliseconds since start are > 50
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360 #remainder operator
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center #we record the location of the rect’s center
            self.image = new_image 
            self.rect = self.image.get_rect() #calculate new rect
            self.rect.center = old_center #set its center to saved (old) one

      
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width) #this if statement makes the Mob respawn if it goes off screen either at the bottom or diagonally
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y): # tells bullet where to appear
        pygame.sprite.Sprite.__init__(self) #initialise bullet
        self.image = pygame.transform.scale(bullet_img, (10, 20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() # initilaise rect around bullet
        self.rect.bottom = y #bottom of screen
        self.rect.centerx = x # bottom centre 
        self.speedy = -10 # negative y value = bullet goes upwards

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0: 
            self.kill() #if it moved off of the top  of the screen kill it

background = pygame.image.load(path.join(img_dir, "starfield.png")).convert() #use uploaded image file as background (staryr night sky in space)
background_rect = background.get_rect()#make background a rectangle
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert() #use uploaded image file as the player (spaceship shooting bullets)
meteor_images = [] #list of diff sized meteors
meteor_list =['meteorBrown_big1.png','meteorBrown_med1.png',
              'meteorBrown_med1.png','meteorBrown_med3.png',
              'meteorBrown_small1.png','meteorBrown_small2.png',
              'meteorBrown_tiny1.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
  
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert() #use uploaded image file of bullets to shoot from the ship towards the meteors 
      
all_sprites = pygame.sprite.Group() #COLLECTION OF ALL SPRITES DRAWN
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player() #INTIALISE PLAYER AS AN OBJECT
all_sprites.add(player) #ADDING PLAYER TO THE GROUP SO IT SPAWNS ON THE SCREEN
for i in range(8): # creates a group of mobs to all spawn on the screen
    m = Mob()
    all_sprites.add(m) # add the mobs to the group
    mobs.add(m)

for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
score = 0 #initializing the score variable
  
#GAME LOOP:      
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS) #MAKE CLOCK TICK AT SPECIFIED FRAMES PER SECOND
    for event in pygame.event.get():# Process input (events)
        if event.type == pygame.QUIT: # CHECK IF WINDOW IS BEING CLOSED
            running = False #IF YES, STOP RUNNING GAME LOOP
        elif event.type == pygame.KEYDOWN: # check if a key has been pressed
            if event.key == pygame.K_SPACE: # if so, was it the space key?
                player.shoot() # if yes, then fire the bullet
          
    all_sprites.update()
  
    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True) # 1st parameter: 1st group 2nd parameter: 2nd group, these groups will collide together and the last 2 parameters decide whether or not the objects in each group are deleted. In this case, both the mobs and the bullets that are hit will be deleted ( dokill is true in both cases)
    for hit in hits: #however, if the mobs keep being deleted everytime they are hit, there is a risk of running out, therefore this loop is added in so that everytime the mobs are deleed, more are created
        score += 50 - hit.radius #depending on how small or big the meteors are, determines how many points they're worth. The smallest ones are worth the most as they are roughly 50-8 = 42 points, whereas with the bigger radius, it is more like 50 - 40 = only worth 10 points.
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    
    #check to see if a mob hit the player:
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)#1st parameter: name of sprite you want to kill, 2nd parameter: name of group you want to kill and 3rd parameter 'dokill' which  lets you set whether the object should be deleted when it gets hit, so for this we do not want the player to just disappear if it gets hit #IMRPOVING COLLISIONS - ADDED IN A FOURTH PARAMETER TO HAVE THE GAME USE THE CIRCLES FOR THE COLLISIONS, RATHER THAN THE ACTUAL SPRITE
    if hits:
        running = False # if a mob has hit the player, stop running

    screen.fill(BLACK) # black screen
    screen.blit(background, background_rect) # makes background the image file uploaded
    all_sprites.draw(screen) #DRAW SCREEN
    draw_text(screen, str(score), 18, WIDTH / 2, 10) #this shows the score at the top of the screen, in the middle
    pygame.display.flip() # *after* drawing everything, flip the display


pygame.quit()