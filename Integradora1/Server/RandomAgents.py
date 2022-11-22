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
import random
import math

class RandomAgent(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model,docks):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.direction = 4
        self.dock_list = docks
        self.carrying = False
        self.next_stack = None
        self.box = None

    def move(self):
        vision = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True)
        possible_steps = self.model.grid.get_neighborhood(self.pos,moore=False,include_center=False) 

        check = lambda x: isinstance(x, BoxObject)

        if not self.carrying: # is it not carrying a box?
            if True in list(map(check, vision)): # is there a box within vision?
                print(list(map(check, possible_steps)))
                if True in list(map(check, possible_steps)): # is the visible box within reach?
                    contents = self.model.grid.get_cell_list_contents(possible_steps[list(map(check, possible_steps)).index(True)])
                    print(f"Agente: {self.unique_id} recogiendo caja {contents[0].unique_id}")
                    for i in contents: # set carrying to true, get the box object, and remove box from grid
                        if isinstance(i, BoxObject):
                            self.carrying = True
                            self.box = i
                            self.model.grid.remove_agent(i)
                            dist = list(map(lambda x: math.sqrt((x[0] - self.pos[0])**2 + (x[1] - self.pos[1])**2), self.dock_list)) # distance vector to find closest stack
                            min_dist = dist.index(min(dist))
                            break
                        else:
                            continue
                else: # if the box is not within reach, move towards it
                    corner_box = possible_steps[map(check, possible_steps).index(True)] # coordinates of the corner with a box
                    corner_box_adjacents = self.model.grid.get_neighborhood(corner_box,moore=False,include_center=False)  # adjacent coordinates of the corner with a box
                    for i in corner_box_adjacents: # if the adjacents of the corner overlap with the possible steps of the robot, and said cell is empty, then move there
                        if i in possible_steps and self.model.grid.is_cell_empty(i):
                            self.direction = possible_steps.index(i)
                            break
                        else:
                            continue

            # Checks which grid cells are empty
            freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))
            if(self.direction > len(possible_steps) - 1):
                self.direction = self.random.choice([i for i, x in enumerate(freeSpaces) if x])
            # If the cell is empty, moves the agent to that cell; otherwise, it stays at the same position
            if freeSpaces[self.direction]:
                self.model.grid.move_agent(self, possible_steps[self.direction])
                print(f"Se mueve de {self.pos} a {possible_steps[self.direction]}; direction {self.direction}")
            else:
                print(f"No se puede mover de {self.pos} en esa direccion.")
        else: # is it carrying a box?
            if self.next_stack in self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False) and not self.next_stack == None: # is the next stack within reach?
                print(f"Agente {self.unique_id} dejo el paquete en el dock {self.next_stack}")
                self.model.grid.place_agent(self.box, self.next_stack)
                self.carrying = False
                self.box = None
                self.next_stack = None
            else: # the next stack is not within reach
                dist = map(lambda x: math.sqrt((x[0] - self.pos[0])**2 + (x[1] - self.pos[1])**2), self.dock_list) # distance vector to find closest stack
                self.next_stack = self.dock_list[dist.index(min(dist))]

                moves = [x for x in possible_steps if self.model.grid.is_cell_empty(x)]

                if len(moves) > 0: # if there are empty cells within reach, move towards the one closest to the stack
                    neigh_dist = map(lambda x: math.sqrt((x[0] - self.dock_list[min_dist][0])**2 + (x[1] - self.dock_list[min_dist][1])**2), moves)
                    min_neigh = neigh_dist.index(min(neigh_dist))

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

class BoxObject(Agent):
    """
    Box object. Just to add boxes to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

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
        self.stacks = []
        coor = math.ceil(boxes/5)
        for i in range(coor):
            if(i+1%2==0):
                self.stacks.append((width-2, i))
            else:
                self.stacks.append((1, i))
        
        self.full_check = [True]*coor
        
        # Creates the border of the grid
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]

        for pos in border:
            obs = ObstacleAgent(pos, self)
            self.schedule.add(obs)
            self.grid.place_agent(obs, pos)
        
        # Creates boxes in the grid
        pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
        for i in range(boxes):
            a = BoxObject(i+2000, self) 
            self.schedule.add(a)
            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos) or pos in self.stacks):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.grid.place_agent(a, pos)

        # Add the agent to a random empty grid cell
        for i in range(self.num_agents):
            a = RandomAgent(i+1000, self, self.stacks) 
            self.schedule.add(a)
            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos) or pos in self.stacks):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.grid.place_agent(a, pos)

    def step(self):
        # Check lists of coordinates of unloading cells to see if they are full
        for i in self.stacks:
            print(i)
            if len(self.grid.get_cell_list_contents(i)) >= 5:
                # If the cell is full, set the corresponding full_check value to False
                self.full_check[self.stacks.index(i)] = False
            else:
                # Otherwise, set the corresponding full_check value to True
                self.full_check[self.stacks.index(i)] = True
        '''Advance the model by one step.'''
        self.schedule.step()
