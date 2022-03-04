from collections import defaultdict
from random import randint, shuffle
import math
import copy
import time
class Iuten():
    def __init__(self):
        self.restart()

    def restart(self):
        self.table = []

        self.s = '2p1d1p1_1p1d2p1a1_1e1p1c1p1e1_1aF_F_F_F_3_1A1_1E1P1C1P1E1_1A2P1D1P1_1P1D2P'

        self.TORRE1 = (5,4)
        self.TORRE2 = (5,8)
        self.TRONO1 = (5,1)
        self.TRONO2 = (5,11)
        self.ELEFANTES1 = 0
        self.ELEFANTES2 = 0
        self.CURPLAYER = 0
        self.pqtd = 8
        self.Pqtd = 8
        self.SPECIALROUND = False
        self.finished = False
        self.types = defaultdict(int)
        self.types['s'] = 1
        self.table = self.codToTable(self.s)
        self.lastMove = None

    # TIME 0 = minusculas
    # TIME 1 = maiusculas

    def toHex(self, n):
        if n > 9:
            return chr(n + 55)
        else:
            return str(n)

    def toDec(self, n):
        n = '0x'+n
        return int(n,16)

    def tableToCod(self, t = None):
        if t == None:
            t = self.table

        # ultima posicao de no-op
        op = 0
        idx = 0
        result = ''
        lastc = 'n'
        pos = op
        linha = 0
        for i in range(11):
            for j in range(9):
                if t[linha][pos] == lastc and idx < 15:
                    idx += 1
                else:
                    result += self.toHex(idx)+lastc
                    idx = 1
                    lastc = t[linha][pos]
                pos += 1
            pos = 0
            linha += 1

        return result + self.toHex(idx)+lastc

    def codToTable(self, t):
        m = []
        l = list(11*'n')
        m.append(l)
        l = ['n']
        idx = 0
        for i in range(len(t)//2):
            n = self.toDec(t[2*i])
            c = t[2*i + 1]
            while n != 0:
                aux = min(9 - idx, n)
                l.extend(aux*c)
                idx += aux
                n -= aux
                if idx == 9:
                    idx = 0
                    l.extend('n')
                    m.append(l)
                    l = ['n']
        l.extend(10*'n')
        m.append(l)
        return m

    def printTable(self, t = None, n = False):
        if t == None:
            t = self.table
        for i in t:
            for j in i:
                if n or j != 'n':
                    print(j, end=' ')
            print()

    def ocupavel(self ,p, team):
        cur = self.table[p[1]][p[0]]

        if cur == 'n':
            return False
        if cur == '_':
            return True
        if team == 0 and cur.isalpha() and cur.isupper():
            return True
        if team == 1 and cur.isalpha() and cur.islower():
            return True
        return False

    # posicao, direcao, tamanho do feixe, time
    def raioLaser(self, p, dir, tam, team, shot = False):
        incx = 1
        incy = 1
        count = 0
        moves = []
        curx = p[0]
        cury = p[1]
        
        # vertical cima
        if dir == 1:
            incx = 0
            incy = -1
        # vertical baixo
        elif dir == 2:
            incx = 0
            incy = 1
        # horizontal esquerda
        elif dir == 3:
            incx = -1
            incy = 0
        # horizontal direira
        elif dir == 4:
            incx = 1
            incy = 0
        # diagonal cimaesquerda -> baixodireita
        elif dir == 5:
            incx = 1
            incy = 1
        # diagonal cimaedireita -> baixoesquerda
        elif dir == 6:
            incx = -1
            incy = 1
        # diagonal baixodireita -> cimaesquerda
        elif dir == 7:
            incx = -1
            incy = -1
        # diagonal baixoesquerda -> cimaedireita
        elif dir == 8:
            incx = 1
            incy = -1

        while True:
            curx += incx
            cury += incy
            possivel = self.ocupavel((curx, cury),team)
            curPos = self.table[cury][curx]
            
            if not possivel or count >= tam:
                if len(moves) > 0 and shot:
                    if curPos != 'n' and (curPos.isupper() and team == 0 or
                     curPos.islower() and team == 1):
                        moves = [moves[-1]]
                    else:
                        moves = []
                break
            elif possivel and (curPos != '_' or (curx, cury) == self.TORRE1 
                or (curx, cury) == self.TORRE2):
                moves.append((curx, cury))
                if shot:
                    moves = [moves[-1]]
                break



            count += 1
            moves.append((curx, cury))
        return moves

    def adjacente(self, p, team):
        moves = []
        moves.extend(self.raioLaser(p,1,1,team))
        moves.extend(self.raioLaser(p,2,1,team))
        moves.extend(self.raioLaser(p,3,1,team))
        moves.extend(self.raioLaser(p,4,1,team))
        moves.extend(self.raioLaser(p,5,1,team))
        moves.extend(self.raioLaser(p,6,1,team))
        moves.extend(self.raioLaser(p,7,1,team))
        moves.extend(self.raioLaser(p,8,1,team))
        return moves

    def peao(self, p, team):
        return (self.adjacente(p, team), [])

    def druida(self, p, team):
        moves = []
        moves.extend(self.raioLaser(p, 1, 2, team))
        moves.extend(self.raioLaser(p, 2, 2, team))
        moves.extend(self.raioLaser(p, 3, 2, team))
        moves.extend(self.raioLaser(p, 4, 2, team))

        ele = []
        if (team == 0 and self.ELEFANTES1 > 0 or team == 1 and self.ELEFANTES2 > 0):
            ele =  self.adjacente(p, team)

        return (moves, ele)

    def arqueiro(self, p, team):
        moves = []
        if p == self.TORRE1 or p == self.TORRE2:
            moves.extend(self.raioLaser(p,5,10,team,True))
            moves.extend(self.raioLaser(p,6,10,team,True))
            moves.extend(self.raioLaser(p,7,10,team,True))
            moves.extend(self.raioLaser(p,8,10,team,True))
            return (self.adjacente(p, team), moves)
        else:
            moves.extend(self.raioLaser(p,5,2,team))
            moves.extend(self.raioLaser(p,6,2,team))
            moves.extend(self.raioLaser(p,7,2,team))
            moves.extend(self.raioLaser(p,8,2,team))
            moves.extend(self.raioLaser(p,3,1,team))
            moves.extend(self.raioLaser(p,4,1,team))

        return (moves, [])

    def elefante(self, p, team):
        moves = []
        if team == 0:
            moves.extend(self.raioLaser(p, 2, 1, team))
            moves.extend(self.raioLaser(p, 5, 1, team))
            moves.extend(self.raioLaser(p, 6, 1, team))
        if team == 1:
            moves.extend(self.raioLaser(p, 1, 1, team))
            moves.extend(self.raioLaser(p, 7, 1, team))
            moves.extend(self.raioLaser(p, 8, 1, team))
        return (moves, [])

    def separador(self, lista, team):
        if len(lista) > 3:
            if self.isMy(lista[-1], abs(team - 1)):
                return [lista[:-1], [lista[-1]]]
            else:  
                return [lista, []]
        else:
            return [lista, []]
        
    def cavaleiro(self, p, team, bonus = False):
        moves = []
        special = []
        if bonus:
            return (self.adjacente(p, team), [])

        aux = self.separador(self.raioLaser(p, 1, 10, team), team)
        moves.extend(aux[0])
        special.extend(aux[1])

        aux = self.separador(self.raioLaser(p, 2, 10, team), team)
        moves.extend(aux[0])
        special.extend(aux[1])

        aux = self.separador(self.raioLaser(p, 3, 8, team), team)
        moves.extend(aux[0])
        special.extend(aux[1])

        aux = self.separador(self.raioLaser(p, 4, 8, team), team)
        moves.extend(aux[0])
        special.extend(aux[1])

        return (moves, special)

    # Quais são os tipos de movimentos?  (nomrais :{mover, capturar},
    # especiais: {atirar, invocar, pular})

    # As posicoes são (x,y) com base no plano cartesiano, logo pra acessar a
    # posicao deve-se fazer table[y][x]
    def isMy(self, p, team, f = lambda e: True):
        peca = self.table[p[1]][p[0]]
        a = (team == 0 and peca.islower() and peca.isalpha() and peca != 'n')
        b = (team == 1 and peca.isupper() and peca.isalpha())
        return f(peca) and (a or b)

    def checkMoves(self, p, team):

        if team != self.CURPLAYER:
            # print(f'Não é o seu turno {self.CURPLAYER} {team}')
            return ([],[])


        if self.finished:
            print('O JOGO ACABOU')
            return 
        

        peca = self.table[p[1]][p[0]]
        if peca == '_':
            return ([], [])


        if not self.isMy(p, team):
            return([], [])
        
        peca = peca.lower()

        if self.isMy(self.TORRE1, team, lambda e: e.lower() != 'a'):
            if p != self.TORRE1:
                return ([], [])
            else:
                return (self.adjacente(p, team),[])
                
        if self.isMy(self.TORRE2, team, lambda e: e.lower() != 'a'):
            if p != self.TORRE2:
                return ([], [])
            else:
                return (self.adjacente(p, team),[])

        if self.SPECIALROUND:
            if peca != 'c':
                return ([],[])
            else: 
                return self.cavaleiro(p, team, True)
            
        if peca == 'p':
            return self.peao(p, team)
        elif peca == 'e':
            return self.elefante(p, team)
        elif peca == 'd':
            return self.druida(p, team)
        elif peca == 'c':
            return self.cavaleiro(p, team)
        elif peca == 'a':
            return self.arqueiro(p, team)
        else:
            return ([],[])

    def gameover(self):
        self.finished = True
        if self.table[self.TRONO1[1]][self.TRONO1[0]] == 'P':
            print('P chegou no trono')
            return 2
        elif self.table[self.TRONO2[1]][self.TRONO2[0]] == 'p':
            print('p chegou no trono')
            return 1
        elif self.pqtd == 0:
            print('todos p morreram')
            return 2
        elif self.Pqtd == 0:
            print('todos P morreram')
            return 1
        self.finished = False
        return 0

    def move(self, p, np, team, type, trustable = False):
        next = 0 if self.CURPLAYER == 1 else 1
        if team != self.CURPLAYER:
            # print('Não é o seu turno')
            return
        if self.finished:
            print('O JOGO ACABOU')
            return

        # Evitar checagem se ja tiver checado
        if not trustable:
            possible = self.checkMoves(p, team)
        if trustable or np in possible[self.types[type]]:
            oldPiece = self.table[np[1]][np[0]]
            piece = self.table[p[1]][p[0]]
            newpos = (np[0], np[1])

            if piece.lower() == 'd' and self.types[type] == 1:
                # Invoca elefante
                if team == 0:
                    self.ELEFANTES1 -= 1
                    self.table[np[1]][np[0]] = 'e' 
                else:
                    self.ELEFANTES2 -= 1
                    self.table[np[1]][np[0]] = 'E' 
            elif piece.lower() == 'a' and self.types[type] == 1:
                # Atira
                self.table[np[1]][np[0]] = '_'
            else:
                # movimento default
                self.table[np[1]][np[0]] = self.table[p[1]][p[0]]
                self.table[p[1]][p[0]] = '_'

            diff = abs(np[1] - p[1]) + abs(np[0] - p[0])

            # Checagem se o jogo acabou
            if oldPiece.lower() == 'p' or piece.lower() == 'p':
                if 'p' == oldPiece:
                    self.pqtd -= 1
                elif 'P' == oldPiece:
                    self.Pqtd -= 1
                self.gameover()

            if oldPiece.lower() == 'e':
                if oldPiece.isupper():
                    self.ELEFANTES1 += 1
                else:
                    self.ELEFANTES2 += 1

            # Caso especial do cavaleiro
            if piece.lower() == 'c' and self.SPECIALROUND:
                self.SPECIALROUND = False
            elif piece.lower() == 'c' and not self.SPECIALROUND and oldPiece != '_' and diff >= 3 and not (newpos in [self.TORRE1, self.TORRE2]):
                self.SPECIALROUND = True
                next = self.CURPLAYER
            self.CURPLAYER = next
                
        else:
            print(f'algo deu errado...{p}=>{np}\n{type}\n{possible[self.types[0]]}\n{possible[self.types[1]]}')
        self.lastMove = (p, np, team, type)
        
    def rand(self,b):
        return 0 if 1 == b  else randint(0, b-1)

    def values(self, e):
        peca = (self.table[e[1]][e[0]]).lower()
        valores = ['c','p','d','a','e','_']
        if peca in valores:
            return valores.index(peca)
        else:
            return 10 

    def bogoSillyIneffectiveChoice(self, team, teste=False):
        moves = []
        special = []
        escolhido = None
        escolhas = []
        esperto = False
        trono = self.TRONO1 if team == 1 else self.TRONO2
        for i in range(1,10):
            for j in range(1,13):
                aux = self.checkMoves((i, j), team)
                if aux != None:
                    if len(aux[0]) > 0:
                        aux[0].sort(key=self.values)
                        alvo = self.table[aux[0][0][1]][aux[0][0][0]]
                        peca = self.table[j][i]
                        
                        if peca.lower() == 'p' and trono in aux[0]:
                            esperto = True
                            moves.insert(0, ((i, j), [trono], 'm'))
                        else:
                            if alvo != '_':
                                esperto = True
                                moves.insert(0, ((i, j), aux[0], 'm'))
                            else:
                                moves.append(((i, j), aux[0], 'm'))
                    if len(aux[1]) > 0:
                        special.append(((i, j), aux[1], 's'))
        
        
        if len(special) > 0:
            escolhas = special[self.rand(len(special))]
        elif len(moves) > 0 and esperto:
            escolhas = moves[0]
        elif len(moves) > 0:
            escolhas = moves[self.rand(len(moves))]
        else:
            return None

        pos = self.table[escolhas[1][0][1]][escolhas[1][0][0]]
        if teste and pos != '_':
            escolhido = ((escolhas[0]), escolhas[1][0], escolhas[2])
        else:
            escolhido = ((escolhas[0]), escolhas[1][self.rand(len(escolhas[1]))], escolhas[2])

        return escolhido

    def IneffectiveChoice(self, team, teste=False):
        if team != self.CURPLAYER:
            return None
        move = self.alphabeta(self, 3, - math.inf, math.inf, None ,True)
        l = ['m', 's']
        return (move[0],move[1],l[move[3]])


    def getState(self,i,j, move, t):
        newState = copy.deepcopy(self) 
        newState.move((i, j), move, self.CURPLAYER, t, True)
        return newState

    def getAllStates(self):
            moves = []
            for i in range(1,10):
                for j in range(1,13):
                    aux = self.checkMoves((i, j), self.CURPLAYER)
                    if aux != None:
                        moves.extend(list(map(lambda e: self.getState(i,j,e,0), aux[0])))
                        moves.extend(list(map(lambda e: self.getState(i,j,e,1), aux[1])))
            return moves

    # depth != 0
    def alphabeta(self, node, depth, alpha, beta, t, root = False):
        aux = node
        maximizingPlayer = node.CURPLAYER != 0
        if depth == 0 or (t is not None and t <= time.time()):
            return self.evaluateState(node)
        elif node.finished:
            return node.gameover() - 1

        if maximizingPlayer:
            value = - math.inf
            children = node.getAllStates()
            children.sort(key=self.evaluateState, reverse=True)
            for child in children:
                oldv = value
                value = max(value, self.alphabeta(child, depth -1, alpha, beta, t))
                alpha = max(alpha, value)
                if value >= beta:
                    break #(* beta cutoff *)
                if oldv != value:
                    aux = child
            if not root:
                return value
            else:
                return aux.lastMove
        else:
            value = math.inf
            children = node.getAllStates()
            children.sort(key=self.evaluateState)
            for child in children:
                oldv = value
                value = min(value, self.alphabeta(child, depth -1, alpha, beta, t))
                beta = min(beta, value)
                if value <= alpha:
                    break #(* alpha cutoff *)
                if oldv != value:
                    aux = child            
            if not root:
                return value
            else:
                return aux.lastMove

    def evaluateState(self, node):
        if not node.finished:
            soma = 0
            for i in range(1,10):
                for j in range(1,13):
                    if node.isMy((i,j),1):
                        soma += 0.00002 * (13-j)
                    elif node.isMy((i,j),0):
                        soma -=  0.00001 * (j +1)
            if node.Pqtd >= node.pqtd:
                soma += 0.1
            soma += node.Pqtd * 0.04

            return soma
        else:
            return node.gameover() -1
