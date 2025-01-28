#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn
print('aaaaa')

# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():

    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')

    
    # Defensive Strategy
    defensive_plan = Sequence(name="Defensive Strategy")
    under_threat_check = Check(planets_under_threat)
    reinforce_action = Action(reinforce_planet)
    defensive_plan.child_nodes = [under_threat_check, reinforce_action]

    # Fleet Reinforcements Offensive
    fleet_reinforcements_offensive = Sequence(name="Fleet Reinforcements Offensive")
    fleet_reinforcements_check = Check(is_fleet_reinforcement_needed)
    fleet_reinforcements_action = Action(fleet_reinforcements_offensive_action)
    fleet_reinforcements_offensive.child_nodes = [fleet_reinforcements_check, fleet_reinforcements_action]

    # Offensive Strategy for Natural Planets
    offensive_plan_for_natural = Sequence(name="Offensive Strategy For Natural Planet")
    natural_planet_under_threat_check = Check(is_neutral_planet_under_threat)
    natural_planet_action = Action(offence_nature_planet_when_under_threat)
    offensive_plan_for_natural.child_nodes = [natural_planet_under_threat_check, natural_planet_action]

    # Offensive Strategy
    offensive_plan = Sequence(name="Offensive Strategy")
    largest_fleet_check = Check(have_largest_fleet)
    attack_action = Action(attack_weak_defended_planets)
    offensive_plan.child_nodes = [largest_fleet_check, attack_action]

    # Spread Strategy
    spread_sequence = Sequence(name="Spread Strategy")
    neutral_planet_check = Check(spread_check)
    spread_action = Action(spread_to_weakest_planet)
    spread_sequence.child_nodes = [neutral_planet_check, spread_action]

    attack_newly_acquired_planets = Sequence(name="attack newly acquired planets")
    newly_acquired_planets_check = Check(spread_check)
    ##newly_acquired_planets_action = Action(attack_weak_defended_planets)
    attack_newly_acquired_planets.child_nodes = [newly_acquired_planets_check, attack_action]

    # Fallback Attack Strategy
    fallback_attack = Action(attack_weak_defended_planets)

    # Attach Strategies to Root Selector
    root.child_nodes = [
        spread_sequence,
        defensive_plan,
        offensive_plan_for_natural,
        fleet_reinforcements_offensive,
        attack_newly_acquired_planets,
        offensive_plan,
        fallback_attack,
    ]



    logging.info('\n' + root.tree_to_string())
    return root

# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)
    ##print('aaaaa')
    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
