__all__ = [
    'Agent',
]


# tag::agent[]
class Agent:
    """
    Main go bot class
    """
    def __init__(self):
        pass

    def select_move(self, game_state):
        """
        :param game_state: current game state
        :return: move
        """
        raise NotImplementedError()
# end::agent[]

    def diagnostics(self):
        return {}
