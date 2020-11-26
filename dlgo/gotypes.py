from collections import namedtuple
import enum


class Player(enum.Enum):
    black = 1
    white = 2

    @property
    def other(self):
        """
        :return: color of other player
        """
        return Player.black if self == Player.white else Player.white


class Point(namedtuple('Point', 'row col')):
    def neighbors(self):
        """
        :return: point neighbors
        """
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),
        ]


if __name__ == "__main__":
    player = Player(1)
    print(player)
    print(player.other)
