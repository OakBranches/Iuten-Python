from collections import defaultdict
from random import randint

class Iuten():
    def __init__(self):
        self.table = []

        self.s = '2p1d1p1_1p1d2p1a1_1e1p1c1p1e1_1aF_F_F_F_3_1A1_1E1P1C1P1E1_1A2P1D1P1_1P1D2P'

        self.TORRE1 = (5,5)
        self.TORRE2 = (5,9)
        self.TRONO1 = (5,2)
        self.TRONO2 = (5,12)
        self.ELEFANTES1 = 0
        self.ELEFANTES2 = 0
        self.CURPLAYER = 0
        self.SPECIALROUND = False
        self.finished = False
        self.types = defaultdict(int)
        self.types['s'] = 1
        self.table = self.codToTable(self.s)

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

    def tableToCod(self, t):
        # ultima posicao de no-op
        op = 23
        idx = 0
        result = ''
        lastc = t[op]
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
        l = list(11*'n')
        m.append(l)
        return m

    def printTable(self, t, n = False):
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
            
            
            #TODO Arrumar ataque especial do arqueiro
            
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

    def cavaleiro(self, p, team, bonus = False):
        moves = []
        if bonus:
            return (self.adjacente(p, team), [])
        moves.extend(self.raioLaser(p, 1, 10, team))
        moves.extend(self.raioLaser(p, 2, 10, team))
        moves.extend(self.raioLaser(p, 3, 8, team))
        moves.extend(self.raioLaser(p, 4, 8, team))
        return (moves, [])

    # Quais são os tipos de movimentos?  (nomrais :{mover, capturar},
    # especiais: {atirar, invocar})

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
            return 1
        elif self.table[self.TRONO2[1]][self.TRONO2[0]] == 'p':
            return 2
        elif sum(list(map(lambda e: e.count('p'), self.table))) == 0:
            return 1
        elif sum(list(map(lambda e: e.count('P'), self.table))) == 0:
            return 2
        self.finished = False
        return 0

    def move(self, p, np, team, type):
        next = 0 if self.CURPLAYER == 1 else 1
        if team != self.CURPLAYER:
            # print('Não é o seu turno')
            return
        if self.finished:
            print('O JOGO ACABOU')
            return


        possible = self.checkMoves(p, team)
        if np in possible[self.types[type]]:
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
            print(f'algo deu errado... {np}\n{possible[self.types[type]]}')

    # TODO implementar
    def process(self,comando):
        pass

    def rand(self,b):
        return 0 if 1 == b  else randint(0, b-1)

    def bogoSillyIneffectiveChoice(self, team):
        moves = []
        special = []
        escolhido = None
        escolhas = []
        for i in range(1,10):
            for j in range(2,13):
                aux = self.checkMoves((i, j), team)
                if aux != None:
                    if len(aux[0]) > 0:
                        moves.append(((i, j), aux[0], 'm'))
                    if len(aux[1]) > 0:
                        special.append(((i, j), aux[1], 's'))
        
        
    
        if len(special) > 0:
            escolhas = special[self.rand(len(special))]
        elif len(moves) > 0:
            escolhas = moves[self.rand(len(moves))]
        else:
            return None

        escolhido = ((escolhas[0]), escolhas[1][self.rand(len(escolhas[1]))], escolhas[2])
        return escolhido



