import matplotlib.pyplot as plt
import numpy as np
import os.path
from matplotlib.animation import FuncAnimation


# -----------------------------FILE MANAGEMENT----------------------- #

def create_fig_filename(base_filename, suffix):
    file_number = 0
    is_filename_used = True
    file_path = None
    while is_filename_used:
        file_number += 1
        file_path = f'results/{base_filename}_{file_number}.{suffix}'
        is_filename_used = os.path.isfile(file_path)
    return file_path


# -----------------------------ANIMATION----------------------- #

def animate_simulation(figure_para, arena, agent_list, num_still, base_filename, delta, survivor_ts, total_time):
    fig = plt.figure(
        figsize=(figure_para["FIGURE_WIDTH"], figure_para["FIGURE_HEIGHT"]),
        dpi=figure_para["FIGURE_DPI"]
    )
    file_path = create_fig_filename(base_filename=base_filename + '_ani', suffix='gif')
    anim = FuncAnimation(fig, create_still, interval=100, frames=int(num_still),
                         fargs=(agent_list, arena, delta, survivor_ts, total_time,))
    anim.save(file_path, writer='ffmpeg', fps=figure_para["ANIMATION_FPS"])

    return file_path


def create_still(i, agent_list, arena, delta, survivor_ts, total_time):
    plt.gca().clear()
    plt.ylim([-0.5, 0.5 + arena.height])
    plt.xlim([-0.5, 0.5 + arena.width])
    plt.xticks([])
    plt.yticks([])
    extent_vec = [-0.5, arena.width + 0.5, -0.5, arena.height + 0.5]
    img = plt.imread("br_map.png")
    plt.imshow(img, aspect='auto', extent=extent_vec,
               origin='lower', alpha=0.6, interpolation='none')
    # plt.imshow(conditions_mod, cmap='RdYlGn_r', aspect='auto', extent=extent_vec,
    #            origin='lower', alpha=0.3, interpolation='none')
    # initialise the empty vectors of co-ordinates and colours and shapes
    x_val = []
    y_val = []
    c = []
    for agent in agent_list:
        x_val.append(agent.position_history[i][0])
        y_val.append(agent.position_history[i][1])
        if agent.status_history[i] == 1:
            c.append(agent.colour_code)
        else:
            c.append(agent.death_code)
    s = plt.scatter(x_val, y_val, color=c, s=70, marker='o', edgecolors="black", linewidths=0.5)

    # Write the current time in the frame
    time_text = f'Current time: {int(np.floor(i * delta))}'
    plt.annotate(text=time_text, xy=(arena.width * 1.02, arena.height * 1.05), annotation_clip=False)
    agents_text = f'Number of players: {survivor_ts[i]}'
    plt.annotate(text=agents_text, xy=(arena.width * 1.02, arena.height * 1.0), annotation_clip=False)
    pc_kills_text = f'PC kill counter: {agent_list[0].kills_history[i]}'  # PC should always be first in the list
    plt.annotate(text=pc_kills_text, xy=(arena.width * 1.02, arena.height * 0.95), annotation_clip=False)
    if agent_list[0].status_history[i] == 1:
        pc_status_text = f'PC status: Alive'  # PC should always be first in the list
    else:
        pc_status_text = f'PC status: Dead'  # PC should always be first in the list
    plt.annotate(text=pc_status_text, xy=(arena.width * 1.02, arena.height * 0.9), annotation_clip=False)

    # Final splash screen
    if i == int(total_time / delta) - 1:
        final_pc_survival_time = agent_list[0].survival_time
        final_pc_kill_count = agent_list[0].kills
        final_text = f"Survival time: {final_pc_survival_time} \n Kills: {final_pc_kill_count}"
        plt.annotate(text=final_text, xy=(arena.width * 0.25, arena.height * 0.3),
                     annotation_clip=False, size=70, c='r')


