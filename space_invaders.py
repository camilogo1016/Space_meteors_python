import pygame, random
# Sizes and dimentions
size_x = 1080
size_y = 720
size_player = 40
size_meteor = 40
laser_speed = 5
# Variables
white = (255,255,255)
black = (0,0,0)

## ------------------- Clases -------------------- ##
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("meteor.png").convert() #load image
        self.image = pygame.transform.scale(self.image, (size_meteor, size_meteor))  #resize
        self.image.set_colorkey(black) #Remove black background
        self.rect = self.image.get_rect() #obtain coordinates for the obect
    def update(self):
        self.rect.y += 1
        #when it reaches the bottom reset position
        if self.rect.y >= size_y:
            self.rect.y = -size_meteor/2
            self.rect.x = random.randrange(size_x-size_meteor)

class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("laser.png").convert() #load image
        #self.image = pygame.transform.scale(self.image, (size_player, size_player))  #resize
        self.image.set_colorkey(black) #Remove black background
        self.rect = self.image.get_rect() #obtain coordinates for the obect
    def update(self):
        self.rect.y -= laser_speed

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player1.png").convert() #load image
        self.image = pygame.transform.scale(self.image, (size_player, size_player))  #resize
        self.image.set_colorkey(black) #Remove black background
        self.rect = self.image.get_rect() #obtain coordinates for the obect
        self.speed_x = 0
        self.rect.x = size_x/2
    def changespeed(self, X):
        self.speed_x = X 
    def update(self):
        self.rect.x += self.speed_x
        # Get mouse position
        ##x, _ = pygame.mouse.get_pos()
        ##self.rect.x = x
        self.rect.y = size_y - 3*size_player/2

class Game(object):
    def __init__(self):
        self.game_over = False
        self.score = 0
        self.lives = 5
        # List for meteors and all elements
        self.meteor_list = pygame.sprite.Group() #a list for meteors
        self.all_sprite_list = pygame.sprite.Group() #a list for all sprites
        self.laser_list = pygame.sprite.Group()
        # Sound of the game
        self.sound = pygame.mixer.Sound("laser_sound.ogg")
        self.explos = pygame.mixer.Sound("explosion.wav")
        pygame.mixer.Sound.set_volume(self.explos, 0.05)#lower the level of the sound
        # Create Meteors and Player
        for _ in range(50):
            meteor = Meteor()
            meteor.rect.x = random.randrange(size_x-size_meteor)
            meteor.rect.y = random.randrange(size_y-size_meteor)
            self.meteor_list.add(meteor)
            self.all_sprite_list.add(meteor)
            # We initialize the class Player
        self.player = Player()
        self.all_sprite_list.add(self.player)
        
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # We create a laser when we click or press Space
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                # If the game was over
                if self.game_over:
                    self.__init__()
                self.laser = Laser()
                self.laser.rect.x = self.player.rect.x + (size_player/2)
                self.laser.rect.y = self.player.rect.y - size_player
                # We add the laser to the sprites list
                self.all_sprite_list.add(self.laser)
                self.laser_list.add(self.laser)
                # Sound of laser
                self.sound.play()
            # Using the keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.changespeed(-3)
                if event.key == pygame.K_RIGHT:
                    self.player.changespeed(3)
            # Stops the move
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.changespeed(0)
                if event.key == pygame.K_RIGHT:
                    self.player.changespeed(0)

    def run_logic(self):
        # If it's not game over
        if not self.game_over:
            # Update position of every element
            self.all_sprite_list.update()
            # Hit list
            self.meteor_hit_list = pygame.sprite.spritecollide(self.player,self.meteor_list, True)
            # We check every laser
            for lasser in self.laser_list:
                # If it leaves the screen, we delete it
                if lasser.rect.y < -10:
                    self.laser_list.remove(lasser)
                    self.all_sprite_list.remove(lasser)
                #We check if there's any collide
                self.meteor_hit_laser = pygame.sprite.spritecollide(lasser, self.meteor_list, True)
                # If there was a collide
                if (self.meteor_hit_laser):
                    self.explos.play()
                # We delete the laser after it explodes
                for _ in self.meteor_hit_laser:
                    self.all_sprite_list.remove(lasser)
                    self.laser_list.remove(lasser)
                    self.score += 1
            # Lives
            for _ in self.meteor_hit_list:
                self.lives -= 1
            # When it's game over
            if self.lives == -1 or len(self.meteor_list)==0:
                self.game_over = True
                self.lives = 0
    
    def display_frame(self, screen, backg):
        # Background white
        screen.blit(backg, [0, 0])
        # Draw all elements
        self.all_sprite_list.draw(screen)
        # Draw Score
        text = pygame.font.SysFont("Courier", 30)
        label = text.render("Score: {}".format(self.score), 1, white)
        screen.blit(label, (size_x*3/8, 10))
        # Draw Lifes
        text = pygame.font.SysFont("Courier", 30)
        label = text.render("Lives: {}".format(self.lives), 1, white)
        screen.blit(label, (size_x*5/8, 10))
        if self.game_over:
            # Draw GAME OVER
            game_text = pygame.font.SysFont("Courier", 120)
            game_text = game_text.render("GAME OVER", True, white)
            screen.blit(game_text, (size_x*2/10, 2*size_y/6))
        # Updates screen
        pygame.display.flip()
        
#####---------------------------------------------------#####
#####---------------------------------------------------#####

# Main Function
def main():
    pygame.init()
    # Create display and clock
    screen = pygame.display.set_mode([size_x, size_y])
    clock = pygame.time.Clock()
    # Mouse invisible        
    pygame.mouse.set_visible(0) #mouse invisible
    # Screen and background
    backg = pygame.image.load("space.jpg").convert()
    backg = pygame.transform.scale(backg, (size_x, size_y))  #resize
    game = Game()
    
    while True:
        game.process_events()
        game.run_logic()
        game.display_frame(screen, backg)
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()