
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
    best_child =node;
    currentState = state
    if node.visits != 0 and len(node.child_nodes) != 0:
        current =node.wins/ node.visits   
        for key in node.child_nodes.keys():
            n = node.child_nodes[key];
            n_c = n.wins/n.visits
            if(n_c >= current):
                current = n_c;
                best_child = n;
        currentState = board.next_state(state, best_child.parent_action);
        best_child = traverse_nodes(best_child,board , currentState, bot_identity);
        ##currentState = board.next_state(currentState, best_child.parent_action);
    return best_child, currentState


def getRandomAct(board, state):
    """ Returns a random move. """
    return choice(board.legal_actions(state))


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
    currentboard = board; 
    next_action = node.untried_actions.pop();
    new_state = board.next_state(state,next_action);
        
    new_node = MCTSNode(node, next_action ,  board.legal_actions(new_state));
    node.child_nodes[next_action] = new_node;

    ##board = currentboard
    return new_node, new_state;




def rollout(board: Board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.
    
    Returns:
        state: The terminal game state

    """
    while not board.is_ended(state):
        action = choice(board.legal_actions(state))  # Choose a random legal action
        state = board.next_state(state, action)     # Update the state
    return state


def backpropagate(node: MCTSNode|None, won: bool):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    
    while node is not None:
        node.visits += 1  # Increment visit count
        if won:
            node.wins += 1
        node = node.parent  # Move to the parent node

def ucb(node: MCTSNode, is_opponent: bool):
    """ Calcualtes the UCB value for the given node from the perspective of the bot

    Args:
        node:   A node.
        is_opponent: A boolean indicating whether or not the last action was performed by the MCTS bot
    Returns:
        The value of the UCB function for the given node
    """
    exploration_param = 1.414
    exploitation_term = node.wins / node.visits if node.visits > 0 else 0
    exploration_term = exploration_param * (sqrt(log(node.parent.visits) / node.visits) if node.visits > 0 else float('inf'))
    return exploitation_term - exploration_term if is_opponent else exploitation_term + exploration_term

def get_best_action(root_node: MCTSNode, board: Board, state):
    """ Selects the best action from the root node in the MCTS tree

    Args:
        root_node:   The root node
    Returns:
        action: The best action from the root node
    
    """
    
    for _ in range(1000):  # Perform 1000 iterations
        # Selection: Traverse the tree to find a promising node
        leaf_node, leaf_state = traverse_nodes(root_node, board, state, board.current_player(state))
        is_win = False;

        if not board.is_ended(leaf_state):
            expanded_node, expanded_state = expand_leaf(leaf_node, board, leaf_state)
            leaf_node.child_nodes[expanded_node.parent_action] = expanded_node
            leaf_node = expanded_node
            leaf_state = expanded_state
        elif board.is_ended(leaf_state):
            i =  board.win_values(state)


        result = rollout(board, leaf_state)
        
        

        backpropagate(leaf_node, is_win)

    
    best_action = max(
        root_node.child_nodes.values(),
        key=lambda child: child.visits
    ).parent_action

    return best_action


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

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    best_action = get_best_action(root_node , board ,state)
    
    print(f"Action chosen: {best_action}")
    return best_action
