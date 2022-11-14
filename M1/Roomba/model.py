from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agent import RandomAgent, ObstacleAgent
import time

class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, N, D, width, height, T):
        self.W = width
        self.H = height
        self.num_agents = N
        self.dust = D
        self.maxTime = T
        self.activationTime = time.time()
        self.grid = MultiGrid(width,height,torus = False) 
        self.schedule = RandomActivation(self)
        self.running = True 

        self.datacollector = DataCollector( 
        agent_reporters={"Steps": lambda a: a.steps_taken if isinstance(a, RandomAgent) else 0})

        D_Percent = int(width * height * self.dust)

        # Add dust to the thing
        for i in range(D_Percent):
            pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
            pos = pos_gen(self.grid.width, self.grid.height)

            obs = ObstacleAgent(i+2000, self)

            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.grid.place_agent(obs, pos)

        # Add the agent to [1,1]
        for i in range(self.num_agents):
            a = RandomAgent(i+1000, self) 
            self.schedule.add(a)

            self.grid.place_agent(a, (1,1))
        
        self.datacollector.collect(self)

    def step(self):
        '''Check if there's still dust left'''
        flag = False

        if (time.time() - self.activationTime) > self.maxTime:
            dirty_cells = 0
            self.running = False
            print("Maximum execution time reached.\nTerminating simulation.")
            for i in self.grid.get_neighbors(pos = (int(self.W/2),int(self.H/2)),moore = True,include_center = True,radius = int(self.W/2)):
                if (isinstance(i, ObstacleAgent)):
                    dirty_cells += 1
            print(f"Percentage of clean cells: {100 - ((dirty_cells)/(self.H * self.W) * 100)}%")
            return

        for i in self.grid.get_neighbors(pos = (int(self.W/2),int(self.H/2)),moore = True,include_center = True,radius = int(self.W/2)):
            if isinstance(i,ObstacleAgent):
                flag = True
                break

        if not flag:
            self.running = False
            print("Execution time:",(time.time() - self.activationTime), "s")
            print("Percentage of clean cells: 100%")
            return
        
        '''Advance the model by one step.'''
        self.schedule.step()
        self.datacollector.collect(self)