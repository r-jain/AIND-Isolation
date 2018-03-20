"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # Agressive game play with constant double weightage to negative of opponent moves
    return float(len(game.get_legal_moves(player)) - (2*len(game.get_legal_moves(game.get_opponent(player)))))

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    #raise NotImplementedError

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    num_my_moves = len(game.get_legal_moves(player))
    num_opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    num_total_available_moves = len(game.get_blank_spaces())
    num_total_initial_moves = game.width * game.height
    percent_remaining = num_total_available_moves/num_total_initial_moves

    # Dynamic scaled aggressive gameplay
    # Start with initial score based on my_moves 
    # Ramps up the agressive moves as game progresses 
    # Agression ramp based on weighted square of opponent moves up as % game complete increases 

    return (percent_remaining * num_my_moves) - ((1 - percent_remaining) * (num_opp_moves**2))

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    # raise NotImplementedError
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # return (my_moves - 2*opponent_moves) - (scaled  distance from center) 
    # Scaling factor {max((h-y)**2)  + max((w-x)**2) => 9+9 =18 * (1/2) => range(0,9)
    # Distance from center scaled for magnitude scale similar to that of (my_moves - opponent_moves) range(-8,8)
    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    return float(len(game.get_legal_moves(player)) - (2*len(game.get_legal_moves(game.get_opponent(player))))) - float(((h - y)**2 + (w - x)**2)*(1/2)) 


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=50.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        legal_moves = game.get_legal_moves()
        if not legal_moves:   
            best_move =  (-1, -1)
        else:
            best_move =  legal_moves[0]

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move
    
    def minimax(self, game, depth):
        #print('*** Enter Minimax ***')
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        def max_value(game, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            #print('*** Enter max_value *** depth:', depth)
            """ Return the value for a loss (-inf) if the game is over,
            otherwise return the maximum value over all legal child
            nodes.
            """
            if not bool(game.get_legal_moves()):
                # return utility value
                return game.utility(self)  
            
            # New conditional depth limit cutoff
            if depth <= 0:  # "==" could be used, but "<=" is safer 
                # self.score()` method for board evaluation
                return self.score(game, self)
            
            v = float("-inf")
            for m in game.get_legal_moves():
                # the depth should be decremented by 1 on each call
                v = max(v, min_value(game.forecast_move(m), depth - 1))
            #print('*** Exit max_value *** value:', v)
            return v

        def min_value(game, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            #print('*** Enter min_value *** depth:', depth)
            """ Return the value for a win (+inf) if the game is over,
            otherwise return the minimum value over all legal child
            nodes.
            """
            if not bool(game.get_legal_moves()):
                # return utility value
                return game.utility(self) 
            
            # New conditional depth limit cutoff
            if depth <= 0:  # "==" could be used, but "<=" is safer 
                #self.score()` method for board evaluation
                return self.score(game, self)
            
            v = float("inf")
            for m in game.get_legal_moves():
                # the depth should be decremented by 1 on each call
                v = min(v, max_value(game.forecast_move(m), depth - 1))
            #print('*** Exit min_value *** value:', v)
            return v


        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        #raise NotImplementedError
        
        """ Return the move along a branch of the game tree that
        has the best possible value.  A move is a pair of coordinates
        in (column, row) order corresponding to a legal move for
        the searching player.
        
        You can ignore the special case of calling this function
        from a terminal state.
        """
        best_score = float("-inf")
        legal_moves = game.get_legal_moves()
        if not legal_moves:   
            best_move =  (-1, -1)
        else:
            best_move =  legal_moves[0]

        for m in game.get_legal_moves():
            # call has been updated with a depth limit
            v = min_value(game.forecast_move(m), depth - 1)
            if v > best_score:
                best_score = v
                best_move = m
        #print('*** Exit Minimax ***  with best_move ***', best_move)
        return best_move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # TODO: finish this function!
        #raise NotImplementedError

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        legal_moves = game.get_legal_moves()
        if not legal_moves:   
            best_move =  (-1, -1)
        else:
            best_move =  legal_moves[0]

        depth = 1
        try:
            # Iterative Deepening
            # Apply cutoff when the timer is about to expire.
            while self.time_left() > self.TIMER_THRESHOLD:
                best_move = self.alphabeta(game, depth)
                depth = depth+1;
            return best_move

        except SearchTimeout:
            # When the time expires: Return the best move from the last completed search iteration
            pass  

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        def max_value(game, depth, alpha, beta):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            #print('*** Enter max_value *** depth:', depth)
            """ Return the value for a loss (-inf) if the game is over,
            otherwise return the maximum value over all legal child
            nodes.
            """
            if not bool(game.get_legal_moves()):
                # return utility value
                return game.utility(self)  
            
            # New conditional depth limit cutoff
            if depth <= 0:  # "==" could be used, but "<=" is safer 
                # self.score()` method for board evaluation
                return self.score(game, self)
            
            v = float("-inf")
            for m in game.get_legal_moves():
                # the depth should be decremented by 1 on each call
                v = max(v, min_value(game.forecast_move(m), depth - 1, alpha, beta))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            #print('*** Exit max_value *** value:', v)
            return v

        def min_value(game, depth, alpha, beta):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            #print('*** Enter min_value *** depth:', depth)
            """ Return the value for a win (+inf) if the game is over,
            otherwise return the minimum value over all legal child
            nodes.
            """
            if not bool(game.get_legal_moves()):
                # return utility value
                return game.utility(self) 
            
            # New conditional depth limit cutoff
            if depth <= 0:  # "==" could be used, but "<=" is safer 
                #self.score()` method for board evaluation
                return self.score(game, self)
            
            v = float("inf")
            for m in game.get_legal_moves():
                # the depth should be decremented by 1 on each call
                v = min(v, max_value(game.forecast_move(m), depth - 1, alpha, beta))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            #print('*** Exit min_value *** value:', v)
            return v

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        #raise NotImplementedError

        """ Return the move along a branch of the game tree that
        has the best possible value.  A move is a pair of coordinates
        in (column, row) order corresponding to a legal move for
        the searching player.
        
        You can ignore the special case of calling this function
        from a terminal state.
        """
        best_score = float("-inf")
        legal_moves = game.get_legal_moves()
        if not legal_moves:   
            best_move =  (-1, -1)
        else:
            best_move =  legal_moves[0]

        for m in game.get_legal_moves():
            # call has been updated with a depth limit
            v = min_value(game.forecast_move(m), depth - 1, alpha, beta)
            if v > best_score:
                best_score = v
                best_move = m
            alpha = max(alpha, best_score)
        #print('*** Exit Minimax ***  with best_move ***', best_move)
        return best_move

if __name__ == "__main__":
    from isolation import Board

    # create an isolation board (by default 7x7)
    player1 = MinimaxPlayer()
    player2 = AlphaBetaPlayer()
    game = Board(player1, player2)

    # place player 1 on the board at row 2, column 3, then place player 2 on
    # the board at row 0, column 5; display the resulting board state.  Note
    # that the .apply_move() method changes the calling object in-place.
    game.apply_move((2, 3))
    game.apply_move((0, 5))
    print(game.to_string())

    # players take turns moving on the board, so player1 should be next to move
    assert(player1 == game.active_player)

    # get a list of the legal moves available to the active player
    print(game.get_legal_moves())

    # get a successor of the current state by making a copy of the board and
    # applying a move. Notice that this does NOT change the calling object
    # (unlike .apply_move()).
    new_game = game.forecast_move((1, 1))
    assert(new_game.to_string() != game.to_string())
    print("\nOld state:\n{}".format(game.to_string()))
    print("\nNew state:\n{}".format(new_game.to_string()))

    # play the remainder of the game automatically -- outcome can be "illegal
    # move", "timeout", or "forfeit"
    winner, history, outcome = game.play()
    print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
    print(game.to_string())
    print("Move history:\n{!s}".format(history))

