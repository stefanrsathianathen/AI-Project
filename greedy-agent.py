import board as b
from random import randrange
from copy import deepcopy


class Board2(b.Board):
    # additional methods
    def value_board(self, team):
        """ determines how favourable this board state is """
        # TODO for a particular team?
        # TODO: very basic: just count number of pieces in each team
        # TODO: consider each piece's distance to middle

        # simple version: just count number of pieces
        ally = team
        enemy = Board2.get_opponent_team(ally)
        counts = {ally: 0, enemy: 0}
        for piece in self.pieces:
            if piece is not None:
                counts[piece['team']] += 1

        return counts[ally] - counts[enemy]

    # TODO define a function that returns distance of piece to middle


class Player(object):
    """
    An agent that can play Watch Your Back.
    This agent looks at the next state caused by each action to pick an action
    """

    def __init__(self, colour):
        """
        :param colour: either 'white' or 'black'
        """
        # set up a new board
        self.board = Board2()
        # set up team allegiances
        self.team = b.BLACK
        if colour == 'white':
            self.team = b.WHITE
        elif colour == 'black':
            self.team = b.BLACK
        else:
            raise ValueError("colour must be 'white' or 'black'")
        self.enemy_team = b.Board.get_opponent_team(self.team)

    def action(self, turns):
        """
        called by the referee to request an action from the player

        :param turns: number of turns that have taken place
            since start of current game phase
        :return: next action
        """
        assert turns == self.board.turn_count
        # gets list of all actions
        actions = self.board.get_all_actions(self.team)
        our_action = None  # will forfeit turn if no actions

        # TODO calculate the board state after applying each action
        # copy the board
        # TODO consider undoing or reusing instead of instantiating more boards
        next_values = [0] * len(actions)
        best_value = -999
        for i in range(len(next_values)):
            # calculate how favourable each next state is
            board = deepcopy(self.board)
            board.do_action(actions[i], self.team)
            next_values[i] = board.value_board(self.team)
            # and keep track of the best value
            best_value = max(best_value, next_values[i])

        # TODO pick among the best states
        # filter out non-favourable states
        best_actions = []
        for i in range(len(next_values)):
            if next_values[i] == best_value:
                best_actions.append(actions[i])

        print("best, len-best, len-all: ", best_value, len(best_actions), len(actions))
        if len(best_actions) > 0:
            # our_action = actions[0]  # choose first action
            # choose random action
            our_action = best_actions[randrange(0, len(best_actions))]

        # Update the board with our action
        self.board.do_action(our_action, self.team)

        return our_action

    def update(self, action):
        """
        Inform player about opponent's most recent move

        :param action: opponent's action
        :return: Nothing
        """
        # Update our board with the opponent's action
        self.board.do_action(action, self.enemy_team)
