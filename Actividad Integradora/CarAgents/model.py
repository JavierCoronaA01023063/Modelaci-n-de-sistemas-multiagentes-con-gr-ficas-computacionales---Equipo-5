from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import *
import json
from random import choice


class RandomModel(Model):
    """
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """

    def __init__(self, N):

        listOfDestinationPos = []
        self.number_cars = N
        self.complete_trips = 0

        dataDictionary = json.load(open("mapDictionary.txt"))

        with open('base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0]) - 1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus=False)
            self.schedule = RandomActivation(self)

            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(f"r{r*self.width+c}",
                                     self, False, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    if col in [".", ",", ";"]:
                        agent = Road(f"r{r*self.width+c}",
                                     self, True, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col in ["R", "U", "L", "A"]:
                        agent = Traffic_Light(
                            f"tl{r*self.width+c}", self, dataDictionary[col][2], False if dataDictionary[col][1] else True, int(dataDictionary[col][0]))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                    elif col == "#":
                        agent = Obstacle(f"ob{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col == "D":
                        agent = Destination(f"d{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        listOfDestinationPos.append((c, self.height - r - 1))

            for i in range(N):
                def pos_gen(w, h):
                    return (self.random.randrange(w), self.random.randrange(h))

                pos = pos_gen(self.grid.width, self.grid.height)

                while (not isinstance(self.grid.get_cell_list_contents(pos)[0], Road)):
                    pos = pos_gen(self.grid.width, self.grid.height)

                car = Car(i, self, choice(listOfDestinationPos), pos)
                self.grid.place_agent(car, pos)
                self.schedule.add(car)

        self.num_agents = N
        self.running = True

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        if self.schedule.steps % 10 == 0:
            for agents, x, y in self.grid.coord_iter():
                for agent in agents:
                    if isinstance(agent, Traffic_Light):
                        agent.state = not agent.state

        if self.complete_trips == self.number_cars:
            self.running = False
            print("All cars arrived safely to their destinations!!!")

    @staticmethod
    def count_type(model, condition):
        count = 0
        for agent in model.schedule.agents:
            if agent.condition == condition:
                count += 1
        return count
