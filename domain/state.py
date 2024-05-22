


class QuoridorState:


    def __init__(
        self,
        agent_positions: list[tuple[tuple[int, int], str]],
        wall_positions: list[tuple[tuple[int, int], str]],
        agent_to_move: str,
        walls_left: tuple[int, int],
        parent = None,
    ):
        self.agent_positions = agent_positions
        self.wall_positions = wall_positions
        self.agent_to_move = agent_to_move
        self.walls_left = walls_left
        self.parent = parent
        self.path_cost = 0 if parent is None else parent.path_cost + 1

    def __repr__(self) -> str:
        board = []
        board.append(f"{self.agent_to_move}|({self.walls_left})")
        flatline = ["-" for i in range(19)]
        flatline = "".join(flatline)
        board.append(flatline)
        # Add the grid and the players to the list of strings
        for y in range(9):
            line = []
            for x in range(9):
                line.append("|")
                for position, agent in self.agent_positions:
                    if (x, y) == position:
                        line.append(agent)
                    else:
                        line.append(" ")
            line.append("|")
            board.append("".join(line))
            board.append(flatline.copy())
        # Add the walls
        for wall in self.wall_positions:
            x, y = wall[0]
            board[(y+1)*2][(x+1)*2] = '#'
            if wall[1] == "v":
                board[(y+1)*2-1][(x+1)*2] = '#'
                board[(y+2)*2-1][(x+1)*2] = '#'
            else:
                board[(y+1)*2][(x+1)*2-1] = '#'
                board[(y+1)*2][(x+2)*2-1] = '#'
        # print the board
        for l in board:
            string = "".join(l)
            print(string)
        return '\n'.join(board)

    def __eq__(self, other) -> bool:
        """
        Notice that we here only compare the agent positions and box positions, but ignore all other fields.
        That means that two states with identical positions but e.g. different parent will be seen as equal.
        """
        if isinstance(other, self.__class__):
            return self.agent_positions == other.agent_positions and self.wall_positions == other.wall_positions and self.agent_to_move == other.agent_to_move and self.walls_left == other.walls_left
        else:
            return False
        
    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
    
    def __hash__(self):
        """
        Allows the state to be stored in a hash table for efficient lookup.
        Notice that we here only hash the agent positions and box positions, but ignore all other fields.
        That means that two states with identical positions but e.g. different parent will map to the same hash value.
        """
        return hash((tuple(self.agent_positions), tuple(self.box_positions), self.agent_to_move, self.walls_left))