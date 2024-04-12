import sys

sys.path.append('./Battle Royale Model')
import os
from agent import Agent, Player
from manager import Manager
from arena import Arena
import data_manager as dm
import imageio
from parameters import master_para
from main import simulation
import matplotlib.pyplot as plt
from tqdm import tqdm

IMAGE_FOLDER_OUT = './Battle Royale Model/results'
# %%

main_para = master_para["main_para"]

print("Running Simulation")
# initialise & run simulation
outer_arena, outer_agent_list, survivor_ts = simulation(para=master_para)
base_filename = 'temp_'

# %%

# TODO: fix aspect ratio
# create a single image
# dm.create_still(20,
#                 agent_list = outer_agent_list,
#                 arena = outer_arena,
#                 delta = main_para["DELTA"],
#                 survivor_ts = survivor_ts,
#                 total_time = main_para['TIME'],
#                 background_image = './Battle Royale Model/br_map.png')
# %%


print("Saving images out")
filenames_list = []  # so we can clean up later
for idx in tqdm(range(0, 100)):
    dm.create_still(idx,
                    agent_list=outer_agent_list,
                    arena=outer_arena,
                    delta=main_para["DELTA"],
                    survivor_ts=survivor_ts,
                    total_time=main_para['TIME'],
                    background_image='./Battle Royale Model/br_map.png')

    filename_out = os.path.join(IMAGE_FOLDER_OUT, f'{base_filename}{idx}.png')
    filenames_list.append(filename_out)
    plt.savefig(filename_out)
    plt.close

# %%


images = []
for _ in filenames_list:
    images.append(imageio.imread(_))
imageio.mimsave(os.path.join(IMAGE_FOLDER_OUT, f'{base_filename}_anim.gif'), images)

for _ in filenames_list:
    try:
        os.remove(_)
    except FileNotFoundError:
        print(f"File {_} not found.")

# %%
