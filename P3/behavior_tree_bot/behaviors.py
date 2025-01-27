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

def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, weakest_planet.num_ships + 2)


def reinforce_planet(state):
    # Find planets under threat
    for my_planet in state.my_planets():
        for enemy_fleet in state.enemy_fleets():
            if enemy_fleet.destination_planet == my_planet.ID and enemy_fleet.num_ships > my_planet.num_ships:
                nearest_planet = None
                min_distance = float('inf')

                for planet in state.my_planets():
                    if planet.ID != my_planet.ID:
                        distance = state.distance(planet.ID, my_planet.ID)
                        if distance < min_distance:
                            nearest_planet = planet
                            min_distance = distance
                required_ships = enemy_fleet.num_ships - my_planet.num_ships + 1;
                if nearest_planet and nearest_planet.num_ships - 5 > required_ships :
                    return issue_order(state, nearest_planet.ID, my_planet.ID, required_ships)
    return False

def offence_nature_planet_when_under_threat(state): 
    #if no more natural planets return False
    
    for enemy_fleet in state.enemy_fleets():
        for neutral_planet in state.neutral_planets():
            if enemy_fleet.destination_planet == neutral_planet.ID and enemy_fleet.num_ships > neutral_planet.num_ships: 
                if enemy_fleet.turns_remaining < 5:  
                    viable_planets = []
                    for my_planet in state.my_planets():
                        if my_planet.num_ships > enemy_fleet.num_ships:
                            viable_planets.append(my_planet)
                    if viable_planets: 
                        nearest_planet = min(viable_planets, key=lambda p: state.distance(p.ID, neutral_planet.ID)) 
                        required_ships = enemy_fleet.num_ships - neutral_planet.num_ships + 10 ##(neutral_planet.growth_rate *(enemy_fleet.num_ships - neutral_planet.num_ships) * 2 )
                        if(nearest_planet.num_ships - 10 > required_ships):
                            return issue_order(state, nearest_planet.ID, neutral_planet.ID, required_ships)
    return False

def attack_weak_defended_planets(state):
    for enemy_planet in sorted(state.enemy_planets(), key=lambda p: p.num_ships):
        for my_planet in sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True):
            ##d = state.distance(my_planet,enemy_planet);
            required_ships =   enemy_planet.num_ships  + 15## (enemy_planet.growth_rate * enemy_planet.num_ships * 12)
            if my_planet.num_ships > required_ships:
                return issue_order(state, my_planet.ID, enemy_planet.ID, required_ships)
    return False

def fleet_reinforcements_offensive_action(state):
    for enemy_planet in sorted(state.enemy_planets(), key=lambda p: p.num_ships):
        for my_planet in sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True):
            # Calculate the distance and turns required
            distance = state.distance(my_planet.ID, enemy_planet.ID)
            turns_remaining = distance

            # Calculate the ships required to conquer the planet
            required_ships = enemy_planet.num_ships + (enemy_planet.growth_rate * turns_remaining) + 1

            # Check if the current planet can send enough ships
            if my_planet.num_ships > required_ships:
                # Send the required ships
                return issue_order(state, my_planet.ID, enemy_planet.ID, required_ships)
            else:
                # Attempt to reinforce the offensive fleet from other planets
                reinforce_planets = [
                    p for p in state.my_planets()
                    if p.ID != my_planet.ID and p.num_ships > (required_ships - my_planet.num_ships)
                ]

                if reinforce_planets:
                    # Find the nearest planet to reinforce the fleet
                    nearest_planet = min(reinforce_planets, key=lambda p: state.distance(p.ID, my_planet.ID))
                    reinforce_ships = required_ships - my_planet.num_ships
                    issue_order(state, nearest_planet.ID, my_planet.ID, reinforce_ships)
                    return issue_order(state, my_planet.ID, enemy_planet.ID, required_ships)

    return False
