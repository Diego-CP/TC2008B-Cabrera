# -*- coding: utf-8 -*-
"""
Modelos de Agente y del medio ambiente
Movimiento aleatorio del auto en el grid

Solución al reto de TC2008B semestre AgostoDiciembre 2021
Autor: Jorge Ramírez Uresti, Octavio Navarro
"""

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import Grid
import Math

class RandomAgent(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.direction = 4

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=True) 
        
        # Checks which grid cells are empty
        freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))

        # If the cell is empty, moves the agent to that cell; otherwise, it stays at the same position
        if freeSpaces[self.direction]:
            self.model.grid.move_agent(self, possible_steps[self.direction])
            print(f"Se mueve de {self.pos} a {possible_steps[self.direction]}; direction {self.direction}")
        else:
            print(f"No se puede mover de {self.pos} en esa direccion.")

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        self.direction = self.random.randint(0,8)
        print(f"Agente: {self.unique_id} movimiento {self.direction}")
        self.move()

class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class BoxObject(Agent,ObstacleAgent):
    """
    Box object. Just to add boxes to the grid.
    """
 
class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, N, width, height,boxes):
        self.num_agents = N
        self.grid = Grid(width,height,torus = False) 
        self.schedule = RandomActivation(self)
        self.running = True 
         
        """
        Creates a list of coordinates for the obstacles
        """  
        stacks = []
        coor = Math.ceil(boxes/5)
        for i in range(coor):
            if(i+1%2==0):
                stacks.append({width-2, i})
            else:
                stacks.append({1, i})
        
        self.schedule.add(a)
        # Creates the border of the grid
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]

        for pos in border:
            obs = ObstacleAgent(pos, self)
            self.schedule.add(obs)
            self.grid.place_agent(obs, pos)
        
        # Creates boxes in the grid
        for i in range(self.num_agents):
            a = (i+2000, self) 
            self.schedule.add(a)
            pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos) or pos in stacks):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.grid.place_agent(a, pos)

        # Add the agent to a random empty grid cell
        for i in range(self.num_agents):
            a = RandomAgent(i+1000, self) 
            self.schedule.add(a)

            pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos) or pos in stacks):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.grid.place_agent(a, pos)

    def step(self):
        # Check lists of coordinates of unloading cells to see if they are full
        for count, content_list in enumerate(self.grid.get_cell_list_contents(self.stacks)):
            if len(content_list) >= 5:
                # If the cell is full, set the corresponding full_check value to False
                self.full_check[count] = False
            else:
                # Otherwise, set the corresponding full_check value to True
                self.full_check[count] = True
        '''Advance the model by one step.'''
        self.schedule.step()