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
        return 1 <= point.row <= self.num_rows and 1 <= point.col <= self.num_cols

    def get(self, point):
        """
        :param point: point
        :return: string color
        """
        string = self._grid.get(point)
        if string is None:
            return None
        return string.color

    def get_got_string(self, point):
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
        assert self.is_on_grid(point)   # if point on grid
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
