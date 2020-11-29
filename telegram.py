import telebot
from hidden2 import bot
from hidden2 import TOKEN
# tag::play_against_your_bot[]
from dlgo import agent
from dlgo import goboard_slow as goboard
from dlgo import gotypes
from dlgo.utils import print_board, print_move, point_from_coords
from six.moves import input
import os
from flask import Flask, request


server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, наберите /play для запуска партии')


board_size = None
game = None
xbot = None


@bot.message_handler(commands=['play'])
def play_message(message):
    global board_size
    global game
    global xbot

    board_size = 9
    game = goboard.GameState.new_game(board_size)
    xbot = agent.RandomBot()
    print_board(game.board)
    bot.send_message(message.chat.id, print_board(game.board))
    bot.send_message(message.chat.id, 'Сделай ход: (Например, A1)')


@bot.message_handler(content_types=['text'])
def play_message(message):
    global board_size
    global game
    global xbot

    try:
        human_move = message.text.upper()
        point = point_from_coords(human_move.strip())
        move = goboard.Move.play(point)

        game = game.apply_move(move)

        bot.send_message(message.chat.id, print_move(game.next_player, move))
        bot.send_message(message.chat.id, print_board(game.board))

        move = xbot.select_move(game)
        game = game.apply_move(move)

        bot.send_message(message.chat.id, print_move(game.next_player, move))
        bot.send_message(message.chat.id, print_board(game.board))

        bot.send_message(message.chat.id, 'Сделай ход: (Например, A1)')

    except Exception:
        bot.send_message(message.chat.id, 'Неразумный ввод =)')


"""
    while not game.is_over():
        print(chr(27) + "[2J")
        print_board(game.board)
        if game.next_player == gotypes.Player.black:
            human_move = input('-- ')
            point = point_from_coords(human_move.strip())
            move = goboard.Move.play(point)
        else:
            move = bot.select_move(game)
        print_move(game.next_player, move)
        game = game.apply_move(move)
"""

bot.polling()


if __name__ == '__main__':
    server.debug = True
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))