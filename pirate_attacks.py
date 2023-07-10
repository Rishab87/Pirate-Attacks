import pygame 
pygame.font.init()
pygame.mixer.init()


HEIGHT , WIDTH = 500,900
SHIP_WIDTH = 46
SHIP_HEIGHT = 73

HEALTH_FONT = pygame.font.SysFont('comicsans' , 40)
WINNER_FONT = pygame.font.SysFont('comicsans' , 100)

BULLET_HIT_SOUND = pygame.mixer.Sound("CANNON.mp3")
HIT_SOUND  = pygame.mixer.Sound("Assets_Grenade+1.mp3")

SHIP_VEL = 2
BULLET_VEL = 4

MAX_BULLET = 2
RED_HIT = pygame.USEREVENT +1
GREEN_HIT = pygame.USEREVENT + 2

RED = (255,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)

FPS = 60

RED_SHIP = pygame.transform.scale(pygame.image.load("ship (3).png") , (SHIP_WIDTH , SHIP_HEIGHT))
GREEN_SHIP = pygame.transform.scale(pygame.image.load("ship (4).png") , (SHIP_WIDTH , SHIP_HEIGHT))
WATER = pygame.transform.scale(pygame.image.load("water.png") , (WIDTH,HEIGHT))

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pirate Attacks!")

def red_handle_movement(key_pressed , red_ship):
    if key_pressed[pygame.K_a] and red_ship.x >0:
        red_ship.x -= SHIP_VEL
    if key_pressed[pygame.K_d] and red_ship.x <WIDTH - SHIP_WIDTH:
        red_ship.x += SHIP_VEL
    if key_pressed[pygame.K_w] and red_ship.y >0:
        red_ship.y -= SHIP_VEL
    if key_pressed[pygame.K_s] and red_ship.y < HEIGHT-SHIP_HEIGHT:
        red_ship.y += SHIP_VEL
    
    
def green_handle_movement(key_pressed , green_ship):
    if key_pressed[pygame.K_LEFT] and green_ship.x >0:
        green_ship.x -= SHIP_VEL
    if key_pressed[pygame.K_RIGHT] and green_ship.x <WIDTH-SHIP_WIDTH:
        green_ship.x += SHIP_VEL
    if key_pressed[pygame.K_UP] and green_ship.y >0:
        green_ship.y -= SHIP_VEL
    if key_pressed[pygame.K_DOWN] and green_ship.y < HEIGHT - SHIP_HEIGHT:
        green_ship.y += SHIP_VEL


def bullet_handle(red_bullets , green_bullets , red_ship , green_ship , other_red_bullets , other_green_bullets):

    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if green_ship.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            red_bullets.remove(bullet)
        elif bullet.x >WIDTH:
            red_bullets.remove(bullet)

    for bullet in green_bullets:
        bullet.x -= BULLET_VEL
        if red_ship.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            green_bullets.remove(bullet)
        elif bullet.x <0:
            green_bullets.remove(bullet)

    for bullet in other_green_bullets:
        bullet.x += BULLET_VEL
        if red_ship.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            other_green_bullets.remove(bullet)
        elif bullet.x >WIDTH:
            other_green_bullets.remove(bullet)
    
    for bullet in other_red_bullets:
        bullet.x -= BULLET_VEL
        if green_ship.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            other_red_bullets.remove(bullet)
        elif bullet.x <0:
            other_red_bullets.remove(bullet)
    
def draw_winner_text(text):
    draw_text = WINNER_FONT.render(text , 1 , WHITE)
    WIN.blit(draw_text , (WIDTH/2 - draw_text.get_width()/2 , HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def draw_window(red_ship , green_ship , red_bullets , green_bullets ,other_red_bullets , other_green_bullets , red_health , green_health):
    WIN.blit(WATER , (0,0))
    WIN.blit(RED_SHIP , (red_ship.x , red_ship.y))
    WIN.blit(GREEN_SHIP , (green_ship.x , green_ship.y))

    red_health_text = HEALTH_FONT.render("HEALTH:" + str(red_health) , 1 , RED)
    green_health_text = HEALTH_FONT.render("HEALTH:" + str(green_health) , 1 ,GREEN)

    WIN.blit(green_health_text , (WIDTH - green_health_text.get_width()-10, 10))
    WIN.blit(red_health_text , (10 , 10))

    for bullet in red_bullets:
        pygame.draw.rect(WIN ,RED , bullet)
    for bullet in green_bullets:
        pygame.draw.rect(WIN , GREEN , bullet)
    for bullet in other_red_bullets:
        pygame.draw.rect(WIN ,RED , bullet)
    for bullet in other_green_bullets:
        pygame.draw.rect(WIN , GREEN , bullet)
    
    pygame.display.update()


def main():
    red_ship = pygame.Rect(300 , 250 , SHIP_WIDTH, SHIP_HEIGHT)
    green_ship = pygame.Rect(600 , 250 , SHIP_WIDTH , SHIP_HEIGHT)

    red_bullets = []
    green_bullets = []
    other_red_bullets = []
    other_green_bullets = []

    red_health = 10
    green_health = 10
    winner_text = ''

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and len(red_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(red_ship.x + red_ship.width , red_ship.y + red_ship.height//2 -5 ,20 , 10)
                    red_bullets.append(bullet)
                    BULLET_HIT_SOUND.play()

                if event.key == pygame.K_RCTRL and len(green_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(green_ship.x , green_ship.y + green_ship.height//2 -5 ,20 , 10)
                    green_bullets.append(bullet)
                    BULLET_HIT_SOUND.play()

                if event.key == pygame.K_q and len(other_red_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(red_ship.x , red_ship.y + red_ship.height//2 -5 ,20 , 10)
                    other_red_bullets.append(bullet)
                    BULLET_HIT_SOUND.play()

                if event.key == pygame.K_KP_0 and len(other_green_bullets) < MAX_BULLET or event.key == pygame.K_0 and len(other_green_bullets)<MAX_BULLET:
                    bullet = pygame.Rect(green_ship.x+ green_ship.width , green_ship.y + green_ship.height//2 -5 ,20 , 10)
                    other_green_bullets.append(bullet)
                    BULLET_HIT_SOUND.play()

            if event.type == RED_HIT:
                red_health -=1
                HIT_SOUND.play()
            if event.type == GREEN_HIT:
                green_health -=1
                HIT_SOUND.play()
        
        if red_health <=0:
            winner_text = "GREEN WINS!"
        if green_health <=0:
            winner_text = "RED WINS!"
        if winner_text != "":
            draw_winner_text(winner_text)
            break

        key_pressed = pygame.key.get_pressed()
        red_handle_movement(key_pressed , red_ship)
        green_handle_movement(key_pressed,green_ship)
        bullet_handle(red_bullets ,green_bullets , red_ship , green_ship , other_red_bullets,other_green_bullets)
        draw_window(red_ship , green_ship , red_bullets , green_bullets , other_red_bullets,other_green_bullets , red_health ,green_health)
  
        
    
    main()

if __name__ == '__main__':
    main()
