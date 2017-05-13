#executable file for game
from game_engine import Game
game = Game()
while len(game.players) > 1:
    game.round