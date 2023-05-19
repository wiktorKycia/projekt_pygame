import pygame
import os
import random
import math
from subprocess import *
pygame.init()
pygame.display.set_caption("Niszczyciel asteroid")
#wczytywanie ustawień
plik = open('settings.txt', 'r')
ustawienia = []
for line in plik.readlines():
    line = line.strip()
    ustawienia.append(line)
plik.close()

x = ustawienia[2]
ustawienia[2] = int(x)
player_name = ustawienia[0]
difficulty_level = ustawienia[1]
fps = ustawienia[2]
plane_style_path = "samolot_" + ustawienia[3] + ".png"
if ustawienia[4] != "zwykly":
    shot_sound_path = "0" + ustawienia[4] + ".wav"
else:
    shot_sound_path = "strza.wav"
bg_style = ustawienia[5] + ".png"
x2 = ustawienia[6]
player_speed = int(x2)


class Player:
    def __init__(self):
        self.x = 50
        self.y = 50
        self.grafika = pygame.image.load(os.path.join(plane_style_path))
        self.width = self.grafika.get_width()
        self.height = self.grafika.get_height()
        self.ksztalt = pygame.Rect(self.x, self.y, self.width, self.height)
        self.pociski = []
        self.zegar = 0
        self.ammo_zegar = 0
        self.amunicja = 30

    def draw(self):
        self.ksztalt = pygame.Rect(self.x, self.y, self.width, self.height)
        screen.blit(self.grafika, (self.x, self.y))
        # pygame.draw.rect(screen, (150, 140, 120), self.ksztalt)

    def tick(self, keys, speed=player_speed):
        if keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_KP8]:
            self.y -= speed * dt
        if keys[pygame.K_a] or keys[pygame.K_LEFT] or keys[pygame.K_KP4]:
            self.x -= speed * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN] or keys[pygame.K_KP5]:
            self.y += speed * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT] or keys[pygame.K_KP6]:
            self.x += speed * dt
        
        if self.y < 60:
            self.y = 60
        if self.y > height - self.height:
            self.y = height - self.height
        if self.x < 0:
            self.x = 0
        if self.x > width - self.width:
            self.x = width - self.width
        
        self.zegar += pygame.time.Clock().tick(max_tps)/1000
        if (keys[pygame.K_SPACE] or keys[pygame.K_KP_PLUS]) and self.zegar >= 0.04 and self.amunicja >= 1:
            self.zegar = 0
            self.amunicja -= 1
            self.pociski.append(Pocisk())
            mixer.Sound.play(shot_sound)
        
        self.ammo_zegar += pygame.time.Clock().tick(max_tps)/1000
        if self.ammo_zegar >= 1.0:
            self.ammo_zegar = 0
            self.amunicja += 1
        
        self.draw()


class Pocisk:
    def __init__(self):
        self.x = player.x + player.width
        self.y = player.y + player.height/2
        self.width = 25
        self.height = 5
        self.ksztalt = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        self.ksztalt = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (255, 0, 0), self.ksztalt)

    def tick(self, keys, speed=100):
        self.x += speed * dt

class Wrogi_pocisk:
    def __init__(self):
        self.x = wrog.x
        self.y = wrog.y + wrog.height/2
        self.width = 40
        self.height = 5
        self.ksztalt = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        self.ksztalt = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (0, 255, 0), self.ksztalt)

    def tick(self, keys, speed=100):
        self.x -= speed * dt

fire_small = pygame.image.load("ogien1.png")
fire_huge = pygame.image.load("ogien2.png")

class Przeszkoda:
    def __init__(self):
        self.asteroida = random.randint(1, 2)
        self.x = 1300
        self.y = random.randint(60, 640)
        if self.asteroida == 1:
            self.width = 50
            self.height = 50
            self.image = pygame.image.load("asteroida1.png")
        if self.asteroida == 2:
            self.width = 80
            self.height = 80
            self.image = pygame.image.load("asteroida2.png")
        self.ksztalt = pygame.Rect(self.x, self.y, self.width, self.height)
        self.angle = 1
        
    def draw(self):
        self.ksztalt = pygame.Rect(self.x, self.y, self.width, self.height)
        obrocony_image = pygame.transform.rotate(self.image, self.angle)
        self.angle += 20 * dt
        if self.asteroida == 1:
            nowy_rect = obrocony_image.get_rect(center = self.image.get_rect(center = (self.x + 25, self.y + 25)).center)
            screen.blit(fire_small, (self.x, self.y))
        if self.asteroida == 2:
            nowy_rect = obrocony_image.get_rect(center = self.image.get_rect(center = (self.x + 40, self.y + 40)).center)
            screen.blit(fire_huge, (self.x, self.y))
        screen.blit(obrocony_image, nowy_rect)

    def tick(self, keys, speed=60):
        self.x -= speed * dt

