# IUTEN

Implementação do jogo de tabuleiro Iuten desenvolvido pelo PET-BCC UFSCar em
python.


## Instalação e criação do virtualenv
```bash
pip install virtualenv
virtualenv .venv
```
## Ativando o ambiente virtual
### Windows
```bash
source .venv/Scripts/activate
```
### Linux
```bash
source .venv/bin/activate
```

## Instalação das dependências

Após ativar o ambiente virtual:

```bash
pip install -r requirements.txt
```

## Variáveis de jogo

No game.py você poderá encontrar as seguintes variáveis

```py
# Número de partidas
nPartidas = 10

# Número de jogadores para a rodada
# 0: BOT1 vs BOT2
# 1: Player vs BOT1
# 2: Player vs Player
NUM_PLAYERS = 1

# DEPTH é a profundidade do minimax
# RND é um valor de 0 a 1 que corresponde as jogadas não-minimax
# 1 = minimax desativado, algoritmo aleatório + guloso
# 0 = todas as jogadas são minimax 

BOT1_RND = 0
BOT1_DEPTH = 2

BOT2_RND = 0
BOT2_DEPTH = 2
````
