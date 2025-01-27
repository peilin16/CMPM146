

def if_neutral_planet_available(state):
    return any(state.neutral_planets())

def if_offensive(state):
    
    if len(state.neutral_planets()) > len(state.my_planets()) + len(state.enemy_planets() ):
        return False
    return True

def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def planets_under_threat(state):
    for my_planet in state.my_planets():
        # Check if any enemy fleet is targeting this planet
        for enemy_fleet in state.enemy_fleets():
            if enemy_fleet.destination_planet == my_planet.ID:
                # Calculate the total reinforcements heading to this planet
                current_offensive_fleet = sum(
                    my_fleet.num_ships
                    for my_fleet in state.my_fleets()
                    if my_fleet.destination_planet == my_planet.ID
                )
                # Check if the enemy fleet poses a threat
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
    for fleet in state.my_fleets():
        # Find the target enemy planet for the fleet
        target_planet = next(
            (planet for planet in state.enemy_planets() if planet.ID == fleet.destination_planet),
            None
        )

        if target_planet:
            # Calculate the total offensive fleet targeting this planet
            total_offensive_fleet = sum(
                my_fleet.num_ships
                for my_fleet in state.my_fleets()
                if my_fleet.destination_planet == target_planet.ID
            )

            # Calculate the ships required to capture the planet
            turns_remaining = fleet.turns_remaining
            required_ships = (
                target_planet.num_ships +
                (target_planet.growth_rate * turns_remaining) +
                5  # Additional buffer to ensure success
            )

            # Check if reinforcements are needed
            if total_offensive_fleet < required_ships:
                return True  # Reinforcements are needed
    return False  # No reinforcements required


def attack_newly_acquired_planets_check(state):
    for enemy_planet in state.enemy_planets():
        # Prioritize newly acquired planets with low ship counts
        if enemy_planet.num_ships < 25:  # Threshold for "newly acquired"
            return True;
    return False;