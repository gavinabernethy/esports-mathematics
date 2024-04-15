import streamlit as st
import tempfile
from PIL import Image
import base64

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
            st.success(f"Simulation complete in {time.time() - start_time:.2f}s")

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

            # this function will create each frame of the animatuion

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

            st.success(f"gif created in {time.time() - start_time:.2f}s")

            # SAVE GIF
            start_time = time.time()
            gif_filename = os.path.join('./results', 'animation.gif')
            ani.save(gif_filename, writer='ffmpeg', fps=master_para['figure_para']["ANIMATION_FPS"])
            st.success(f"Animation saved to gif in {time.time() - start_time:.2f}s")

            # SAVE MP4
            start_time = time.time()
            mp4_path = gif_filename.replace('.gif', '.mp4')
            convert_gif_to_mp4(gif_filename, mp4_path)
            st.success(f"Animation saved to mp4 in {time.time() - start_time:.2f}s")
            st.video(mp4_path)

    else:
        st.info("Click the button to start the simulation.")


if __name__ == "__main__":
    main_ui()
