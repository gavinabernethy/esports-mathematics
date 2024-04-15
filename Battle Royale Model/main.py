import streamlit as st
import tempfile
from PIL import Image
import base64
import streamlit.components.v1 as components

import sys

sys.path.append('.')
from agent import Agent, Player
from manager import Manager
from arena import Arena
import data_manager
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

    manager = Manager(arena=arena, agent_list=agent_list, show_progress_bar=True)
    manager.simulate_event(time=para["main_para"]["TIME"], delta=para["main_para"]["DELTA"])
    return arena, agent_list, manager.number_of_survivors_history


from moviepy.editor import *


def convert_gif_to_mp4(gif_path, mp4_path):
    clip = (VideoFileClip(gif_path))
    clip.write_videofile(mp4_path, codec='libx264')


# %%

def main_ui():
    st.title("Simulation: pedagogical")

    if st.button("Run Simulation"):
        with st.spinner("Procrastinating..."):

            # SIMULATION
            start_time = time.time()
            # Execute a fresh simulation to generate new history:
            outer_arena, outer_agent_list, survivor_ts = simulation(para=master_para)

            if timings:
                st.success(f"Simulation complete in {time.time() - start_time:.2f}s")
            else:
                st.success("Simulation complete")

            # CREATE GIF
            start_time = time.time()
            im = Image.open(bg_image_path)
            fig, ax = plt.subplots()
            ax.set_ylim([-0.5, 0.5 + outer_arena.height])
            ax.set_xlim([-0.5, 0.5 + outer_arena.width])
            extent_vec = [-0.5, outer_arena.width + 0.5, -0.5, outer_arena.height + 0.5]

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
            components.html(ani.to_jshtml(), height=600)

            if timings:
                st.success(f'gif displayed in {time.time() - start_time:.2f}s')

    else:
        st.info("Click the button to start the simulation.")


if __name__ == "__main__":
    main_ui()
