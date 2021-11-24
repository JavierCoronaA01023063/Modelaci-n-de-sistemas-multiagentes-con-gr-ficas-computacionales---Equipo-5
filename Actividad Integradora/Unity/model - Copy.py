from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from agent import OrganizingAgent, ObstacleAgent, BoxAgent


class StorageModel(Model):

    def __init__(self, N, box, width, height, density=0.6):
        self.n_agents = N
        self.num_box = box
        self.number_of_moves = 0
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.running = True

        # Creates the border of the grid
        border = [(x, y) for y in range(height) for x in range(
            width) if y in [0, height-1] or x in [0, width - 1]]

        for pos in border:
            obs = ObstacleAgent(self)
            self.schedule.add(obs)
            self.grid.place_agent(obs, pos)

        # Add the organizing agent to a random cell
        for i in range(self.n_agents):

            def pos_gen(w, h):
                return (self.random.randrange(w), self.random.randrange(h))

            pos = pos_gen(self.grid.width, self.grid.height)

            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)

            new_organizing_agent = OrganizingAgent(i+1000, self, pos)
            self.grid._place_agent(pos, new_organizing_agent)
            self.schedule.add(new_organizing_agent)

        # Add the box to a random cell
        for i in range(self.num_box):

            def pos_gen(w, h):
                return (self.random.randrange(w), self.random.randrange(h))

            pos = pos_gen(self.grid.width, self.grid.height)

            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)

            new_box_agent = BoxAgent(i+2000, self, pos)
            self.grid._place_agent(pos, new_box_agent)
            self.schedule.add(new_box_agent)

    def step(self):
        """
        Advanced the model by one step
        """
        if self.count_type(self, "Delivered") == self.num_box:
            self.running = False

        self.schedule.step()

    @staticmethod
    def count_type(model, condition):
        count = 0
        for agent in model.schedule.agents:
            if agent.condition == condition:
                count += 1
        return count
