
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
    

    
    current_state = state
    ## if end run out
    if board.is_ended(state) == False and len(node.untried_actions) != 0:

        best_node =None;
        best_ucb = -9999999;
        best_action = node.parent_action
        for current_action, current_node in node.child_nodes:
            
            ## detect the current identify
            is_opponent = True;
            if board.current_player(bot_identity):
                is_opponent = False;
            current_ucb = ucb(node, is_opponent)

            if(current_ucb > best_ucb):
                best_ucb = current_ucb
                best_node = current_node
                best_action = current_action
                
        if best_node is None:
            return node, current_state

        current_state = board.next_state(state,best_action);
        return  traverse_nodes(best_node, board, current_state, bot_identity);
        ##currentState = board.next_state(currentState, best_child.parent_action);
    return node, current_state


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
    if board.is_ended(state):
        return node,state
    

    
    next_action = node.untried_actions.pop();
    next_state = board.next_state(state,next_action);
        
    new_node = MCTSNode(node, next_action ,  board.legal_actions(next_state));
    node.child_nodes[next_action] = new_node;


    ##board = currentboard
    return new_node, next_state;




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
    if node.visits == 0:
        return float('inf');
    win = node.wins/node.visits;
    if is_opponent:
        win =  win * -1


    return win + (explore_faction * sqrt(log(node.parent.visits) / node.visits))

def get_best_action(root_node: MCTSNode):
    """ Selects the best action from the root node in the MCTS tree

    Args:
        root_node:   The root node
    Returns:
        action: The best action from the root node
    
    """
    
    best_visits = -9999999
    best_action = None
    for current_action, current_node in root_node.child_nodes:
        if current_node.visits > best_visits:
            best_visits = current_node.visits
            best_action = current_action

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
        node, state =  traverse_nodes(node , board , state, bot_identity );
        node,state = expand_leaf(node,board,state);
        result = rollout(board,state);
        won = is_win(board, result, bot_identity)
        backpropagate(node, won)
        # Do MCTS - This is all you!
        # ...

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    best_action = get_best_action(root_node , board ,state)
    
    print(f"Action chosen: {best_action}")
    return best_action
