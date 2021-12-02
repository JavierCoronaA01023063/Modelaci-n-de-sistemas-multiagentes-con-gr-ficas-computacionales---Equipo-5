from mesa import Agent
from math import sqrt
from queue import PriorityQueue


def reconstruct_path(cameFrom, current):
    total_path = [current]
    while current in cameFrom:
        current = cameFrom[current]
        total_path.insert(0, current)
    return total_path


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# A * finds a path from start to goal.
# h is the heuristic def. h(n) estimates the cost to reach goal from node n.


def algorithm(self, start, goal, h):
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or priority queue rather than a hash-set.
    openSet = PriorityQueue()
    openSet.put(start)

    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
    # to n currently known.
    cameFrom = {}

    # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
    gScore = {(x, y): float("inf")
              for content, x, y in self.model.grid.coord_iter()}
    gScore[start] = 0

    # For node n, fScore[n] = gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how short a path from start to finish can be if it goes through n.
    fScore = {(x, y): float("inf")
              for content, x, y in self.model.grid.coord_iter()}
    fScore[start] = h(start, goal)

    open_set_hash = {start}

    while not openSet.empty():
        current = openSet.get()

        self.possible_steps = self.model.grid.get_neighborhood(
            current,
            # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            moore=True,
            include_center=True)

        self.getCarDirections(current)

        # Checks which grid cells are empty
        # Open a list of empty spaces
        self.getFreeSpaces(current)

        self.next_moves = [p for p, f in zip(
            self.possible_steps, self.freeSpaces) if f == True]

        # This operation can occur in O(1) time if openSet is a min-heap or a priority queue

        if current == goal:
            return reconstruct_path(cameFrom, current)

        open_set_hash.remove(current)

        for neighbor in self.next_moves:
            # print(neighbor, "Neighbor")
            # if isinstance(neighbor, Road):
            # d(current, neighbor) is the weight of the edge from current to neighbor
            # tentative_gScore is the distance from start to the neighbor through current
            tentative_gScore = gScore[current] + 1
            if tentative_gScore < gScore[neighbor]:
                # This path to neighbor is better than any previous one. Record it!
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = tentative_gScore + \
                    h(neighbor, goal)
                if neighbor not in open_set_hash:
                    openSet.put(neighbor)
                    open_set_hash.add(neighbor)
            # self.model.grid.move_agent(self, current)
    # Open set is empty but goal was never reached
    return ["Fail"]


