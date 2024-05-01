import random
import numpy as np


class Agent:

    def __init__(self,
                 agent_para,
                 number,
                 colour_code='blue',
                 death_code='black',
                 default_survival_time=0,
                 ):
        self.number = number
        self.agent_para = agent_para
        self.colour_code = colour_code
        self.death_code = death_code
        self.speed = agent_para["DEFAULT_SPEED"] * random.uniform(0.4, 0.6)
        self.inertia = agent_para["INERTIA_WEIGHTING"]
        self.kill_probability = agent_para["KILL_PROBABILITY"]
        self.attack_radius = agent_para["ATTACK_RADIUS"]
        self.health = 1.0
        self.kills = 0
        self.survival_time = default_survival_time
        self.status = 1  # (1) 'alive' or (0) 'dead'

        # Initialise current movement values
        self.previous_direction = np.asarray([0.0, 0.0])
        self.position = np.asarray([0.0, 0.0])
        self.new_position = np.asarray([0.0, 0.0])

        # History vectors
        self.position_history = []
        self.status_history = []
        self.kills_history = []

    def update_and_record(self):
        self.position = self.new_position
        self.position_history.append(self.position)
        self.status_history.append(self.status)
        self.kills_history.append(self.kills)

    def collision_detector(self, agent, current_time):
        separation = np.linalg.norm(self.position - agent.position)
        my_attack_radius = self.attack_radius
        enemy_attack_radius = agent.attack_radius
        is_kill = False
        is_killed = False

        if enemy_attack_radius < separation < my_attack_radius:
            # only I attack
            is_kill = bool(np.random.binomial(n=1, p=self.kill_probability, size=1))

        elif my_attack_radius < separation < enemy_attack_radius:
            # only you attack
            is_killed = bool(np.random.binomial(n=1, p=agent.kill_probability, size=1))

        elif separation < min(my_attack_radius, enemy_attack_radius):
            # both attack - one will definitely win
            probability_of_kill = self.kill_probability / (self.kill_probability + agent.kill_probability)
            if bool(np.random.binomial(n=1, p=probability_of_kill, size=1)):
                is_kill = True
            else:
                is_killed = True
        else:
            pass
        # resolve outcome
        if is_kill:
            self.kills += 1
            agent.status = 0  # DEAD
            agent.survival_time = current_time
        if is_killed:
            agent.kills += 1
            self.status = 0
            self.survival_time = current_time

    def calculate_new_position(self, arena, agent_list, delta, current_time):

        if self.status == 1:

            # Collision with other agents
            self_index = agent_list.index(self)
            for agent in agent_list[self_index + 1:]:
                if agent is not self and agent.status == 1:
                    self.collision_detector(agent=agent, current_time=current_time)

            # Movement
            direction = np.asarray([np.random.normal(0, 1, 1)[0], np.random.normal(0, 1, 1)[0]])
            if np.linalg.norm(direction) != 0.0:
                direction = self.speed * direction / np.linalg.norm(direction)
            direction = self.inertia * self.previous_direction + (1.0 - self.inertia) * direction

            # Check for override if near boundary
            if self.position[0] < 0.05 * arena.width:
                direction[0] = 1
            elif self.position[0] > 0.95 * arena.width:
                direction[0] = -1
            if self.position[1] < 0.05 * arena.height:
                direction[1] = 1
            elif self.position[1] > 0.95 * arena.height:
                direction[1] = -1

            # Re-normalise
            if np.linalg.norm(direction) != 0.0:
                direction = direction / np.linalg.norm(direction)

            # Update
            self.previous_direction = direction
            self.new_position = self.position + self.speed * direction * delta

            # Ensure can't be mapped out of bounds:
            self.new_position[0] = min(arena.width, max(0.0, self.new_position[0]))
            self.new_position[1] = min(arena.height, max(0.0, self.new_position[1]))

        else:
            self.new_position = self.position


# -----------------------------AGENT SUBCLASSES----------------------- #

# children
class Player(Agent):

    def __init__(self, number, agent_para, player_para, default_survival_time):
        super().__init__(
            agent_para=agent_para,
            number=number,
            death_code='brown',
            default_survival_time=default_survival_time,
        )
        self.number = number
        self.inertia = player_para["INERTIA_WEIGHTING"]
        self.starting_x_percentage = player_para["TEAMS"][number]["STARTING_X_PERCENTAGE"]
        self.starting_y_percentage = player_para["TEAMS"][number]["STARTING_Y_PERCENTAGE"]
        self.initial_bearing = player_para["TEAMS"][number]["INITIAL_BEARING"]
        self.kill_probability = player_para["TEAMS"][number]["KILL_PROBABILITY"]
        self.attack_radius = player_para["TEAMS"][number]["ATTACK_RADIUS"]
        self.colour_code = player_para["TEAMS"][number]["COLOUR"]
