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


def initialisation(para):
    initial_arena = Arena(width=para["arena_para"]["WIDTH"], height=para["arena_para"]["HEIGHT"])
    initial_agent_list = [Player(agent_para=para["agent_para"],
                                 player_para=para["player_para"],
                                 default_survival_time=para["main_para"]["TIME"])]
    for agent in range(para["main_para"]["NUM_AGENTS"]):
        initial_agent_list.append(Agent(agent_para=para["agent_para"], default_survival_time=para["main_para"]["TIME"]))
    return initial_agent_list, initial_arena


def simulation(para):
    agent_list, arena = initialisation(para=para)

    manager = Manager(arena=arena, agent_list=agent_list, show_progress_bar=False)
    manager.simulate_event(time=para["main_para"]["TIME"], delta=para["main_para"]["DELTA"])
    return arena, agent_list, manager.number_of_survivors_history


# %%

def convert_coords(coord_str):
    coord_str = coord_str.strip('()')
    coords = coord_str.split(',')

    coord_dict = {'STARTING_X_PERCENTAGE': float(coords[0]), 'STARTING_Y_PERCENTAGE': float(coords[1])}
    return coord_dict


def main_ui():
    st.title("Simulation: pedagogical")

    player_coords = st.text_input('Starting coordinate (%): (x,y)', "(x, y)")
    im = Image.open(bg_image_path)

    # grab arena parameters so I can create the arena plot
    _, outer_arena = initialisation(
        para=master_para)  # TODO: consider changing `initialisation` and `simulation` function outputs
    extent_vec = [-0.5, outer_arena.width + 0.5, -0.5, outer_arena.height + 0.5]

    if st.button("Run Simulation"):
        with st.spinner("Procrastinating..."):

            # SIMULATION
            start_time = time.time()

            master_para['player_para'].update(
                convert_coords(player_coords)
            )

            # Execute a fresh simulation to generate new history:
            _, outer_agent_list, survivor_ts = simulation(para=master_para)

            if timings:
                st.success(f"Simulation complete in {time.time() - start_time:.2f}s")
            else:
                st.success("Simulation complete")

        with st.spinner("Doing something very important:"):
            # CREATE GIF
            start_time = time.time()

            fig, ax = plt.subplots()
            ax.set_ylim([-0.5, 0.5 + outer_arena.height])
            ax.set_xlim([-0.5, 0.5 + outer_arena.width])

            # TODO: ensure correct aspect ratio
            ax.imshow(im, aspect='auto', extent=extent_vec, origin='lower', alpha=0.6, interpolation='none')
            scatter = ax.scatter([], [])  # create our blank scatterplot axis

            # this function will create each frame of the animation
            def update(frame):
                # initialise empty lists
                xval = []
                yval = []
                cols = []

                # calculqte colours and positions of each agent
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
            components.html(ani.to_jshtml(default_mode='once'), height=600)

            if timings:
                st.success(f'gif displayed in {time.time() - start_time:.2f}s')

    else:
        st.info("Click the button to start the simulation.")
        fig, ax = plt.subplots()
        # TODO: ensure the aspect ratio of the arena is correct
        ax.imshow(im, aspect='auto', extent=extent_vec, origin='lower', alpha=1.0, interpolation='none')
        st.pyplot(fig)


if __name__ == "__main__":
    main_ui()
