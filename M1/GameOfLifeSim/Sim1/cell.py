from mesa import Agent


class Cell(Agent):
    """Represents a single ALIVE or DEAD cell in the simulation."""

    DEAD = 0
    ALIVE = 1

    def __init__(self, pos, model, init_state=DEAD):
        """
        Create a cell, in the given state, at the given x, y position.
        """
        super().__init__(pos, model)
        self.x, self.y = pos
        self.state = init_state
        self._nextState = None

    def isAlive(self):
        return self.state == self.ALIVE

    def neighbors(self):
        return self.model.grid.neighbor_iter((self.x, self.y), True)

    def step(self):
        """
        Compute if the cell will be dead or alive at the next tick.  This is
        based on the number of alive or dead neighbors.  The state is not
        changed here, but is just computed and stored in self._nextState,
        because our current state may still be necessary for our neighbors
        to calculate their next state.
        """

        # Get the neighbors and apply the rules on whether to be alive or dead
        # at the next tick.
        if self.y != self.model.grid.height - 1:
            live_neighbors = ''.join([str(int(i.isAlive())) for i in self.neighbors() if i.y == self.y+1])
        else:
            live_neighbors = ''.join([str(int(i.isAlive())) for i in self.neighbors() if i.y == 0])

        # Assume nextState is unchanged, unless changed below.
        self._nextState = self.state

        if self.y != self.model.grid.height - 1:
            if live_neighbors == '000':
                self._nextState = self.DEAD
            elif live_neighbors == '001':
                self._nextState = self.ALIVE
            elif live_neighbors == '010':
                self._nextState = self.DEAD
            elif live_neighbors == '011':
                self._nextState = self.ALIVE
            elif live_neighbors == '100':
                self._nextState = self.ALIVE
            elif live_neighbors == '101':
                self._nextState = self.DEAD
            elif live_neighbors == '110':
                self._nextState = self.ALIVE
            elif live_neighbors == '111':
                self._nextState = self.DEAD
        else:
            self._nextState = self.state

    def advance(self):
        """
        Set the state to the new computed state -- computed in step().
        """
        self.state = self._nextState