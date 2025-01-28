import sys
sys.path.insert(0, '../')
from planet_wars import issue_order

""""
def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)
"""

def spread_to_weakest_planet(state):
    
    weak_planets = [planet for planet in state.neutral_planets() + state.enemy_planets() if planet.num_ships < 20]


    weak_planets = sorted(weak_planets, key=lambda p: p.num_ships)

    for target_planet in weak_planets:
        required_ships = target_planet.num_ships + 5  
        current_fleet_to_planet = 0
        for my_fleet in state.my_fleets():
            if my_fleet.destination_planet == target_planet.ID:
                current_fleet_to_planet += my_fleet.num_ships
        if current_fleet_to_planet > 0:
            continue;
        viable_planets = [ my_planet for my_planet in state.my_planets() if my_planet.num_ships > required_ships]


        if viable_planets:
            nearest_planet = min(viable_planets, key=lambda p: state.distance(p.ID, target_planet.ID) )
            return issue_order(state, nearest_planet.ID, target_planet.ID, required_ships)

    return False


def reinforce_planet(state):
    planet_under_threat = None
    total_enemy_fleet = 0
    current_fleet_to_planet = 0

    for my_planet in state.my_planets():
        for enemy_fleet in state.enemy_fleets():
            if enemy_fleet.destination_planet == my_planet.ID:
                planet_under_threat = my_planet
                total_enemy_fleet += enemy_fleet.num_ships

    if not planet_under_threat or total_enemy_fleet < planet_under_threat.num_ships:
        return False
    
    for my_fleet in state.my_fleets():
        if my_fleet.destination_planet == planet_under_threat.ID:
            current_fleet_to_planet += my_fleet.num_ships
    

    required_ships = total_enemy_fleet - planet_under_threat.num_ships
    if  current_fleet_to_planet > required_ships:
        return False;
    required_ships = required_ships - current_fleet_to_planet 
    if required_ships == 0:
        return False;

    viable_planets = [ my_planet for my_planet in state.my_planets() if my_planet.num_ships > required_ships ]


    if viable_planets:
        nearest_planet = min(
            viable_planets,
            key=lambda p: state.distance(p.ID, planet_under_threat.ID)
        )


        if nearest_planet and nearest_planet.num_ships > required_ships:
            return issue_order(state, nearest_planet.ID, planet_under_threat.ID, required_ships)

    return False

def offence_nature_planet_when_under_threat(state):
    
    natural_planet_under_threat = None
    current_enemy_fleet = None
    for enemy_fleet in state.enemy_fleets():
        for neutral_planet in state.neutral_planets():
            if (enemy_fleet.destination_planet == neutral_planet.ID and enemy_fleet.num_ships > neutral_planet.num_ships and enemy_fleet.turns_remaining < 5):
                natural_planet_under_threat = neutral_planet
                current_enemy_fleet = enemy_fleet
                break  # Found a natural planet under threat
        if natural_planet_under_threat:
            break

    if not natural_planet_under_threat:
        return False


    current_fleet_to_planet = 0;
    required_ships = current_enemy_fleet.num_ships - natural_planet_under_threat.num_ships + 5
    for my_fleet in state.my_fleets():
        if my_fleet.destination_planet == natural_planet_under_threat.ID:
            current_fleet_to_planet += my_fleet.num_ships

    if current_fleet_to_planet > required_ships:
        return False;
    required_ships = required_ships - current_fleet_to_planet 
    if required_ships == 0:
        return False;

    viable_planets = [
        my_planet for my_planet in state.my_planets() if my_planet.num_ships > required_ships
    ]
    # If viable planets are available, find the nearest one
    if viable_planets:
        closest_planet = min(viable_planets, key=lambda p: state.distance(p.ID, natural_planet_under_threat.ID))

        ##strongest_planet = max(closest_planets, key=lambda p: p.num_ships, default=None)

        # Issue the order to send the required ships
        return issue_order(state, closest_planet.ID, natural_planet_under_threat.ID, required_ships)
    return False

def attack_weak_defended_planets(state):
    sorted_enemy_planets = sorted(state.enemy_planets(), key=lambda p: p.num_ships)
    enemy_planet_offensive = None
    
    for enemy_planets in sorted_enemy_planets:
        isEnought = False
        for my_fleet in state.my_fleets():
            if my_fleet.destination_planet == enemy_planets.ID and my_fleet.num_ships > enemy_planets.num_ships :
                isEnought = True
                break;
        if isEnought == False:
            enemy_planet_offensive = enemy_planets;
            break;
    
    if not enemy_planet_offensive:
        return False
    ##enemy_planet_offensive = min(state.enemy_planets(), key=lambda p: p.num_ships, default=None)
    require_ships = enemy_planet_offensive.num_ships + 15

    if len(state.enemy_planets()) < 4:
        require_ships = require_ships + 25

    viable_planets = [ my_planet for my_planet in state.my_planets() if my_planet.num_ships > require_ships]
     # Take the 3 closest planets
    if viable_planets:
        closest_planets = sorted(viable_planets,key=lambda p: state.distance(p.ID, enemy_planet_offensive.ID))[:3] 
        # Find the strongest planet among the 3 closest
        strongest_planet = max(closest_planets, key=lambda p: p.num_ships, default=None)

        return issue_order(state, strongest_planet.ID, enemy_planet_offensive.ID, require_ships)
    return False



def fleet_reinforcements_offensive_action(state):
    require_ships = 0
    target_planet = None

    for enemy_planet in sorted(state.enemy_planets(), key=lambda p: p.num_ships):
        avg_turn = 0
        fleet_num = 0
        total_fleet = 0
        for my_fleet in sorted(state.my_fleets(), key=lambda f: f.num_ships, reverse=True):
            if my_fleet.destination_planet == enemy_planet.ID:
                total_fleet += my_fleet.num_ships
                fleet_num += 1
                avg_turn += my_fleet.turns_remaining
        if fleet_num == 0:
            continue;
        avg_turn = avg_turn / fleet_num if fleet_num > 0 else 0

        # Calculate the required ships to capture the planet
        require_ships = enemy_planet.num_ships + (enemy_planet.growth_rate * avg_turn) 
        if total_fleet < require_ships and total_fleet > 0:
            require_ships -= total_fleet
            target_planet = enemy_planet
            require_ships = require_ships + 15
            break

    if not target_planet:
        return False
    viable_planets = [my_planet for my_planet in state.my_planets() if my_planet.num_ships > require_ships]

    if viable_planets:
        closest_planets = sorted(viable_planets,key=lambda p: state.distance(p.ID, target_planet.ID))[:3]  
        # Find the strongest planet among the 3 closest
        strongest_planet = max(closest_planets, key=lambda p: p.num_ships, default=None)

        if strongest_planet:
            return issue_order(state, strongest_planet.ID, target_planet.ID, require_ships)

    return False
