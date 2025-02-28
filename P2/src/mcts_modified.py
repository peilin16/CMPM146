
from mcts_node import MCTSNode
from p2_t3 import Board
from random import choice
from math import sqrt, log

num_nodes = 100
explore_faction = 2.

def traverse_nodes(node: MCTSNode, board: Board, state, bot_identity: int):
    """ Traverses the tree until the end criterion are met.
    e.g. find the best expandable node (node with untried action) if it exist,
    or else a terminal node

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 1 or 2

    Returns:
        node: A node from which the next stage of the search can proceed.
        state: The state associated with that node

    """
    while not node.untried_actions and node.child_nodes:
        node = max(node.child_nodes.values(), key=lambda n: ucb(n, board.current_player(state) != bot_identity))
        state = board.next_state(state, node.parent_action)
    return node, state

def expand_leaf(node: MCTSNode, board: Board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node (if it is non-terminal).

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:
        node: The added child node
        state: The state associated with that node

    """
    if not node.untried_actions:
        return node, state
    next_action = node.untried_actions.pop()
    next_state = board.next_state(state, next_action)
    child_node = MCTSNode(node, next_action, board.legal_actions(next_state))
    node.child_nodes[next_action] = child_node
    return child_node, next_state


def rollout(board: Board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.
    
    Returns:
        state: The terminal game state

    """
    while not board.is_ended(state):
        legal_moves = board.legal_actions(state)
        best_move = None

        for move in legal_moves:
            next_state = board.next_state(state, move)
            if board.is_ended(next_state):
                outcome = board.points_values(next_state)
                if outcome[board.current_player(state)] == 1:  # Winning move
                    best_move = move
                    break
                if outcome[board.current_player(state)] == -1:  # Blocking move
                    best_move = move

        if not best_move:
            for move in legal_moves:
                if move[2] == 1 and move[3] == 1:  # If the move is in the center of the local board
                    best_move = move
                    break

        if not best_move:
            best_move = choice(legal_moves)

        state = board.next_state(state, best_move)
    return state


def backpropagate(node: MCTSNode|None, won: bool):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    while node:
        node.visits += 1
        node.wins += int(won)
        node = node.parent

def ucb(node: MCTSNode, is_opponent: bool):
    """ Calcualtes the UCB value for the given node from the perspective of the bot

    Args:
        node:   A node.
        is_opponent: A boolean indicating whether or not the last action was performed by the MCTS bot
    Returns:
        The value of the UCB function for the given node
    """
    if node.visits == 0:
        return float('inf')
    exploitation = node.wins / node.visits
    exploration = explore_faction * sqrt(log(node.parent.visits) / node.visits)
    return exploitation - exploration if is_opponent else exploitation + exploration

def get_best_action(root_node: MCTSNode):
    """ Selects the best action from the root node in the MCTS tree

    Args:
        root_node:   The root node
    Returns:
        action: The best action from the root node
    
    """
    return max(root_node.child_nodes.items(), key=lambda item: item[1].visits)[0]

def is_win(board: Board, state, identity_of_bot: int):
    # checks if state is a win state for identity_of_bot
    outcome = board.points_values(state)
    assert outcome is not None, "is_win was called on a non-terminal state"
    return outcome[identity_of_bot] == 1

def think(board: Board, current_state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        current_state:  The current state of the game.

    Returns:    The action to be taken from the current state

    """
    bot_identity = board.current_player(current_state) # 1 or 2
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(current_state))

    for _ in range(num_nodes):
        state = current_state
        node = root_node

        # Do MCTS - This is all you!
        # ...
        node, state = traverse_nodes(node, board, state, bot_identity)
        if node.untried_actions:
            node, state = expand_leaf(node, board, state)
        result = rollout(board, state)
        won = is_win(board, result, bot_identity)
        backpropagate(node, won)
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    best_action = get_best_action(root_node)
    
    print(f"Action chosen: {best_action}")
    return best_action
