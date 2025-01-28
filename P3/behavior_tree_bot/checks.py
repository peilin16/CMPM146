

def if_neutral_planet_available(state):
    return any(state.neutral_planets())

def if_offensive(state):
    
    if len(state.neutral_planets()) > len(state.my_planets()) + len(state.enemy_planets() ):
        return False
    return True

def have_largest_fleet(state):
    if len(state.my_planets()) < 4:
        return False;
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def planets_under_threat(state):
    if len(state.my_planets()) < 4:
        return False;
    for my_planet in state.my_planets():
        # Check if any enemy fleet is targeting this planet
        for enemy_fleet in state.enemy_fleets():
            if enemy_fleet.destination_planet == my_planet.ID:
                # Calculate the total reinforcements 
                current_offensive_fleet = sum(
                    my_fleet.num_ships
                    for my_fleet in state.my_fleets()
                    if my_fleet.destination_planet == my_planet.ID
                )
                # Check the enemy fleet poses a threat
                if enemy_fleet.num_ships > my_planet.num_ships + current_offensive_fleet:
                    return True  # The planet is under threat
    return False

def is_neutral_planet_under_threat(state):
    if len(state.neutral_planets()) == 0 or len(state.enemy_fleets()) == 0:
        return False
    for enemy_fleet in state.enemy_fleets():
        for neutral_planet in state.neutral_planets():
            if enemy_fleet.destination_planet == neutral_planet.ID and  enemy_fleet.turns_remaining < 3:
                current_offensive_fleet = sum(
                    my_fleet.num_ships
                    for my_fleet in state.my_fleets()
                    if my_fleet.destination_planet == neutral_planet.ID
                )
                if current_offensive_fleet < enemy_fleet.num_ships - neutral_planet.num_ships + 15:
                    return True
            ##return False
    return False

def is_fleet_reinforcement_needed(state):
    if len(state.my_planets())< 3:
        return False;
    
    for enemy_planet in sorted(state.enemy_planets(), key=lambda p: p.num_ships):
        avg_turn = 0
        fleet_num = 0
        total_fleet = 0

        # Calculate the total offensive fleet and average turns remaining
        for my_fleet in sorted(state.my_fleets(), key=lambda f: f.num_ships, reverse=True):
            if my_fleet.destination_planet == enemy_planet.ID:
                total_fleet += my_fleet.num_ships
                fleet_num += 1
                avg_turn += my_fleet.turns_remaining
        if fleet_num == 0:
            continue;
        
        avg_turn = avg_turn / fleet_num if fleet_num > 0 else 0
        require_ships = enemy_planet.num_ships + (enemy_planet.growth_rate * avg_turn)

        if total_fleet < require_ships and total_fleet > 0:
            return True
    return False;


def spread_check(state):
    
    for enemy_planet in state.enemy_planets():
        if enemy_planet.num_ships < 25:  
            return True;
    for enemy_planet in state.neutral_planets():
            if enemy_planet.num_ships < 25:  # Threshold for "newly acquired"
                return True;
    return False;