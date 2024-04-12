import streamlit as st
import tempfile
from PIL import Image
import base64

from agent import Agent, Player
from manager import Manager
from arena import Arena
import data_manager
from parameters import master_para


main_para = master_para["main_para"]


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

def main_ui():
    st.title("Simulation: pedagogical")

    if st.button("Run Simulation"):
        with st.spinner("Procrastinating..."):
            # Execute a fresh simulation to generate new history:
            outer_arena, outer_agent_list, survivor_ts = simulation(para=master_para)
            st.success("Simulation complete!")



            gif_base_filename = master_para["main_para"]["BASE_FILENAME"]  + '.gif'
            filepath = data_manager.animate_simulation(figure_para=master_para["figure_para"],
                                            arena=outer_arena,
                                            agent_list=outer_agent_list,
                                            num_still=master_para["main_para"]["TIME"] / master_para["main_para"]["DELTA"],
                                            base_filename=gif_base_filename,
                                            delta=master_para["main_para"]["DELTA"],
                                            survivor_ts=survivor_ts,
                                            total_time=master_para["main_para"]["TIME"])
            st.success("Animation saved to gif!")

            mp4_path = filepath.replace('.gif', '.mp4')
            convert_gif_to_mp4(filepath, mp4_path)

            st.video(mp4_path)
            # st.success(f'Opening {filepath}')
            # file_ = open(filepath, "rb")
            # contents = file_.read()
            # data_url = base64.b64encode(contents).decode("utf-8")
            # file_.close()
            #
            # st.markdown(
            #     f'<img src="data:image/gif;base64,{data_url}" alt="Simulation gif">',
            #     unsafe_allow_html=True,
            # )


    else:
        st.info("Click the button to start the simulation.")

if __name__ == "__main__":
    main_ui()