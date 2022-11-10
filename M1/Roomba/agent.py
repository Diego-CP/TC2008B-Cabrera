from mesa import Agent

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
        self.steps_taken = 0

    def move(self):

        contents = self.model.grid.get_cell_list_contents(self.pos)
        check = lambda x: isinstance(x, ObstacleAgent)
        giveAgent = lambda x: isinstance(x, RandomAgent)

        if True in map(check,contents):
            for i in contents:
                if check(i):
                    self.model.grid.remove_agent(i)
                    break
        else:
            """ 
            Determines if the agent can move in the direction that was chosen
            """
            possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
                include_center=False) 

            next_moves_dirt = []

            for i in possible_steps:
                if not self.model.grid.is_cell_empty(i):
                    for j in self.model.grid.get_cell_list_contents(i):
                        if isinstance(j,ObstacleAgent):
                            next_moves_dirt.append(i)
                            break
                        else:
                            continue

            for i in next_moves_dirt:
                lst = self.model.grid.get_cell_list_contents(i)
                for j in lst:
                    if isinstance(j,RandomAgent):
                        next_moves_dirt.remove(i)
                        break

            for i in possible_steps:
                lst = self.model.grid.get_cell_list_contents(i)
                for j in lst:
                    if isinstance(j,RandomAgent):
                        possible_steps.remove(i)
                        break
            
            if len(next_moves_dirt) > 0:
                next_move = self.random.choice(next_moves_dirt)
            else:
                next_move = self.random.choice(possible_steps)

            # Now move:
            if self.random.random() < 0.1:
                self.model.grid.move_agent(self, next_move)
                self.steps_taken+=1

            # If the cell is empty, moves the agent to that cell; otherwise, it stays at the same position
            # if freeSpaces[self.direction]:
            #     self.model.grid.move_agent(self, possible_steps[self.direction])
            #     print(f"Se mueve de {self.pos} a {possible_steps[self.direction]}; direction {self.direction}")
            # else:
            #     print(f"No se puede mover de {self.pos} en esa direccion.")

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        # self.direction = self.random.randint(0,8)
        # print(f"Agente: {self.unique_id} movimiento {self.direction}")
        self.move()

class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  