class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID
        direction: Randomly chosen direction chosen from one of eight directions
    """

    def __init__(self, unique_id, model, destination, startPos):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.pos = startPos
        self.destination = destination
        self.condition = "Driving"
        self.steps_taken = 1
        self.stepsWaited = 0
        self.freeSpaces = []
        self.possible_steps = []
        self.next_moves = []
        self.upIndexes = []
        self.downIndexes = []
        self.leftIndexes = []
        self.rightIndexes = []
        self.path = algorithm(self, startPos, destination, h)

    def getCarDirections(self, pos):
        self.upIndexes = []
        self.downIndexes = []
        self.leftIndexes = []
        self.rightIndexes = []
        currentPos = pos
        counter = 0
        for step in self.possible_steps:
            if step[0] - currentPos[0] < 0:
                self.leftIndexes.append(counter)
            if step[0] - currentPos[0] > 0:
                self.rightIndexes.append(counter)
            if step[1] - currentPos[1] > 0:
                self.upIndexes.append(counter)
            if step[1] - currentPos[1] < 0:
                self.downIndexes.append(counter)
            counter += 1

    def getFreeSpaces(self, pos):
        self.freeSpaces = []
        currentIndex = 0
        for step in self.possible_steps:
            content = self.model.grid.get_cell_list_contents(step)[0]
            if isinstance(content, Road):
                if not content.twoWay:
                    if content.direction == "Up" and currentIndex in self.upIndexes:
                        self.freeSpaces.append(True)
                    elif content.direction == "Down" and currentIndex in self.downIndexes:
                        self.freeSpaces.append(True)
                    elif content.direction == "Left" and currentIndex in self.leftIndexes:
                        self.freeSpaces.append(True)
                    elif content.direction == "Right" and currentIndex in self.rightIndexes:
                        self.freeSpaces.append(True)
                    else:
                        self.freeSpaces.append(False)
                else:
                    if content.direction[0] == "Up" and currentIndex in self.upIndexes:
                        self.freeSpaces.append(True)
                    elif content.direction[0] == "Down" and currentIndex in self.downIndexes:
                        self.freeSpaces.append(True)
                    elif content.direction[1] == "Left" and currentIndex in self.leftIndexes:
                        self.freeSpaces.append(True)
                    elif content.direction[1] == "Right" and currentIndex in self.rightIndexes:
                        self.freeSpaces.append(True)
                    else:
                        self.freeSpaces.append(False)
            elif isinstance(content, Traffic_Light):
                if content.direction == "Up" and currentIndex in self.upIndexes:
                    self.freeSpaces.append(True)
                elif content.direction == "Down" and currentIndex in self.downIndexes:
                    self.freeSpaces.append(True)
                elif content.direction == "Left" and currentIndex in self.leftIndexes:
                    self.freeSpaces.append(True)
                elif content.direction == "Right" and currentIndex in self.rightIndexes:
                    self.freeSpaces.append(True)
                else:
                    self.freeSpaces.append(False)

            elif isinstance(content, Destination) and content.pos == self.destination:
                self.freeSpaces.append(True)
            else:
                self.freeSpaces.append(False)
            currentIndex += 1

    def checkForTrafficLight(self, pos):
        for content in self.model.grid.iter_cell_list_contents(pos):
            if isinstance(content, Traffic_Light):
                return True
        return False

    def checkForOtherCar(self, pos):
        for content in self.model.grid.iter_cell_list_contents(pos):
            if isinstance(content, Car) and content.condition != "Arrived":
                return True
        return False

    def move(self):
        pass

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        print(f"Agente: {self.unique_id} movimiento {self.steps_taken}")
        if self.condition == "Driving":
            if self.pos != self.destination:
                # self.move()
                next_position = self.path[self.steps_taken]
                if self.checkForOtherCar(next_position):
                    if self.stepsWaited > 10:
                        print(
                            f"RECALCULATING (Waited for more than 10 steps for car to move), Agent: {self.unique_id}")
                        self.path = algorithm(
                            self, self.pos, self.destination, h)
                    else:
                        print(
                            f"Theres a car where I want to go!!, I'll wait here for a sec, Agent: {self.unique_id}")
                        self.stepsWaited += 1
                elif self.checkForTrafficLight(next_position):
                    if not self.model.grid.get_cell_list_contents(next_position)[0].state:
                        print(
                            f"Traffic light is red, I need to wait for green, Agent: {self.unique_id}")
                    else:
                        self.model.grid.move_agent(self, next_position)
                        self.steps_taken += 1
                        self.stepsWaited = 0
                else:
                    self.model.grid.move_agent(self, next_position)
                    self.steps_taken += 1
                    self.stepsWaited = 0

            else:
                print(
                    f"Arrived to destination at: {self.pos}!!!, Agent: {self.unique_id}")
                self.condition = "Arrived"
                self.model.complete_trips += 1


class Traffic_Light(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """

    def __init__(self, unique_id, model, direction, state=False, timeToChange=10):
        super().__init__(unique_id, model)
        self.state = state
        self.timeToChange = timeToChange
        self.condition = ""
        self.direction = direction

    def step(self):
        # if self.model.schedule.steps % self.timeToChange == 0:
        #     self.state = not self.state
        pass


class Destination(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.condition = ""

    def step(self):
        pass


class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.condition = ""

    def step(self):
        pass


class Road(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """

    def __init__(self, unique_id, model, twoWay, direction="Left"):
        super().__init__(unique_id, model)
        self.condition = ""
        self.direction = direction
        self.twoWay = twoWay

    def step(self):
        pass
