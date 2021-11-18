from mesa import Agent

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

    def __init__(self, unique_id, pos, model):
        """
        Creates a new organizing agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.direction = 4
        self.condition = "Organizing"
        # How many moves the agent has made
        self.move_count = 0
        # How many boxes the agent has picked up
        self.box_count = 0
        self.pos = pos
        self.stash_count = 0

    def move(self):
        """
        Determines if the agent can move in the direction that was chosen
        """

        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=False, include_center=False)

        # Open a list of empty spaces
        freeSpaces = []
        for step in possible_steps:
            # If there is an Obstacle or Organazing Agent in the direction you are looking at, it will append a false to or free space list, meaning it wont be able to move there
            if isinstance(self.model.grid[step[0]][step[1]], ObstacleAgent) or isinstance(self.model.grid[step[0]][step[1]], OrganizingAgent):
                freeSpaces.append(False)
            else:
                # Else, it is possible to move to the cell grid
                freeSpaces.append(True)

        # If there is a free space, it will move the organizing agent to that cell
        if freeSpaces[self.direction]:
            # If there is an instance of a Box, it will move the Organizing Agent to that cell
            if isinstance(self.model.grid[possible_steps[self.direction][0]][possible_steps[self.direction][1]], BoxAgent):
                self.model.grid.move_agent(
                    self, possible_steps[self.direction])
                self.move_count += 1
                print(f"Agent {self.unique_id} se movió")
                print(self.model.number_of_moves)
                # Pick up the box
                self.model.grid[possible_steps[self.direction][0]][possible_steps[self.direction][1]].move_agent(self.pos)
            
                self.model.number_of_moves += 1
        else: 
            print(f"Agent {self.unique_id} no se movió")
            
                


    def step(self):
        self.direction = self.random.randint(0, 8)
        self.move()


"""
Class to define the obstacle agent
"""


class ObstacleAgent(Agent):
    """
    Obstacle agent
    """

    def __init__(self, unique_id, model):
        """
            Creates a new obstacle agent.
            Args:
                unique_id: The agent's ID
                model: Model reference for the agent
            """
        super().__init__(unique_id, model)
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

    def __init__(self, unique_id, model):
        """
        Creates a new box agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.condition = "Box"

    def step(self):
        pass
