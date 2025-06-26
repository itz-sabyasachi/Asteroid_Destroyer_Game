import pygame 
import random
import os 

#Initializing pygame 
pygame.init()
pygame.font.init()

#Initializing game constants......
WIDTH = 1280
HEIGHT = 720

player_width = 120
player_height = 120

ASTEROID_width = 60
ASTEROID_height = 60

BULLET_width = 50
BULLET_height = 50

BUTTON_width = 250
BUTTON_height = 100

ALIEN_width = 200
ALEIN_height = 200

BEEM_width = 720
BEEM_height = 40

X = (WIDTH - 120) // 2
Y = HEIGHT - 140

FONT_X = 20
FONT_Y = 20

ALIEN_appearence_interval = 500 

WHITE = (255,255,255)

#Loading ASSETS....
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Asteroid_Destroyer!!")
BG_0 = pygame.image.load(os.path.join("Asteroid_Destroyer","Assets","Images","BG_1.png")) #loading the background
BG = pygame.transform.scale(BG_0, (WIDTH,HEIGHT))  # resize to match screen
BUTTON = pygame.transform.scale(pygame.image.load(os.path.join("Asteroid_Destroyer","Assets","Images","BUTTON.png")),(BUTTON_width,BUTTON_height))
ALIEN = pygame.transform.scale(pygame.image.load(os.path.join("Asteroid_Destroyer","Assets","Images","ALIEN.png")),(ALIEN_width,ALEIN_height))
ALIEN_BEEM = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("Asteroid_Destroyer","Assets","Images","ALIEN_BEEM.png")),(BEEM_width,BEEM_height)),270)
PEW = pygame.mixer.Sound(os.path.join("Asteroid_Destroyer","Assets","SFX","PEW.wav"))
BOOM = pygame.mixer.Sound(os.path.join("Asteroid_Destroyer","Assets","SFX","BOOM.wav"))
font = pygame.font.SysFont("arial", 30, bold = True)
font_custom = pygame.font.Font(os.path.join("Asteroid_Destroyer","Assets","Fonts","Orbitron_regular.ttf"),80)
LEVEL_UP = pygame.mixer.Sound(os.path.join("Asteroid_Destroyer","Assets","SFX","LEVEL_UP.mp3"))
ALIEN_LASER_SOUND = pygame.mixer.Sound(os.path.join("Asteroid_Destroyer","Assets","SFX","LASER_SOUND.wav"))
ALIEN_LASER_SOUND.set_volume(0.5)
ALEIN_DEATH_SOUND = pygame.mixer.Sound(os.path.join("Asteroid_Destroyer","Assets","SFX","ALIEN_DEATH.wav"))
ALIEN_BGM_PATH = os.path.join("Asteroid_Destroyer", "Assets", "SFX", "ALIEN_THEME.wav")
SPACE_BGM_PATH = os.path.join("Asteroid_Destroyer","Assets","SFX","BGM.wav")
PAUSE = pygame.mixer.Sound(os.path.join("Asteroid_Destroyer","Assets","SFX","PAUSE.wav"))

class Player:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height 
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("Asteroid_Destroyer","Assets","Images","SHIP.png")),(120,120))
        self.rect = pygame.Rect(x,y,width,height)

    def draw(self,WIN):
        WIN.blit(self.image,(self.rect.x,self.rect.y))

    def move(self,keys,dt = 0):
        if keys[pygame.K_a] and self.rect.left >= 0:
            self.rect.x -= 600*dt
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += 600*dt
        if keys[pygame.K_w] and self.rect.top >= 0:  
            self.rect.y -= 600 * dt
        if keys[pygame.K_s] and self.rect.bottom <= HEIGHT:  
            self.rect.y += 600 * dt


class ASteroid:
    def __init__(self):
        ASTEROID_SPAWN_MIN_Y = -HEIGHT // 4
        ASTEROID_SPAWN_MAX_Y = -HEIGHT // 15
        self.x = random.randint(0,WIDTH-60)
        self.y = random.randrange(ASTEROID_SPAWN_MIN_Y, ASTEROID_SPAWN_MAX_Y)
        self.speed = 250
        self.final_speed = 750
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("Asteroid_Destroyer","Assets","Images","ASTEROID.png")),(ASTEROID_width,ASTEROID_height))
        self.rect = pygame.Rect(self.x, self.y,ASTEROID_width,ASTEROID_height)

    def draw(self,WIN):
        WIN.blit(self.image,(self.rect.x,self.rect.y))
    def move(self,SCORE,dt):
        self.speed = min(250 + (SCORE*0.25),self.final_speed)
        self.rect.y += self.speed*dt