skrzynia_image = pygame.image.load("Ammo.png")

class Skrzynia:
    def __init__(self):
        self.x = 1300
        self.y = random.randint(60, 660)
        self.width = 80
        self.height = 80
        self.ksztalt = pygame.Rect(self.x, self.y, self.width, self.height)
        self.kolor = (255, 255, 255)

    def draw(self):
        self.ksztalt = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.kolor, self.ksztalt)
        screen.blit(skrzynia_image,(self.x, self.y))

    def tick(self, keys, speed=20):
        self.x -= speed * dt

hp_image = pygame.image.load("hp.png")

class HP:
    def __init__(self):
        self.x = 409
        self.y = 9
        self.width = 202
        self.height = 32
        self.ksztalt = pygame.Rect(self.x, self.y, self.width, self.height)
        self.kolor = (255, 0, 0)

    def draw(self):
        self.ksztalt = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.kolor, self.ksztalt)
        screen.blit(hp_image,(400, 0))

wrog_image = pygame.image.load("wrog.png")

class Wrog:
    def __init__(self):
        self.x = 1180
        self.y = random.randint(0, 660)
        self.width = 100
        self.height = 50
        self.ksztalt = pygame.Rect(self.x, self.y, self.width, self.height)
        self.kolor = (0, 0, 255)
        self.kierunek = 1
        self.zegar = 0
        self.pociski = []

    def draw(self):
        self.ksztalt = pygame.Rect(self.x, self.y, self.width, self.height)
        screen.blit(wrog_image, (self.x, self.y))

    def tick(self, speed=30):
        if self.kierunek == 1:
            self.y += speed * dt
            if self.y >= 680:
                self.kierunek = 2
        if self.kierunek == 2:
            self.y -= speed * dt
            if self.y <= 0:
                self.kierunek = 1
        self.zegar += pygame.time.Clock().tick(max_tps)/1000
        if self.zegar >= 0.12:
            self.zegar = 0
            self.pociski.append(Wrogi_pocisk())
            mixer.Sound.play(shot_sound)
        for pocisk in self.pociski:
            pocisk.tick(keys)
            pocisk.draw()
            if pocisk.x == 0:
                self.pociski.remove(pocisk)
            if pocisk.ksztalt.colliderect(player.ksztalt):
                mixer.Sound.play(wybuch_sound)
                self.pociski.remove(pocisk)
                hp.width -= 51

    

from pygame import mixer

#Instantiate mixer

background_music = "interweb.mp3"
mixer.init()
wybuch_sound = mixer.Sound('wybuch.WAV')
wybuch_sound.set_volume(0.1)
shot_sound = mixer.Sound(shot_sound_path)
shot_sound.set_volume(0.2)
mixer.music.load(background_music)
mixer.music.set_volume(0.4)
mixer.music.play(-1)
#Load audio file
# mixer.Sound.load('00001000.WAV')#quiet short
# mixer.Sound.load('00001998.WAV')#heavy rifle
# mixer.Sound.load('00028001.WAV')#revolwer
# mixer.Sound.load('00028000.WAV')#frog
#Set preferred volume

width = 1280
height = 720
poziom = difficulty_level
screen = pygame.display.set_mode((width, height))

koniec_image = pygame.image.load("tabela_wynik.png")

dyrektor_image = pygame.image.load("dyrektor.png")

przegrana_image = pygame.font.Font.render(pygame.font.SysFont("arial", 50), f"PRZEGRAŁAŚ/EŚ", True, (0, 0, 0))
#score
score = 0
score_zegar = 0

#obstacles
przeszkody = []
przeszkody_zegar = 0

skrzynki = []
skrzynki_zegar = 0

wrogowie = []
wrogowie_zegar = 0

