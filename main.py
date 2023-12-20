from graphics import *
from chess import *
import time
import random

def main():
    pplayer1 = HumanPlayer("white")
    pplayer2 = ComputerPlayer("black")
    game = Game(pplayer1, pplayer2)
    game.start()

if __name__ == "__main__":
    main()