
from random import randint, random
import pygame
import time
import iuten 
import threading
from collections import defaultdict
from copy import copy


nPartidas = 10

c = threading.Condition()
pygame.init()


##########################**SPRITES**#############################


def sprites(peca):
    n = 0 if peca.islower() else 1
    image = pygame.image.load(f'images/{peca}{n}.png')
    return pygame.transform.scale(image, (30,30))
    
sprite = defaultdict(lambda: None)

###################################################################


tile_width = 30
tile_height = 30
margin = 8 
win = pygame.display.set_mode(((tile_width+margin)*17, (tile_height+margin)*11))

white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
yellow = (245, 245, 66)
blue = (0, 0, 255)
cyan = (0, 255, 255)

clock = pygame.time.Clock()
moves = []
attack = []
myfont = pygame.font.SysFont("Comic Sans MS", 30)

cooldown = 0.1
debouncing = time.time()
SELECTED = None

iut = iuten.Iuten()

def fcolor(peca):
    if peca.islower() and TEAM == 0 or peca.isupper() and TEAM == 1:
        return black
    return red

def color(x, y):
    if (x,y) in moves:
        return green
    elif (x,y) in attack:
        return yellow
    elif iut.lastMove!= None and (x,y) in iut.lastMove:
        return cyan
    elif (x,y) in [iut.TORRE1,iut.TORRE2]:
        return blue
    elif (x,y) in [iut.TRONO1,iut.TRONO2]:
        return red
    return white


run = True

NUM_PLAYERS = 0

# VC Começa
TEAM = 1 - iut.CURPLAYER

BOT1_RND = 0
BOT1_DEPTH = 2

BOT2_RND = 0
BOT2_DEPTH = 2



##############################################################

def sillyAI(team, depth, rnd):
    coin = random()
    if iut.CURPLAYER == team and not iut.finished:
        if rnd >= coin:
            move = iut.IneffectiveChoice(team, depth)
        else:
            move = iut.bogoSillyIneffectiveChoice(team, True)
        print(move, team, "random" if rnd < coin else "minimax")

        if move != None:
            iut.move(move[0],move[1],team, move[2])

class Silly_Thread(threading.Thread):
    def __init__(self, name, team, fun, depth, intelect):
        threading.Thread.__init__(self)
        self.name = name
        self.team = team
        self.intelect = intelect
        self.fun = fun
        self.depth = depth
        self.killed = False

    def run(self):
        global iut     
        while not self.killed:
            self.fun(self.team, self.depth, self.intelect)
        

    def kill(self):
        self.killed = True


a = Silly_Thread("IA", 1 - TEAM, sillyAI, BOT1_DEPTH, 1 - BOT1_RND)
b = Silly_Thread("IA_2", TEAM, sillyAI, BOT2_DEPTH, 1 - BOT2_RND)

if NUM_PLAYERS < 2:
    a.start()
if NUM_PLAYERS == 0:
    b.start()
partidas = [0,0,0]
###############################################################
def updateCimiterio(cemiterio):
    rect = pygame.Rect(0, 0, 4*(tile_width + margin) , 9*(tile_height+ margin))
    pygame.draw.rect(win, black, rect)
    rect = pygame.Rect(13*(tile_width + margin), 0, 4*(tile_width + margin) , 9*(tile_height+ margin))
    pygame.draw.rect(win, black, rect)

    cemi_1_list = list(filter(lambda e: not e.islower(), cemiterio))
    cemi_2_list = list(filter(lambda e: e.islower(), cemiterio))
    cont = 0
    x = 0
    for i in range(len(cemi_1_list)):
        peca = cemi_1_list[i]
        if sprite[peca] == None:
            sprite[peca] = sprites(peca)
        win.blit(sprite[peca], (x +(tile_width + margin) * (cont %4), cont//4 * (tile_height + margin)))
        cont += 1 

    x = (tile_height + margin) * 13
    cont = 0
    for i in range(len(cemi_2_list)):
        peca = cemi_2_list[i]
        if sprite[peca] == None:
            sprite[peca] = sprites(peca)
        win.blit(sprite[peca], (x + (tile_width + margin) * (cont %4), cont//4 * (tile_height + margin)))
        cont += 1

cemiterio = []
rowsSaved = [[],[],[],[],[],[],[],[],[],[],[]]
lastMove = (0,0)
quit = False
for i in range(nPartidas):
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                iut.finished = True
                run = False
                quit = True
        

        y = margin  
        for row in range(11):
            x = 4*(tile_width+margin)
            # TODO melhorar o render
            # if str(iut.table[row+1]) != str(rowsSaved[row]) or row == lastMove[0]:
            #     if iut.lastMove and str(lastMove) != str(iut.lastMove):
            #         lastMove = copy(iut.lastMove)
                # rowsSaved[row] = [*iut.table[row+1]]
            for column in range(9):
                rect = pygame.Rect(x, y, tile_width, tile_height)
                pygame.draw.rect(win, color(column+1,row+1), rect)
                peca = iut.table[row+1][column+1]
                if peca != '_':
                    imagem = sprite[peca]
                    if sprite[peca] == None:
                        sprite[peca] = sprites(peca)
                    win.blit(sprite[peca], (x, y))
                x += tile_width + margin
            y += tile_height + margin



        if str(cemiterio) != str(iut.cemiterio):
            cemiterio = copy(iut.cemiterio)
            
            updateCimiterio(cemiterio)

        mouse = pygame.mouse.get_pressed()
        if iut.finished:
            break
        if mouse[0] and (time.time() - debouncing) > cooldown:
            print(iut.evaluateState(iut),iut.cemiterio, cemiterio)
            
            debouncing = time.time()
            pos = pygame.mouse.get_pos()
            curx = pos[0]//(tile_width+margin) - 4
            cury = pos[1]//(tile_height+margin)
            if color(curx+1, cury+1) == green and not iut.finished:
                iut.move(SELECTED, (curx+1, cury+1), TEAM, 'm')
                moves = []
            if color(curx+1, cury+1) == yellow and not iut.finished:
                iut.move(SELECTED, (curx+1, cury+1), TEAM, 's')
                moves = []
                attack = []
            elif not iut.finished:
                result = iut.checkMoves((curx+1,cury+1), TEAM)
                moves = result[0]
                attack = result[1]
                SELECTED = (curx+1, cury+1)
            if NUM_PLAYERS == 2:
                TEAM = iut.CURPLAYER
        elif mouse[2] and (time.time() - debouncing) > cooldown:
            print(f'{iut.evaluateState(iut)} {iut.CURPLAYER}')
            debouncing = time.time()
            pos = pygame.mouse.get_pos()
            curx = pos[0]//(tile_width+margin) - 4
            cury = pos[1]//(tile_height+margin)
            result = iut.checkMoves((curx+1,cury+1), TEAM)
            moves = []
            attack = result[1]
            SELECTED = (curx+1, cury+1)
            if NUM_PLAYERS == 2:
                TEAM = iut.CURPLAYER
        keys=pygame.key.get_pressed()
        if keys:
            if keys[pygame.K_r]:
                iut.restart()
        pygame.display.update()
    run = True
    ganhador = iut.gameover()
    time.sleep(1)
    partidas[ganhador] += 1
    iut.restart()
    if quit:
        break
    
a.kill()
b.kill()
print(partidas)
pygame.quit()