class Bullet:
    def __init__(self,x,y):
        self.x = x
        self.y = y 
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("Asteroid_Destroyer\Assets\Images\BLAST.png")),(BULLET_width,BULLET_height)),270)
        self.rect = pygame.Rect(self.x,self.y,BULLET_width,BULLET_height)
        self.speed = 2000
    def draw(self,WIN):
        WIN.blit(self.image,(self.rect.x,self.rect.y))
    def move(self,dt):
        self.rect.y -= self.speed * dt



class Button:
    def __init__(self,x,y,text,image,width,height):
        self.x = x
        self.y = y
        self.text = text 
        self.image = image 
        self.rect = self.image.get_rect(topleft=(x, y)) #changing here now
    def draw(self,font,colour,WIN):
        WIN.blit(self.image,(self.rect.x,self.rect.y))        
        font_size = int(self.rect.height* 0.4)  # You can adjust 0.5 to your preference
        dynamic_font = pygame.font.Font(None, font_size)
        button_text = dynamic_font.render(self.text, True, colour)
        text_rect = button_text.get_rect(center=self.rect.center)
        WIN.blit(button_text,(self.rect.x + int(self.rect.width / 2) - int(button_text.get_width() / 2) , self.rect.y + 35 ))
    def is_clicked(self,mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class Alien:
    def __init__(self,width,height,image,HP = 100):
        self.x = WIDTH//2 - 85
        self.y = -50
        self.width = width 
        self.height = height 
        self.image = image 
        self.HP = HP 
        self.y_fixed = 20
        self.speed = 200
        self.reached_position = False
        self.direction = 1 
        self.rect = self.image.get_rect(topleft = (self.x,self.y))
        self.alive = True
        self.laser = None
        self.shoot_delay = 3  # seconds between possible shots
        self.shoot_timer = 0
        self.is_shooting = False

    def update(self, dt):
        if not self.alive:
            return 
        if not self.reached_position:
            self.rect.y += self.speed * dt
            if self.rect.y >= self.y_fixed:
                self.rect.y = self.y_fixed
                self.reached_position = True
        else:
            self.rect.x += self.speed * dt * self.direction
            if self.rect.right >= WIDTH or self.rect.left <= 0:
                self.direction *= -1 
            
            self.shoot_timer += dt
            if self.shoot_timer >= self.shoot_delay and not self.is_shooting:
                self.shoot_laser()
                self.shoot_timer = 0

        if self.laser:
            self.laser.update(dt)
            if not self.laser.active:
                self.laser = None
                self.is_shooting = False

    def damage(self,amount):
        self.HP -= amount
        if self.HP <= 0:
            self.alive = False
            self.laser = None
            ALEIN_DEATH_SOUND.play()

    def shoot_laser(self):
        self.is_shooting = True
        laser_x = self.rect.centerx - 5
        laser_y = self.rect.bottom
        self.laser = Alien_Laser(laser_x, laser_y, 10, HEIGHT - laser_y)
        ALIEN_LASER_SOUND.play()

    def draw(self,WIN):
        if self.alive:
            WIN.blit(self.image,self.rect)
            if self.laser:
                self.laser.draw(WIN)

class Alien_Laser:
    def __init__(self,x,y,width,height):
        self.image = ALIEN_BEEM
        self.rect = self.image.get_rect(topleft = (x,y))
        self.speed = 600
        self.active = True 
    def update(self,dt):
        if self.active:
            self.rect.y += self.speed * dt
            if self.rect.top >= HEIGHT:
                self.active = False 
    def draw(self,WIN):
        if self.active:
            WIN.blit(self.image,self.rect)

def score(WIN,SCORE):
    score_font = font.render(f"SCORE:{SCORE}",True,(255,255,255))
    WIN.blit(score_font,(FONT_X,FONT_Y))

def load_high_score():
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
        return 0
    with open("highscore.txt", "r") as f:
        content = f.read().strip()
        if content.isdigit():
            return int(content)
        else:
            return 0
    
def save_high_score(new_score):
    with open("highscore.txt","w") as f:
        f.write(str(new_score))

def main_menu():
    waiting = True
    play_button = Button((WIDTH//2) - 350,HEIGHT//2 + 120,"PLAY",BUTTON,BULLET_width,BUTTON_height)
    settings_button = Button((WIDTH//2) + 50,HEIGHT//2 + 120,"SETTINGS",BUTTON,BULLET_width,BUTTON_height)
    high_score = load_high_score()
    while waiting:
        WIN.blit(BG,(0,0))
        welcome_menu_UP_font = font_custom.render("WELCOME TO",True,WHITE)
        welcome_menu_LOW_font = font_custom.render("ASTEROID DESTROYER!!",True,WHITE)
        high_score_display = font.render(f"HIGH SCORE: {load_high_score()}", True, WHITE)
        pause_message_font = font_custom.render("Press p to PAUSE!!",True,WHITE)
        welcome_menu_UP_font_rect =welcome_menu_UP_font.get_rect(center = (WIDTH//2,HEIGHT//2 - 100))
        welcome_menu_LOW_font_rect =welcome_menu_UP_font.get_rect(center = (WIDTH//2 - 200,HEIGHT//2 - 10 ))
        high_score_rect = high_score_display.get_rect(center=(WIDTH//2, HEIGHT//2 + 40))
        pause_message_font_rect = pause_message_font.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 300))
        WIN.blit(welcome_menu_UP_font,welcome_menu_UP_font_rect)
        WIN.blit(welcome_menu_LOW_font,welcome_menu_LOW_font_rect)
        WIN.blit(high_score_display, high_score_rect)
        play_button.draw(font_custom,WHITE,WIN)
        settings_button.draw(font_custom,WHITE,WIN)
        WIN.blit(pause_message_font,pause_message_font_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button.is_clicked(mouse_pos):
                    waiting = False
                    main()
                elif settings_button.is_clicked(mouse_pos):
                    settings()


def game_over(BUTTON,SCORE,WIN,WHITE,running):
    waiting = True
    play_again_button = Button((WIDTH//2) - 350,HEIGHT//2 + 120,"PLAY AGAIN",BUTTON,BULLET_width,BUTTON_height)
    quit_button = Button((WIDTH//2) + 70,HEIGHT//2 + 120,"QUIT",BUTTON,BULLET_width,BUTTON_height)
    while waiting:
        WIN.blit(BG,(0,0))
        game_over_font = font_custom.render("GAME OVER!",False,(255,255,255))
        final_score = font.render(f"SCORE = {SCORE}",False,(255,255,255))
        high_score_display = font.render(f"HIGH SCORE = {load_high_score()}", False, WHITE)
        game_over_rect = game_over_font.get_rect(center=(WIDTH//2, HEIGHT//2))
        final_score_rect = final_score.get_rect(center=(WIDTH//2, HEIGHT//2 +60))
        high_score_rect = high_score_display.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
        WIN.blit(game_over_font,game_over_rect)
        WIN.blit(final_score,final_score_rect)
        WIN.blit(high_score_display, high_score_rect)
        play_again_button.draw(font_custom,WHITE,WIN)
        quit_button.draw(font_custom,WHITE,WIN)
        pygame.display.update() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                break 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_button.is_clicked(mouse_pos):
                    waiting = False  
                    return "RESTART"
                elif quit_button.is_clicked(mouse_pos):
                    waiting = False 
                    pygame.quit()
                    exit()

def settings():
    global FPS
    setting = True
    fps60_button = Button(WIDTH//2 - 200, HEIGHT//2, "60 FPS", BUTTON, BUTTON_width, BUTTON_height)
    fps144_button = Button(WIDTH//2 + 50, HEIGHT//2, "144 FPS", BUTTON, BUTTON_width, BUTTON_height)
    while setting:
        WIN.blit(BG, (0, 0))
        settings_text = font_custom.render("SELECT FRAME RATE", True, WHITE)
        settings_text_rect = settings_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
        WIN.blit(settings_text, settings_text_rect)
        fps60_button.draw(font_custom, WHITE, WIN)
        fps144_button.draw(font_custom, WHITE, WIN)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if fps60_button.is_clicked(mouse_pos):
                    FPS = 60
                    setting = False
                elif fps144_button.is_clicked(mouse_pos):
                    FPS = 144
                    setting = False

# def play_music(path, volume=0.2, loop=-1):
#     pygame.mixer.music.load(path)
#     pygame.mixer.music.set_volume(volume)
#     pygame.mixer.music.play(loop)


def draw(ship,asteroid,asteroids,bullets,SCORE,dt,alien):
    WIN.blit(BG,(0,0))
    ship.draw(WIN)
    score(WIN,SCORE)
    for asteroid in asteroids[:]:
        asteroid.move(SCORE,dt)
        if asteroid.rect.y > HEIGHT:
            asteroids.remove(asteroid)
        else:
            asteroid.draw(WIN)
    for bullet in bullets[:]:
        bullet.move(dt)
        if bullet.rect.y < 0:
            bullets.remove(bullet)
        else:
            bullet.draw(WIN)
    if alien and alien.alive:
        alien.update(dt)
        alien.draw(WIN)
    if alien and alien.laser and alien.laser.active:
        alien.laser.draw(WIN)
    pygame.display.update()


def main():
    running  = True 
    FPS = 60
    SCORE = 0
    HIGH_SCORE = load_high_score()
    player = pygame.Rect(X,Y,player_width,player_height)
    clock = pygame.time.Clock()
    ship = Player(X,Y,player_width,player_height)
    asteroid = ASteroid()
    asteroids = []
    bullets = []
    SPAWN_INTERVAL = 1000  
    MIN_SPAWN_INTERVAL = 200
    SPAWN_DECREASE_STEP = 100
    THRESHOLD = 100
    last_spawn_time = 0
    alien = None 
    next_alien_score = ALIEN_appearence_interval
    pygame.mixer.music.load(SPACE_BGM_PATH)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    alien_music_playing = False
    paused = False
    pause_start_time = 0
    total_paused_duration = 0
    fullscreen = False

    while running:        
        dt = clock.tick(FPS)/1000
        current_time = pygame.time.get_ticks()
        if (alien is None or not alien.alive) and  current_time - last_spawn_time >= SPAWN_INTERVAL:
             asteroids.append(ASteroid())
             last_spawn_time = current_time
        for event in pygame.event.get():
            if event.type  == pygame.QUIT:
                running = False
                break  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if  event.button == 1 :
                    bullets.append(Bullet(ship.rect.centerx - BULLET_width//2,ship.rect.y))
                    PEW.play()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                    PAUSE.play()
                    if not paused:
                        last_spawn_time = pygame.time.get_ticks()
                    else:
                        total_paused_duration += pygame.time.get_ticks() - pause_start_time

        if paused:
            pause_text = font.render("PAUSED - Press 'P' to Resume", True, WHITE)
            text_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            WIN.blit(pause_text, text_rect)
            pygame.display.update()
            continue

        keys = pygame.key.get_pressed()
        ship.move(keys,dt)
        for asteroid in asteroids[:]:
            if asteroid.rect.colliderect(ship.rect):
                BOOM.play()
                running  = False
                break
        if not running:
             asteroids.clear()
             bullets.clear()
             if SCORE > HIGH_SCORE:
                HIGH_SCORE = SCORE
                save_high_score(SCORE)
             result = game_over(BUTTON, SCORE, WIN, WHITE, running)
             if result == "RESTART":
                main()

        for asteroid in asteroids[:]:
            for bullet in bullets[:]:
                if asteroid.rect.colliderect(bullet.rect):
                    SCORE += 10                  
                    asteroids.remove(asteroid)
                    bullets.remove(bullet)
                    BOOM.play()
 
        if SCORE >= next_alien_score:
            alien = Alien(ALIEN_width,ALEIN_height,ALIEN)
            next_alien_score += ALIEN_appearence_interval

        if alien and alien.alive:
            alien.update(dt)
            if alien.laser:
                alien.laser.update(dt)
        
        if alien and alien.alive and not alien_music_playing:
            alien_music_playing = True
            pygame.mixer.music.load(ALIEN_BGM_PATH)  
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)

        if alien and not alien.alive and alien_music_playing:
            alien_music_playing = False
            pygame.mixer.music.load(SPACE_BGM_PATH)
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)

        if alien and alien.laser and alien.laser.active:
             if ship.rect.colliderect(alien.laser.rect):
                BOOM.play()
                running = False
             if SCORE > HIGH_SCORE:
                HIGH_SCORE = SCORE
                save_high_score(SCORE)
                
        if not running:
            asteroids.clear()
            bullets.clear()
            result = game_over(BUTTON,SCORE,WIN,WHITE,running)
            if result == "RESTART":
                main()
            
        for bullet in bullets[:]:
            if alien and alien.alive and alien.rect.colliderect(bullet.rect):
                alien.damage(5)
                bullets.remove(bullet)
                BOOM.play()
                    
        if SCORE >= THRESHOLD and SPAWN_INTERVAL > MIN_SPAWN_INTERVAL:
            SPAWN_INTERVAL -= SPAWN_DECREASE_STEP
            THRESHOLD += 100
            LEVEL_UP.play()
    
        draw(ship,asteroid,asteroids,bullets,SCORE,dt,alien)

    pygame.quit() 

if __name__ == "__main__":
    main_menu()



