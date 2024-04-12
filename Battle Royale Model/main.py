from agent import Agent, Player
from manager import Manager
from arena import Arena
import data_manager
from parameters import master_para

# ----------------------------- PARAMETERS -----------------------------#

# Advanced:
#  - Could adapt the congestion analysis code into some data analysis of spatial distribution of fights/deaths?

main_para = master_para["main_para"]


# --------------------- FUNCTIONS ---------------------#

def initialisation(para):
    # Returns the generic arena and the ordered list of agent objects
    initial_arena = Arena(width=para["arena_para"]["WIDTH"], height=para["arena_para"]["HEIGHT"])
    initial_agent_list = [Player(agent_para=para["agent_para"],
                                 player_para=para["player_para"],
                                 default_survival_time=para["main_para"]["TIME"])]
    for agent in range(para["main_para"]["NUM_AGENTS"]):
        initial_agent_list.append(Agent(agent_para=para["agent_para"], default_survival_time=para["main_para"]["TIME"]))
    return initial_agent_list, initial_arena


def simulation(para):
    # The function executes the simulation, and returns the completed agent list (with history) and the arena.
    agent_list, arena = initialisation(para=para)

    # Simulate the event:
    manager = Manager(arena=arena, agent_list=agent_list)
    manager.simulate_event(time=para["main_para"]["TIME"], delta=para["main_para"]["DELTA"])
    return arena, agent_list, manager.number_of_survivors_history


# ---------------------- EXECUTE ---------------------- #

# Execute a fresh simulation to generate new history:
outer_arena, outer_agent_list, survivor_ts = simulation(para=master_para)

# Animation
data_manager.animate_simulation(figure_para=master_para["figure_para"],
                                arena=outer_arena,
                                agent_list=outer_agent_list,
                                num_still=master_para["main_para"]["TIME"] / master_para["main_para"]["DELTA"],
                                base_filename=master_para["main_para"]["BASE_FILENAME"],
                                delta=master_para["main_para"]["DELTA"],
                                survivor_ts=survivor_ts,
                                total_time=master_para["main_para"]["TIME"],
                                )