player = Player()
hp = HP()

# background
bg = pygame.image.load(bg_style).convert()
bg_width = bg.get_width()

scroll = 0
tiles = math.ceil(width / bg_width) + 1

# tps
max_tps = fps
clock = pygame.time.Clock()

flaga = False # potrzebne przy wypisywaniu wyników
Ernest = 0 # Ernest jest potrzebny przy zapisywaniu wyników
while True:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    keys = pygame.key.get_pressed()

    #Ticking
    dt = clock.tick(max_tps) / 100 # clock.tick(100.0) <- zwraca czas pomiędzy klatkami
    
    # Main program
    match poziom:
        case "latwy": #==================================================ŁATWY==================================================
            if hp.width > 0: #gra
                #background
                for i in range(0, tiles):
                    screen.blit(bg, (i*bg_width + scroll, 0))
                scroll -= 10
                if abs(scroll) > bg_width:
                    scroll = 0
                
                player.tick(keys)

                hp.draw()
                
                #PRZESZKODY
                przeszkody_zegar += pygame.time.Clock().tick(max_tps)/1000
                if przeszkody_zegar >= 0.7:
                    przeszkody_zegar = 0
                    przeszkody.append(Przeszkoda())
                
                for przeszkoda in przeszkody:
                    przeszkoda.tick(keys)
                    przeszkoda.draw()
                    zniszczona = False
                    for pocisk in player.pociski:
                        if przeszkoda.ksztalt.colliderect(pocisk.ksztalt) or pocisk.ksztalt.colliderect(przeszkoda.ksztalt):
                            mixer.Sound.play(wybuch_sound)
                            if przeszkoda.asteroida == 1:
                                score += 5
                            if przeszkoda.asteroida == 2:
                                score += 8
                            przeszkody.remove(przeszkoda)
                            player.pociski.remove(pocisk)
                            zniszczona = True
                            break
                    
                    if zniszczona: break
                    
                    if przeszkoda.ksztalt.colliderect(player.ksztalt):
                        if przeszkoda.asteroida == 1:
                            hp.width -= 25
                        if przeszkoda.asteroida == 2:
                            hp.width -= 40
                        try:
                            mixer.Sound.play(wybuch_sound)
                            przeszkody.remove(przeszkoda)
                        except TypeError or ValueError or Exception or BaseException:
                            pass
                        continue
                    elif przeszkoda.x < 0:
                        if przeszkoda.asteroida == 1:
                            score -= 5
                        if przeszkoda.asteroida == 2:
                            score -= 8
                        przeszkody.remove(przeszkoda)

                #SKRZYNIE
                skrzynki_zegar += pygame.time.Clock().tick(max_tps)/1000
                if skrzynki_zegar >= 1.5:
                    skrzynki_zegar = 0
                    skrzynki.append(Skrzynia())
                
                for skrzynka in skrzynki:
                    skrzynka.tick(keys)
                    skrzynka.draw()
                    if skrzynka.ksztalt.colliderect(player.ksztalt):
                        skrzynki.remove(skrzynka)
                        player.amunicja += 20
                        break
                    for pocisk in player.pociski:
                        if skrzynka.ksztalt.colliderect(pocisk.ksztalt):
                            player.pociski.remove(pocisk)
                            try:
                                mixer.Sound.play(wybuch_sound)
                                skrzynki.remove(skrzynka)
                            except ValueError or BaseException or TypeError or Exception:
                                pass
                            break
                    if skrzynka.x < 0:
                        skrzynki.remove(skrzynka)

                #POCISKI
                for pocisk in player.pociski:
                    pocisk.tick(keys)
                    pocisk.draw()
                    if pocisk.x > 1280:
                        player.pociski.remove(pocisk)

                #AMMO
                ammo_image = pygame.font.Font.render(pygame.font.SysFont("arial",48), f"Amunicja: {player.amunicja}", True, (150, 150, 0))
                screen.blit(ammo_image, (900, 0))
                
                #WYNIK
                score_zegar += pygame.time.Clock().tick(max_tps)/1000
                if score_zegar >= 1.0:
                    score_zegar = 0.0
                    score += 1
                score_image = pygame.font.Font.render(pygame.font.SysFont("arial",48), f"Wynik: {score}", True, (150, 150, 0))
                screen.blit(score_image, (0, 0))
                
            if hp.width <= 0: #wyniki po grze
                if keys[pygame.K_x]:
                    Popen(["python", "runner.py"])
                    pygame.quit()
                    quit()
                for i in range(0, tiles):
                    screen.blit(bg, (i*bg_width + scroll, 0))
                if abs(scroll) > bg_width:
                    scroll = 0
                player.draw()
                hp.draw()
                if player.amunicja > 0:
                    score += 1
                    player.amunicja -= 1
                    ammo_image = pygame.font.Font.render(pygame.font.SysFont("arial", 48), f"Amunicja: {player.amunicja}", True, (150, 150, 0))
                if player.amunicja == 0:
                    flaga = True
                screen.blit(ammo_image, (900, 0))
                screen.blit(score_image, (0, 0))
                for pocisk in player.pociski:
                    pocisk.draw()
                for skrzynka in skrzynki:
                    skrzynka.draw()
                for przeszkoda in przeszkody:
                    przeszkoda.draw()
                screen.blit(koniec_image,(290, 135))
                screen.blit(przegrana_image, (315, 150))
                screen.blit(dyrektor_image, (650, 280))
                gratulacje_image = pygame.font.Font.render(pygame.font.SysFont("arial", 30), f"Gratulacje!", True, (0, 0, 0))
                screen.blit(gratulacje_image, (735, 240))
                score_image2 = pygame.font.Font.render(pygame.font.SysFont("arial", 50), f"Twój wynik: {score}", True, (0, 0, 150))
                score_image3 = pygame.font.Font.render(pygame.font.SysFont("arial", 30),  f"Najlepsze wyniki poziomie {poziom}:", True, (0, 0, 0))
                screen.blit(score_image2, (685, 150))
                screen.blit(score_image3, (315, 210))
                info = pygame.font.Font.render(pygame.font.SysFont("arial", 31), "Wciśnij x by zagrać ponownie", True, (0, 150, 0))
                screen.blit(info, (315, 515))
                
                # Tabela wyników
                if Ernest == 0 and flaga: # w tym wypadku wykona się tylko 1 raz
                    # Zapisywanie do pliku z najlepszymi wynikami
                    Ernest += 1
                    plik = open("wyniki.txt", "a+")
                    plik.write(f"{player_name} {score} {poziom} \n")
                    
                    # zapisywanie wyników do listy
                    plik.seek(0) # ustawienie kursora na początek pliku
                    wyniki = []
                    for line in plik.readlines():
                        x = line.split()
                        x[1] = int(x[1]) # zamiana wyniku na typ int
                        wyniki.append(x)
                    
                    # Sortowanie wyników
                    for i in range(1, len(wyniki)):
                        key = wyniki[i][1]
                        key2 = wyniki[i]
                        j = i
                        while j-1 >= 0 and key > wyniki[j-1][1]:
                            wyniki[j] = wyniki[j-1]
                            j -= 1
                        wyniki[j] = key2
                    
                    plik.close()
                
                if flaga is False:
                    plik = open("wyniki.txt", "r")
                    # zapisywanie wyników do listy
                    
                    wyniki = []
                    for line in plik.readlines():
                        x = line.split()
                        x[1] = int(x[1]) # zamiana wyniku na typ int
                        wyniki.append(x)
                    
                    # Sortowanie wyników
                    for i in range(1, len(wyniki)):
                        key = wyniki[i][1]
                        key2 = wyniki[i]
                        j = i
                        while j-1 >= 0 and key > wyniki[j-1][1]:
                            wyniki[j] = wyniki[j-1]
                            j -= 1
                        wyniki[j] = key2
                    
                    plik.close()
                
                #Pokazywanie najlepszych wyników
                j = 0
                for wynik in wyniki:
                    if j > 9:
                        break
                    if wynik[2] == poziom:
                        color = (0, 0, 0)
                        if player_name == wynik[0] and score == wynik[1]:
                            color = (180, 0, 0)
                        screen.blit(pygame.font.Font.render(pygame.font.SysFont("arial", 27), f"{j+1}. ", True, color), (315, 245 + j*25))
                        screen.blit(pygame.font.Font.render(pygame.font.SysFont("arial", 27), wynik[0], True, color), (350, 245 + j*25))
                        screen.blit(pygame.font.Font.render(pygame.font.SysFont("arial", 27), str(wynik[1]), True, color), (570, 245 + j*25))
                        j += 1
                
            pygame.display.update()
        case "normalny": #==================================================NORMALNY==================================================
            if hp.width > 0: #gra
                #background
                for i in range(0, tiles):
                    screen.blit(bg, (i*bg_width + scroll, 0))
                scroll -= 10
                if abs(scroll) > bg_width:
                    scroll = 0
                
                player.tick(keys)

                hp.draw()
                
                #PRZESZKODY
                przeszkody_zegar += pygame.time.Clock().tick(max_tps)/1000
                if przeszkody_zegar >= 0.5:
                    przeszkody_zegar = 0
                    przeszkody.append(Przeszkoda())
                
                for przeszkoda in przeszkody:
                    przeszkoda.tick(keys)
                    przeszkoda.draw()
                    zniszczona = False
                    for pocisk in player.pociski:
                        if przeszkoda.ksztalt.colliderect(pocisk.ksztalt) or pocisk.ksztalt.colliderect(przeszkoda.ksztalt):
                            mixer.Sound.play(wybuch_sound)
                            if przeszkoda.asteroida == 1:
                                score += 5
                            if przeszkoda.asteroida == 2:
                                score += 8
                            przeszkody.remove(przeszkoda)
                            player.pociski.remove(pocisk)
                            zniszczona = True
                            break
                    if zniszczona: break
                    
                    if przeszkoda.ksztalt.colliderect(player.ksztalt):
                        if przeszkoda.asteroida == 1:
                            hp.width -= 50
                        if przeszkoda.asteroida == 2:
                            hp.width -= 80
                        try:
                            mixer.Sound.play(wybuch_sound)
                            przeszkody.remove(przeszkoda)
                        except TypeError or ValueError or Exception or BaseException:
                            pass
                        continue
                    elif przeszkoda.x < 0:
                        if przeszkoda.asteroida == 1:
                            score -= 5
                        if przeszkoda.asteroida == 2:
                            score -= 8
                        przeszkody.remove(przeszkoda)
                        

                #SKRZYNIE
                skrzynki_zegar += pygame.time.Clock().tick(max_tps)/1000
                if skrzynki_zegar >= 2.0:
                    skrzynki_zegar = 0
                    skrzynki.append(Skrzynia())
                
                for skrzynka in skrzynki:
                    skrzynka.tick(keys)
                    skrzynka.draw()
                    if skrzynka.ksztalt.colliderect(player.ksztalt):
                        skrzynki.remove(skrzynka)
                        player.amunicja += 15
                        break
                    for pocisk in player.pociski:
                        if skrzynka.ksztalt.colliderect(pocisk.ksztalt):
                            player.pociski.remove(pocisk)
                            try:
                                mixer.Sound.play(wybuch_sound)
                                skrzynki.remove(skrzynka)
                            except ValueError or BaseException or TypeError or Exception:
                                pass
                            break
                    if skrzynka.x < 0:
                        skrzynki.remove(skrzynka)

                #POCISKI
                for pocisk in player.pociski:
                    pocisk.tick(keys)
                    pocisk.draw()
                    if pocisk.x > 1280:
                        player.pociski.remove(pocisk)

                #AMMO
                ammo_image = pygame.font.Font.render(pygame.font.SysFont("arial",48), f"Amunicja: {player.amunicja}", True, (150, 150, 0))
                screen.blit(ammo_image, (900, 0))
                
                #WYNIK
                score_zegar += pygame.time.Clock().tick(max_tps)/1000
                if score_zegar >= 1.0:
                    score_zegar = 0.0
                    score += 1
                score_image = pygame.font.Font.render(pygame.font.SysFont("arial",48), f"Wynik: {score}", True, (150, 150, 0))
                screen.blit(score_image, (0, 0))
                
            if hp.width <= 0: #wyniki po grze
                if keys[pygame.K_x]:
                    Popen(["python", "runner.py"])
                    pygame.quit()
                    quit()
                for i in range(0, tiles):
                    screen.blit(bg, (i*bg_width + scroll, 0))
                if abs(scroll) > bg_width:
                    scroll = 0
                player.draw()
                hp.draw()
                if player.amunicja > 0:
                    score += 1
                    player.amunicja -= 1
                    ammo_image = pygame.font.Font.render(pygame.font.SysFont("arial",48), f"Amunicja: {player.amunicja}", True, (150, 150, 0))
                if player.amunicja == 0:
                    flaga = True
                screen.blit(ammo_image, (900, 0))
                screen.blit(score_image, (0, 0))
                for pocisk in player.pociski:
                    pocisk.draw()
                for skrzynka in skrzynki:
                    skrzynka.draw()
                for przeszkoda in przeszkody:
                    przeszkoda.draw()
                screen.blit(koniec_image,(290, 135))
                screen.blit(przegrana_image, (315, 150))
                screen.blit(dyrektor_image, (650, 280))
                gratulacje_image = pygame.font.Font.render(pygame.font.SysFont("arial", 30), f"Gratulacje!", True, (0, 0, 0))
                screen.blit(gratulacje_image, (735, 240))
                score_image2 = pygame.font.Font.render(pygame.font.SysFont("arial", 50), f"Twój wynik: {score}", True, (0, 0, 150))
                score_image3 = pygame.font.Font.render(pygame.font.SysFont("arial", 30),  f"Najlepsze wyniki poziomie {poziom}:", True, (0, 0, 0))
                screen.blit(score_image2, (685, 150))
                screen.blit(score_image3, (315, 210))
                info = pygame.font.Font.render(pygame.font.SysFont("arial", 31), "Wciśnij x by zagrać ponownie", True, (0, 150, 0))
                screen.blit(info, (315, 515))
                
                # Tabela wyników
                if Ernest == 0 and flaga: # w tym wypadku wykona się tylko 1 raz
                    # Zapisywanie do pliku z najlepszymi wynikami
                    Ernest += 1
                    plik = open("wyniki.txt", "a+")
                    plik.write(f"{player_name} {score} {poziom} \n")
                    
                    # zapisywanie wyników do listy
                    plik.seek(0) # ustawienie kursora na początek pliku
                    wyniki = []
                    for line in plik.readlines():
                        x = line.split()
                        x[1] = int(x[1]) # zamiana wyniku na typ int
                        wyniki.append(x)
                    
                    # Sortowanie wyników
                    for i in range(1, len(wyniki)):
                        key = wyniki[i][1]
                        key2 = wyniki[i]
                        j = i
                        while j-1 >= 0 and key > wyniki[j-1][1]:
                            wyniki[j] = wyniki[j-1]
                            j -= 1
                        wyniki[j] = key2
                    
                    plik.close()
                
                if flaga is False:
                    plik = open("wyniki.txt", "r")
                    # zapisywanie wyników do listy
                    
                    wyniki = []
                    for line in plik.readlines():
                        x = line.split()
                        x[1] = int(x[1]) # zamiana wyniku na typ int
                        wyniki.append(x)
                    
                    # Sortowanie wyników
                    for i in range(1, len(wyniki)):
                        key = wyniki[i][1]
                        key2 = wyniki[i]
                        j = i
                        while j-1 >= 0 and key > wyniki[j-1][1]:
                            wyniki[j] = wyniki[j-1]
                            j -= 1
                        wyniki[j] = key2
                    
                    plik.close()
                
                #Pokazywanie najlepszych wyników
                j = 0
                for wynik in wyniki:
                    if j > 9:
                        break
                    if wynik[2] == poziom:
                        color = (0, 0, 0)
                        if player_name == wynik[0] and score == wynik[1]:
                            color = (180, 0, 0)
                        screen.blit(pygame.font.Font.render(pygame.font.SysFont("arial", 27), f"{j+1}. ", True, color), (315, 245 + j*25))
                        screen.blit(pygame.font.Font.render(pygame.font.SysFont("arial", 27), wynik[0], True, color), (350, 245 + j*25))
                        screen.blit(pygame.font.Font.render(pygame.font.SysFont("arial", 27), str(wynik[1]), True, color), (570, 245 + j*25))
                        j += 1
                
            pygame.display.update()
        case "trudny": #==================================================TRUDNY==================================================
            if hp.width > 0: #gra
                #background
                for i in range(0, tiles):
                    screen.blit(bg, (i*bg_width + scroll, 0))
                scroll -= 10
                if abs(scroll) > bg_width:
                    scroll = 0
                
                player.tick(keys)

                hp.draw()
                
                #WROGOWIE
                wrogowie_zegar += pygame.time.Clock().tick(max_tps)/1000
                if wrogowie_zegar >= 3.5:
                    wrogowie_zegar = 0
                    wrogowie.append(Wrog())

                for wrog in wrogowie:
                    wrog.tick()
                    wrog.draw()
                    for pocisk in player.pociski:
                        if pocisk.ksztalt.colliderect(wrog.ksztalt):
                            mixer.Sound.play(wybuch_sound)
                            player.pociski.remove(pocisk)
                            wrogowie.remove(wrog)
                            score += 5

                #PRZESZKODY
                przeszkody_zegar += pygame.time.Clock().tick(max_tps)/1000
                if przeszkody_zegar >= 0.35:
                    przeszkody_zegar = 0
                    przeszkody.append(Przeszkoda())
                
                for przeszkoda in przeszkody:
                    przeszkoda.tick(keys)
                    przeszkoda.draw()
                    zniszczona = False
                    for pocisk in player.pociski:
                        if przeszkoda.ksztalt.colliderect(pocisk.ksztalt) or pocisk.ksztalt.colliderect(przeszkoda.ksztalt):
                            mixer.Sound.play(wybuch_sound)
                            if przeszkoda.asteroida == 1:
                                score += 5
                            if przeszkoda.asteroida == 2:
                                score += 8
                            przeszkody.remove(przeszkoda)
                            player.pociski.remove(pocisk)
                            zniszczona = True
                            break
                    if zniszczona: break
                    
                    if przeszkoda.ksztalt.colliderect(player.ksztalt):
                        if przeszkoda.asteroida == 1:
                            hp.width -= 101
                        if przeszkoda.asteroida == 2:
                            hp.width -= 202
                        try:
                            mixer.Sound.play(wybuch_sound)
                            przeszkody.remove(przeszkoda)
                        except TypeError or ValueError or Exception or BaseException:
                            pass
                        continue
                    elif przeszkoda.x < 0:
                        if przeszkoda.asteroida == 1:
                            score -= 5
                        if przeszkoda.asteroida == 2:
                            score -= 8
                        przeszkody.remove(przeszkoda)

                #SKRZYNIE
                skrzynki_zegar += pygame.time.Clock().tick(max_tps)/1000
                if skrzynki_zegar >= 2.5:
                    skrzynki_zegar = 0
                    skrzynki.append(Skrzynia())
                
                for skrzynka in skrzynki:
                    skrzynka.tick(keys)
                    skrzynka.draw()
                    if skrzynka.ksztalt.colliderect(player.ksztalt):
                        skrzynki.remove(skrzynka)
                        player.amunicja += 15
                        break
                    for pocisk in player.pociski:
                        if skrzynka.ksztalt.colliderect(pocisk.ksztalt):
                            player.pociski.remove(pocisk)
                            try:
                                mixer.Sound.play(wybuch_sound)
                                skrzynki.remove(skrzynka)
                            except ValueError or BaseException or TypeError or Exception:
                                pass
                            break
                    if skrzynka.x < 0:
                        skrzynki.remove(skrzynka)

                #POCISKI
                for pocisk in player.pociski:
                    pocisk.tick(keys)
                    pocisk.draw()
                    if pocisk.x > 1280:
                        player.pociski.remove(pocisk)

                #AMMO
                ammo_image = pygame.font.Font.render(pygame.font.SysFont("arial",48), f"Amunicja: {player.amunicja}", True, (150, 150, 0))
                screen.blit(ammo_image, (900, 0))
                
                #WYNIK
                score_zegar += pygame.time.Clock().tick(max_tps)/1000
                if score_zegar >= 1.0:
                    score_zegar = 0.0
                    score += 1
                score_image = pygame.font.Font.render(pygame.font.SysFont("arial",48), f"Wynik: {score}", True, (150, 150, 0))
                screen.blit(score_image, (0, 0))
                
            if hp.width <= 0: #wyniki po grze
                if keys[pygame.K_x]:
                    Popen(["python", "runner.py"])
                    pygame.quit()
                    quit()
                for i in range(0, tiles):
                    screen.blit(bg, (i*bg_width + scroll, 0))
                if abs(scroll) > bg_width:
                    scroll = 0
                player.draw()
                hp.draw()
                
                if player.amunicja > 0:
                    score += 1
                    player.amunicja -= 1
                    ammo_image = pygame.font.Font.render(pygame.font.SysFont("arial",48), f"Amunicja: {player.amunicja}", True, (150, 150, 0))
                if player.amunicja == 0:
                    flaga = True
                screen.blit(ammo_image, (900, 0))
                screen.blit(score_image, (0, 0))
                for pocisk in player.pociski:
                    pocisk.draw()
                for skrzynka in skrzynki:
                    skrzynka.draw()
                for przeszkoda in przeszkody:
                    przeszkoda.draw()
                screen.blit(koniec_image,(290, 135))
                screen.blit(przegrana_image, (315, 150))
                screen.blit(dyrektor_image, (650, 280))
                gratulacje_image = pygame.font.Font.render(pygame.font.SysFont("arial", 30), f"Gratulacje!", True, (0, 0, 0))
                screen.blit(gratulacje_image, (735, 240))
                score_image2 = pygame.font.Font.render(pygame.font.SysFont("arial", 50), f"Twój wynik: {score}", True, (0, 0, 150))
                score_image3 = pygame.font.Font.render(pygame.font.SysFont("arial", 30), f"Najlepsze wyniki poziomie {poziom}:", True, (0, 0, 0))
                screen.blit(score_image2, (685, 150))
                screen.blit(score_image3, (315, 210))
                info = pygame.font.Font.render(pygame.font.SysFont("arial", 31), "Wciśnij x by zagrać ponownie", True, (0, 150, 0))
                screen.blit(info, (315, 515))
                
                # Tabela wyników
                if Ernest == 0 and flaga: # w tym wypadku wykona się tylko 1 raz
                    # Zapisywanie do pliku z najlepszymi wynikami
                    Ernest += 1
                    plik = open("wyniki.txt", "a+")
                    plik.write(f"{player_name} {score} {poziom} \n")
                    
                    # zapisywanie wyników do listy
                    plik.seek(0) # ustawienie kursora na początek pliku
                    wyniki = []
                    for line in plik.readlines():
                        x = line.split()
                        x[1] = int(x[1]) # zamiana wyniku na typ int
                        wyniki.append(x)
                    
                    # Sortowanie wyników
                    for i in range(1, len(wyniki)):
                        key = wyniki[i][1]
                        key2 = wyniki[i]
                        j = i
                        while j-1 >= 0 and key > wyniki[j-1][1]:
                            wyniki[j] = wyniki[j-1]
                            j -= 1
                        wyniki[j] = key2
                    
                    plik.close()
                    
                if flaga is False:
                    plik = open("wyniki.txt", "r")
                    # zapisywanie wyników do listy
                    
                    wyniki = []
                    for line in plik.readlines():
                        x = line.split()
                        x[1] = int(x[1]) # zamiana wyniku na typ int
                        wyniki.append(x)
                    
                    # Sortowanie wyników
                    for i in range(1, len(wyniki)):
                        key = wyniki[i][1]
                        key2 = wyniki[i]
                        j = i
                        while j-1 >= 0 and key > wyniki[j-1][1]:
                            wyniki[j] = wyniki[j-1]
                            j -= 1
                        wyniki[j] = key2
                    
                    plik.close()
                
                #Pokazywanie najlepszych wyników
                j = 0
                for wynik in wyniki:
                    if j > 9:
                        break
                    if wynik[2] == poziom:
                        color = (0, 0, 0)
                        if player_name == wynik[0] and score == wynik[1]:
                            color = (180, 0, 0)
                        screen.blit(pygame.font.Font.render(pygame.font.SysFont("arial", 27), f"{j+1}. ", True, color), (315, 245 + j*25))
                        screen.blit(pygame.font.Font.render(pygame.font.SysFont("arial", 27), wynik[0], True, color), (350, 245 + j*25))
                        screen.blit(pygame.font.Font.render(pygame.font.SysFont("arial", 27), str(wynik[1]), True, color), (570, 245 + j*25))
                        j += 1
                 
            pygame.display.update()
        case _:
            print("coś poszło nie tak (prawdopodobnie jest to związane z poziomem trudności)")
            quit()

    screen.fill((40, 40, 40))
