from mesa import Agent
from math import sqrt

"""
Class that defines the agent that moves the boxes in the grid
"""


class OrganizingAgent(Agent):
    """
    Agent that moves, detects boxes, pickup boxes and puts them in a defined coordinate of the grid. (It can put 5 boxes in a stash)
    Attributes:
        unique_id: Agent´s ID
        direction: Randomly chose a direcction from the eight directions
    """

    def __init__(self, unique_id, model, pos):
        """
        Creates a new organizing agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.direction = 0
        self.name = "OrganizingAgent"
        self.condition = "Searching"
        # How many moves the agent has made
        self.move_count = 0
        # How many boxes the agent has picked up
        self.box_count = 0
        self.stash_count = 0
        self.freeSpaces = []
        self.possible_steps = []
        self.carried_box = None

    def get_free_spaces(self):
        """
        Determines if the agent can move in the direction that was chosen
        """
        self.possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=False, include_center=False)

        # Open a list of empty spaces
        self.freeSpaces = []
        for step in self.possible_steps:
            # If there is an Obstacle or Organazing Agent in the direction you are looking at, it will append a false to or free space list, meaning it wont be able to move there
            if self.model.grid.is_cell_empty(step):
                self.freeSpaces.append(2)
            else:
                for content in self.model.grid.iter_cell_list_contents(step):
                    if content.condition == "Delivered":
                        self.freeSpaces.append(2)
                        break
                    elif content.condition == "OrganizingAgent" or content.condition == "Obstacle":
                        self.freeSpaces.append(0)
                        break
                    else:
                        self.freeSpaces.append(1)
                        break

        print(self.possible_steps, self.freeSpaces)

    def check_for_box(self):
        for neighbor in self.model.grid.neighbor_iter(self.pos, moore=False):
            if neighbor.condition == "Box":
                return True
        return False

    def grab_box(self):
        self.condition = "Carrying"
        for neighbor in self.model.grid.neighbor_iter(self.pos):
            if neighbor.condition == "Box":
                self.carried_box = neighbor
                self.carried_box.condition = "Moving"
                break
        self.model.grid.move_agent(self.carried_box, self.pos)

    def head_home(self):
        if self.pos == (1, 1):
            self.condition = "Searching"
            self.carried_box.condition = "Delivered"
            return

        home_x = 1
        home_y = 1
        current_pos_x = self.pos[0]
        current_pos_y = self.pos[1]

        distances = []
        distances.append(sqrt(((current_pos_x - 1) - home_x)
                              ** 2 + (current_pos_y - home_y) ** 2))
        distances.append(sqrt((current_pos_x - home_x) **
                              2 + (current_pos_y - 1 - home_y) ** 2))
        distances.append(sqrt((current_pos_x - home_x) **
                              2 + (current_pos_y + 1 - home_y) ** 2))
        distances.append(sqrt(((current_pos_x + 1) - home_x)
                              ** 2 + (current_pos_y - home_y) ** 2))

        min_index = 0
        min_value = 1000
        for distance in range(len(distances)):
            print(distances)
            if distances[distance] < min_value and self.freeSpaces[distance] == 2:
                min_value = distances[distance]
                min_index = distance

        self.model.grid.move_agent(self, self.possible_steps[min_index])
        self.model.grid.move_agent(
            self.carried_box, self.possible_steps[min_index])
        self.pos = self.possible_steps[min_index]

    def move(self):
        # If there is a free space, it will move the organizing agent to that cell
        if self.freeSpaces[self.direction] == 2:
            self.model.grid.move_agent(
                self, self.possible_steps[self.direction])
        else:
            print(f"Agent {self.unique_id} no se movió")

    def step(self):
        print(self.condition)
        self.direction = self.random.randint(0, 3)
        self.get_free_spaces()

        if self.condition == "Searching":
            if self.check_for_box():
                self.grab_box()
            else:
                self.move()
        elif self.condition == "Carrying":
            self.head_home()


"""
Class to define the obstacle agent
"""


class ObstacleAgent(Agent):
    """
    Obstacle agent
    """

    def __init__(self, model):
        """
            Creates a new obstacle agent.
            Args:
                unique_id: The agent's ID
                model: Model reference for the agent
            """
        super().__init__(self, model)
        self.condition = "Obstacle"

    def step(self):
        pass


""""
Class of Box Agent
"""


class BoxAgent(Agent):
    """
    Box agent
    """

    def __init__(self, unique_id, model, pos):
        """
        Creates a new box agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.condition = "Box"
        if self.pos == (1, 1):
            self.condition = "Delivered"

    def step(self):
        pass
