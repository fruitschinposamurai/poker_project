# executable file for game
from poker_cards.game_engine import Game
import pdb
game = Game(2)
#serverSocket = Game_Socket(game)
while len(game.players) > 1:
    game.round()