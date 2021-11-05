
import pygame
import time
import iuten 
import threading
c = threading.Condition()


pygame.init()


tile_width = 30
tile_height = 30
margin = 8 
win = pygame.display.set_mode(((tile_width+margin)*9, (tile_height+margin)*11))
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
yellow = (245, 245, 66)
blue = (0, 0, 255)
clock = pygame.time.Clock()

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
    elif (x,y) in [iut.TORRE1,iut.TORRE2]:
        return blue
    elif (x,y) in [iut.TRONO1,iut.TRONO2]:
        return red
    return white

moves = []
attack = []
run = True
myfont = pygame.font.SysFont("Comic Sans MS", 30)
# TEAM = iut.CURPLAYER
TEAM = 0


##############################################################

def sillyAI(team):
    while not iut.finished:
        time.sleep(0.1)
        if iut.CURPLAYER == team:
            move = iut.bogoSillyIneffectiveChoice(team)
            if move != None:
                iut.move(move[0],move[1],team, move[2])
            else:
                iut.printTable(iut.table)
                break

class Silly_Thread(threading.Thread):
    def __init__(self, name, team, fun):
        threading.Thread.__init__(self)
        self.name = name
        self.team = team
        self.fun = fun
    def run(self):
        global iut     
        self.fun(self.team)

# a = Silly_Thread("IA", 0, sillyAI)
b = Silly_Thread("IA_2", 1, sillyAI)
# a.start()
b.start()
###############################################################


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            iut.finished = True
            run = False

    x = margin
    for column in range(9):
        y = margin
        for row in range(11):
            rect = pygame.Rect(x, y, tile_width, tile_height)
            pygame.draw.rect(win, color(column+1,row+2), rect)
            peca = iut.table[row+2][column+1]
            if peca != '_':
                label = myfont.render(peca, 1, fcolor(peca))
                win.blit(label, (x+8, y-8))
            y = y + tile_height + margin
        x = x + tile_width + margin
    mouse = pygame.mouse.get_pressed()
    if mouse[0] and (time.time() - debouncing) > cooldown:
        debouncing = time.time()
        pos = pygame.mouse.get_pos()
        curx = pos[0]//(tile_width+margin)
        cury = pos[1]//(tile_height+margin)
        if color(curx+1, cury+2) == green and not iut.finished:
            iut.move(SELECTED, (curx+1, cury+2), TEAM, 'm')
            moves = []
        if color(curx+1, cury+2) == yellow and not iut.finished:
            iut.move(SELECTED, (curx+1, cury+2), TEAM, 's')
            moves = []
            attack = []
        elif not iut.finished:
            result = iut.checkMoves((curx+1,cury+2), TEAM)
            moves = result[0]
            attack = result[1]
            SELECTED = (curx+1, cury+2)
        # TEAM = iut.CURPLAYER
    elif mouse[2] and (time.time() - debouncing) > cooldown:
        debouncing = time.time()
        pos = pygame.mouse.get_pos()
        curx = pos[0]//(tile_width+margin)
        cury = pos[1]//(tile_height+margin)
        result = iut.checkMoves((curx+1,cury+2), TEAM)
        attack = result[1]
        SELECTED = (curx+1, cury+2)
        # TEAM = iut.CURPLAYER
    pygame.display.update()

pygame.quit()

