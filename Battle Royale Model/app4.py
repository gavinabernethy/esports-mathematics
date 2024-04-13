import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import sys
import time

sys.path.append('.')
from agent import Agent, Player
from manager import Manager
from arena import Arena
from parameters import master_para
from PIL import Image


start_time = time.time()

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


outer_arena, outer_agent_list, survivor_ts = simulation(para=master_para)

# Create figure and axis

bg_image_path = 'br_map.png'
im = Image.open(bg_image_path)
arena = outer_arena
fig, ax = plt.subplots()
ax.set_ylim([-0.5, 0.5 + arena.height])
ax.set_xlim([-0.5, 0.5 + arena.width])
extent_vec = [-0.5, arena.width + 0.5, -0.5, arena.height + 0.5]
ax.imshow(im, aspect='auto', extent=extent_vec,
          origin='lower', alpha=0.6, interpolation='none')  # Set alpha value for the background image
scatter = ax.scatter([], [])


# Initialize function to create each frame of the animation
def update(frame):
    x_val = []
    y_val = []
    c = []
    for agent in outer_agent_list:
        x_val.append(agent.position_history[frame][0])
        y_val.append(agent.position_history[frame][1])
        if agent.status_history[frame] == 1:
            c.append(agent.colour_code)
        else:
            c.append(agent.death_code)

    scatter.set_offsets(np.column_stack([x_val, y_val]))
    scatter.set_facecolors(c)  # Set the face colors directly
    return scatter,


# Create animation
ani = FuncAnimation(fig, update, frames=100, interval=100, blit=True)  # Set interval to control animation speed

end_time = time.time()

print(end_time - start_time)

# Show plot
plt.show()

