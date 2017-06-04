#executable file for game
from poker_cards.game_engine import Game
game = Game()
while len(game.players) > 1:
    game.round()