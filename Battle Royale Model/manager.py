from numpy import cos, sin, pi, asarray, floor, mod as numpy_mod, random as numpy_random
import streamlit as st
from agent import Player


# TODO: is there really much value in the Manager object? The simulation loop could be brought
#  into main, and the initial position and bearing could be set at Agent initialisation.

class Manager:

    def __init__(self,
                 arena,
                 agent_list,
                 show_progress_bar=False,
                 ):
        self.arena = arena
        self.agent_list = agent_list
        self.number_of_agents = len(agent_list)
        self.number_of_survivors_history = []
        self.show_progress_bar = show_progress_bar

    def set_starting_positions(self):
        for agent in self.agent_list:
            if isinstance(agent, Player):
                # get starting position from input
                starting_x = self.arena.width * agent.starting_x_percentage / 100.0
                starting_y = self.arena.height * agent.starting_y_percentage / 100.0

                # convert input bearing from degrees to radians
                bearing = agent.initial_bearing * pi / 180.0

                # get starting x- and y- movement from bearing
                x_movement = sin(bearing)
                y_movement = cos(bearing)

                agent.previous_direction = asarray([x_movement, y_movement])

                agent.direction = asarray([x_movement, y_movement])

            else:
                # for NPC agents, draw from 2D Gaussian centred at centre of map
                starting_x = numpy_random.normal(0.5 * self.arena.width, 0.2 * self.arena.width, 1)
                starting_y = numpy_random.normal(0.5 * self.arena.height, 0.2 * self.arena.height, 1)
            # check within bounds
            agent.position[0] = min(0.95 * self.arena.width, max(0.05 * self.arena.width, starting_x))
            agent.position[1] = min(0.95 * self.arena.height, max(0.05 * self.arena.height, starting_y))

    def update_positions(self, delta, current_time):
        for agent in self.agent_list:
            agent.calculate_new_position(arena=self.arena, agent_list=self.agent_list,
                                         delta=delta, current_time=current_time)
        for agent in self.agent_list:
            agent.update_and_record()

    def simulate_event(self, time, delta):
        self.set_starting_positions()
        total_steps = int(time / delta)
        if self.show_progress_bar:
            progress_bar = st.progress(0)
        for time_step in range(total_steps):
            current_time = int(floor(time_step * delta))
            self.update_positions(delta, current_time)
            if self.show_progress_bar and numpy_mod(time_step, 10) == 0:
                progress_bar.progress(time_step / total_steps)
            # count survivors
            current_survivors = 0
            for agent in self.agent_list:
                current_survivors += agent.status
            self.number_of_survivors_history.append(current_survivors)
        if self.show_progress_bar:
            progress_bar.progress(1.0)
