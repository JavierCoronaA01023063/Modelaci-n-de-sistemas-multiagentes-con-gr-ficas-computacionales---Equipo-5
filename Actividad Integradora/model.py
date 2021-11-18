from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import Grid
from agent import OrganizingAgent, ObstacleAgent, BoxAgent


class StorageModel(Model):

    def __init__(self, N, box, max_time, width, height, density=0.6):
        self.n_agents = N
        self.max_time = max_time
        self.num_box = box
        self.number_of_moves = 0
        self.grid = Grid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True

        # Creates the border of the grid
        border = [(x, y) for y in range(height) for x in range(
            width) if y in [0, height-1] or x in [0, width - 1]]

        for pos in border:
            obs = ObstacleAgent(pos, self)
            self.schedule.add(obs)
            self.grid.place_agent(obs, pos)

        # Add the organizing agent to a random cell
        for i in range(self.n_agents):
            a = OrganizingAgent(i+1000, self)
            self.schedule.add(a)

            def pos_gen(w, h): return (
                self.random.randrange(w), self.random.randrange(h))
            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos) and pos != (1, 1)):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.grid.place_agent(a, pos)

        # Add the box to a random cell
        for i in range(self.num_box):
            b = BoxAgent(i + 2000, self)
            self.schedule.add(b)

            def pos_gen(w, h): return (
                self.random.randrange(w), self.random.randrange(h))
            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos) and pos != (1, 1)):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.grid.place_agent(b, pos)

    def step(self):
        """
        Advanced the model by one step
        """
        if self.count_type(self, "Box") == 0 or self.max_time <= 0:
            self.running = False

        self.max_time -= 1
        self.schedule.step()

    @staticmethod
    def count_type(model, condition):
        count = 0
        for agent in model.schedule.agents:
            if agent.conidition == condition:
                count += 1
        return count
