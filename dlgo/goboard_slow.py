from dlgo.gotypes import Player
import copy


class Move:
    def __init__(self, point=None, is_pass=False, is_resign=False):
        """
        :param point: point
        :param is_pass: pass
        :param is_resign: exit game
        """
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point):
        """
        :param point: point
        :return: initialized game
        """
        return Move(point=point)

    @classmethod
    def pass_turn(cls):
        """
        :return: passed game
        """
        return Move(is_pass=True)

    @classmethod
    def resign(cls):
        """
        :return: resigned game
        """
        return Move(is_resign=True)


class GoString:
    def __init__(self, color, stones, liberties):
        """
        :param color: color of stones
        :param stones: stones
        :param liberties: liberties
        """
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)

    def remove_liberty(self, point):
        """
        :param point: point
        :return: deleted point from liberties
        """
        self.liberties.remove(point)

    def add_liberty(self, point):
        """
        :param point: point
        :return: added point from liberties
        """
        self.liberties.add(point)

    def merge_with(self, go_string):
        """
        :param go_string: new string of stones
        :return: merged stones list
        """
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | go_string.liberties) - combined_stones
        )

    @property
    def num_liberties(self):
        """
        :return: num of liberties
        """
        return len(self.liberties)

    def __eq__(self, other):
        """
        :param other: other string
        :return: compare strings
        """
        return isinstance(other, GoString) and \
            self.color == other.color and \
            self.stones == other.stones and \
            self.liberties == other.liberties


class Board:
    def __init__(self, num_rows, num_cols):
        """
        :param num_rows: rows num in board
        :param num_cols: cols num in board
        :param grid: board grid
        """
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}

    def is_on_grid(self, point):
        """
        :param point: point
        :return: is point on grid
        """
        return 1 <= point.row <= self.num_rows and \
            1 <= point.col <= self.num_cols

    def get(self, point):
        """
        :param point: point
        :return: string color
        """
        string = self._grid.get(point)
        if string is None:
            return None
        return string.color

    def get_go_string(self, point):
        """
        :param point: point
        :return: return string
        """
        string = self._grid.get(point)
        if string is None:
            return None
        return string

    def place_stone(self, player, point):
        """
        :param player: player
        :param point: point
        :return:
        """
        assert self.is_on_grid(point)  # if point on grid
        assert self._grid.get(point) is None  # if point not none
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = []
        for neighbor in point.neighbors():
            if not self.is_on_grid(neighbor):  # if neighbor out of grid
                continue
            neighbor_string = self._grid.get(neighbor)  # get neighbor stone
            if neighbor_string is None:  # if neighbor stone is none
                liberties.append(neighbor)
            elif neighbor_string.color == player:  # if neighbor stone is player
                if neighbor_string not in adjacent_same_color:  # if not in adjacent list
                    adjacent_same_color.append(neighbor_string)
            else:
                if neighbor_string not in adjacent_opposite_color:  # if neighbor stone is enemy
                    adjacent_opposite_color.append(neighbor_string)  # if not in adjacent list

        new_string = GoString(player, [point], liberties)

        for same_color_string in adjacent_same_color:
            new_string = new_string.merge_with(same_color_string)
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string
        for other_color_string in adjacent_opposite_color:
            other_color_string.remove_liberty(point)
        for other_color_string in adjacent_opposite_color:
            if other_color_string.num_liberties == 0:
                self._remove_string(other_color_string)

    def _remove_string(self, string):
        """
        :param string: string
        :return: removed string
        """
        for point in string.stones:
            for neighbor in point.neighbors():
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:
                    neighbor_string.add_liberty(point)
            self._grid[point] = None


class GameState:
    def __init__(self, board, next_player, previous, move):
        """
        :param board: board
        :param next_player: player
        :param previous: previous
        :param move: move
        """
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        self.last_move = move

    def apply_move(self, move):
        """
        :param move: move
        :return: game state with new move
        """
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
        else:
            next_board = self.board

        return GameState(next_board, self.next_player.other, self, move)

    @classmethod
    def new_game(cls, board_size):
        """
        :param board_size: board_size
        :return: new game state
        """
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(*board_size)
        return GameState(board, Player.black, None, None)

    def is_over(self):
        """
        :return: check is game over
        """
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        return self.last_move.is_pass and second_last_move.is_pass

    def is_move_self_capture(self, player, move):
        """
        :param player: player
        :param move: move
        :return: is move self capture
        """
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        new_string = next_board.get_go_string(move.point)
        return new_string.num_liberties == 0

    @property
    def situation(self):
        """
        :return: situation data
        """
        return self.next_player, self.board

    def does_move_violate_ko(self, player, move):
        """
        :param player: player
        :param move: move
        :return: does move violate ko
        """
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        next_situation = (player.other, next_board)
        past_state = self.previous_state
        while past_state is not None:
            if past_state.situation == next_situation:
                return True
            past_state = past_state.previous_state
        return False

    def is_valid_move(self, move):
        """
        :param move: move
        :return: is move valid
        """
        if self.is_over():
            return False
        if move.is_pass or move.is_resign:
            return True
        return (
                self.board.get(move.point) is None and
                not self.is_move_self_capture(self.next_player, move) and
                not self.does_move_violate_ko(self.next_player, move)
        )
