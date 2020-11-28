from dlgo import agent
from dlgo.agent import naive
from dlgo import goboard_slow as goboard
from dlgo import gotypes
from dlgo.utils import print_board, print_move, point_from_coords
import time
import os


def main():
    board_size = 9
    game = goboard.GameState.new_game(board_size)
    bot = agent.naive.RandomBot()

    while not game.is_over():
        os.system('cls' if os.name == 'nt' else 'clear')
        print_board(game.board)
        if game.next_player == gotypes.Player.black:
            human_move = input('-- ')
            point = point_from_coords(human_move.strip())
            move = goboard.Move.play(point)
        else:
            move = bot.select_move(game)
        print_move(game.next_player, move)
        game = game.apply_move(move)


if __name__ == '__main__':
    main()
