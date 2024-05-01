# All the parameters for a single fully-specified simulation.

# ----------------------------------------------------------------------#

# Core:
main_para = {
    "NUM_PLAYERS": 3,
    "NUM_AGENTS": 99,
    "DELTA": 0.5,
    "TIME": 100,
    "BASE_FILENAME": 'battle_royale',
}

# ----------------------------------------------------------------------#

# Player parameters
player_para = {
    "VICTORY_WEIGHTING": 3.0,
    "SPEED": 6,
    "INERTIA_WEIGHTING": 0.90,
    "TEAMS": {x: {
        "STARTING_X_PERCENTAGE": 70.0,  # literally a percentage from 0 to 100!
        "STARTING_Y_PERCENTAGE": 80.0,  # literally a percentage from 0 to 100!
        "INITIAL_BEARING": 90.0  # initial bearing (north, clockwise) from 0 to 360 degrees
    } for x in range(main_para["NUM_PLAYERS"])},
}

# Agent parameters:
agent_para = {
    "VICTORY_WEIGHTING": 1.0,
    "DEFAULT_SPEED": 4,
    "DEFAULT_RADIUS": 0.6,
    "RANDOM_SPEED_VARIATION": 0.2,
    "INERTIA_WEIGHTING": 0.7,
}

# ----------------------------------------------------------------------#

# Arena parameters:
arena_para = {
    "WIDTH": 200,
    "HEIGHT": 100,
}

# ----------------------------------------------------------------------#

# Figure parameters:
figure_para = {
    "ANIMATION_FPS": 20,
    "FIGURE_WIDTH": 20,
    "FIGURE_HEIGHT": 6,
    "FIGURE_DPI": 100,
    "EPSILON": 0.0000001,
}


# ----------------------------------------------------------------------#

# Combine them:
master_para = {
    "main_para": main_para,
    "player_para": player_para,
    "agent_para": agent_para,
    "arena_para": arena_para,
    "figure_para": figure_para,
}
