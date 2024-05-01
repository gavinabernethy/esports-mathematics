import streamlit as st
import streamlit.components.v1 as components

# set the maximum animation size
import matplotlib

matplotlib.rcParams['animation.embed_limit'] = 2 ** 10

import sys

sys.path.append('.')

from agent import Agent, Player
from manager import Manager
from arena import Arena
from parameters import master_para
import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from PIL import Image

main_para = master_para["main_para"]
bg_image_path = 'br_map.png'
timings = False
st.set_page_config(layout="wide")


def initialisation(para):
    initial_arena = Arena(width=para["arena_para"]["WIDTH"], height=para["arena_para"]["HEIGHT"])
    # generate list of player subclass agents
    initial_agent_list = [Player(agent_para=para["agent_para"],
                                 number=_,
                                 player_para=para["player_para"],
                                 default_survival_time=para["main_para"]["TIME"])
                          for _ in range(main_para["NUM_PLAYERS"])]
    # generate remaining agents
    for agent in range(para["main_para"]["NUM_AGENTS"]):
        number = main_para["NUM_PLAYERS"] + agent
        initial_agent_list.append(Agent(agent_para=para["agent_para"],
                                        default_survival_time=para["main_para"]["TIME"],
                                        number=number)
                                  )
    return initial_agent_list, initial_arena


def simulation(para):
    agent_list, arena = initialisation(para=para)

    manager = Manager(arena=arena, agent_list=agent_list, show_progress_bar=False)
    manager.simulate_event(time=para["main_para"]["TIME"], delta=para["main_para"]["DELTA"])
    return arena, agent_list, manager.number_of_survivors_history


# required to help ensure correct aspect ratio
def forceaspect(ax, aspect=1.0):
    im = ax.get_images()
    extent = im[0].get_extent()
    ax.set_aspect(abs((extent[1] - extent[0]) / (extent[3] - extent[2])) / aspect)


# %%

# TODO: change program so we use absolute coordinates as player input
def convert_coords(coord_str):
    coord_str = coord_str.strip('()')
    coords = coord_str.split(',')
    coord_dict = {'STARTING_X_PERCENTAGE': float(coords[0]), 'STARTING_Y_PERCENTAGE': float(coords[1])}
    return coord_dict


def convert_bearing(bearing_str):
    bearing_str = bearing_str.strip('()')
    bearing_dict = {"INITIAL_BEARING": float(bearing_str)}
    return bearing_dict


def convert_widget(key, string):
    value = st.session_state[key]
    new_dict = {string: value}
    return new_dict


def main_ui():
    st.title("Simulation: Battle Royale")
    # TODO: Choose player colour;
    #  Final outcomes (kills, survival) will need to be displayed per team.
    # setup based on number of players
    num_players = main_para["NUM_PLAYERS"]
    player_coords = []
    player_bearing = []
    for player_num in range(num_players):
        col_1, col_2, col_3, col_4, col_5 = st.columns(5)  # looks better and room for additional attributes
        player_coords.append(col_1.text_input(f'Team {player_num + 1}: Starting coordinate (%):', "(x, y)",
                                              key=5 * player_num))
        player_bearing.append(col_2.text_input(f'Team {player_num + 1}: Bearing (0 - 360 degrees):',
                                               "\u03B8", key=5 * player_num + 1))

        def update(change):
            if np.mod(change, 5) == 2:
                st.session_state[change + 1] = (11.0 - st.session_state[change]) / 10.0
            elif np.mod(change, 5) == 3:
                st.session_state[change - 1] = 11.0 - 10.0 * st.session_state[change]

        col_3.slider(f'Team {player_num + 1}: Attack radius (1 - 10)', min_value=1, max_value=10, value=5,
                     key=5 * player_num + 2, on_change=update, args=(5 * player_num + 2,))
        col_4.slider(f'Team {player_num + 1}: Kill probability (0.1 - 1)', min_value=0.1, max_value=1.0, value=0.6,
                     key=5 * player_num + 3, on_change=update, args=(5 * player_num + 3,))

        col_5.selectbox(f'Team {player_num + 1} colour:', ('red', 'orange', 'yellow', 'green', 'purple'),
                        key=5 * player_num + 4)

    im = Image.open(bg_image_path)

    # grab arena parameters so I can create the arena plot
    _, outer_arena = initialisation(
        para=master_para)  # TODO: consider changing `initialisation` and `simulation` function outputs
    extent_vec = [-0.5, outer_arena.width + 0.5, -0.5, outer_arena.height + 0.5]

    if st.button("Run Simulation"):
        with st.spinner("Procrastinating..."):

            # SIMULATION
            start_time = time.time()

            for player_num in range(num_players):
                master_para['player_para']['TEAMS'][player_num].update(convert_coords(player_coords[player_num]))
                master_para['player_para']['TEAMS'][player_num].update(convert_bearing(player_bearing[player_num]))
                master_para['player_para']['TEAMS'][player_num].update(
                    convert_widget(key=5 * player_num + 2, string="ATTACK_RADIUS"))
                master_para['player_para']['TEAMS'][player_num].update(
                    convert_widget(key=5 * player_num + 3, string="KILL_PROBABILITY"))
                master_para['player_para']['TEAMS'][player_num].update(
                    convert_widget(key=5 * player_num + 4, string="COLOUR"))

            # Execute a fresh simulation to generate new history:
            _, outer_agent_list, survivor_ts = simulation(para=master_para)

            if timings:
                st.success(f"Simulation complete in {time.time() - start_time:.2f}s")
            else:
                st.success("Simulation complete")

        with st.spinner("Doing something very important:"):
            # CREATE GIF
            start_time = time.time()

            fig, ax = plt.subplots(figsize=(12, 6))
            ax.set_ylim([-0.5, 0.5 + outer_arena.height])
            ax.set_xlim([-0.5, 0.5 + outer_arena.width])

            # TODO: ensure correct aspect ratio
            ax.imshow(im, extent=extent_vec, origin='lower', alpha=0.6,
                      interpolation='none')
            forceaspect(ax, aspect=im.width / im.height)
            scatter = ax.scatter([], [])  # create our blank scatterplot axis

            # this function will create each frame of the animation
            def update(frame):
                # initialise empty lists
                xval = []
                yval = []
                cols = []

                # calculate colours and positions of each agent
                for agent in outer_agent_list:
                    xval.append(agent.position_history[frame][0])
                    yval.append(agent.position_history[frame][1])

                    # check alive status & colour accordingly
                    if agent.status_history[frame] == 1:
                        cols.append(agent.colour_code)
                    else:
                        cols.append(agent.death_code)

                scatter.set_offsets(np.column_stack([xval, yval]))
                scatter.set_facecolors(cols)
                return scatter,

            ani = FuncAnimation(fig, update, frames=100, interval=100,
                                blit=True)  # set interval to control animation speed

            if timings:
                st.success(f"gif created in {time.time() - start_time:.2f}s")

            # SHOW animation
            start_time = time.time()
            components.html(ani.to_jshtml(default_mode='once'), height=800, scrolling=True)

            if timings:
                st.success(f'gif displayed in {time.time() - start_time:.2f}s')

    else:
        st.info("Click the button to start the simulation.")
        fig, ax = plt.subplots()
        # TODO: ensure the aspect ratio of the arena is correct

        ax.imshow(im, extent=extent_vec, origin='lower', alpha=1.0, interpolation='none')
        forceaspect(ax, aspect=im.width / im.height)
        st.pyplot(fig)


if __name__ == "__main__":
    main_ui()
