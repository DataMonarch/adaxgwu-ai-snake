from typing import Dict, List, Set, Tuple

class Board():
    """Board class to represent the game board
    """
    def __init__(self, size) -> None:
        self.size = size
        self.board = [['-' for _ in range(size)] for _ in range(size)]
        self.board[0][4] = 'Y'
        self.board[1][0] = 'R'
        self.board[1][1] = 'A'
        self.board[3][0] = 'E'
        self.board[4][4] = 'K'
        
        self.alphabet = [chr(i) for i in range(65, 91)]
        self.assigned_letters = self.get_assigned_letters()
        self.unassigned_letters = self.get_unassigned_letters()
        print(self.unassigned_letters)
        
        self.domains = self.generate_domains()
        
    def get_unassigned_letters(self) -> List[str]:
        """Get unassigned letters
        """
        
        unassigned_letters = self.alphabet.copy()
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != '-':
                    unassigned_letters.remove(self.board[i][j])
        return unassigned_letters
        
    def get_assigned_letters(self) -> List[str]:
        """Get assigned letters
        """
        assigned_letters = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != '-':
                    assigned_letters.append(self.board[i][j])
        return assigned_letters
        
    def generate_domains(self, ) -> Dict[Tuple[int, int], Set[str]]:
        """Generate domain for each cell"""
        domains = {}
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != '-':
                    domains[(i, j)] = [self.board[i][j]]
                else:
                    domains[(i, j)] = self.unassigned_letters.copy()
        return domains
    
        
    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """Get empty cells
        """
        empty_cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == '-':
                    empty_cells.append((i, j))
        return empty_cells
    
    def is_cell_consistent(self, cell_location: Tuple[int, int], letter: str) -> bool:
        """Check if the board is consistent"""
        adjacent_cells = self.get_adjacent_cells(cell_location)
        for adjacent_cell in adjacent_cells:
            i, j = adjacent_cell
            if self.board[i][j] != '-':
                if self.adjacent_letters_constraint(letter, self.board[i][j]):
                    return True
        
        return False
        
    def get_adjacent_cells(self, cell_location: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get neighbors of a cell"""
        i, j = cell_location
        adjacent_cells = []
        if j > 0:
            adjacent_cells.append((i, j-1))
        if i > 0:
            adjacent_cells.append((i-1, j))
        if j < self.size - 1:
            adjacent_cells.append((i, j+1))
        if i < self.size - 1:
            adjacent_cells.append((i+1, j))
        return adjacent_cells

    def get_cell_domain(self, cell_location: Tuple[int, int]) -> List[str]:
        """ Get the domain of the cell at cell_location as 
        alphabets that are adjacent to the letter in that location
        """
        if self.board[cell_location[0]][cell_location[1]] != '-':
            return [self.board[cell_location[0]][cell_location[1]]]
        
        adjacent_cells = self.get_adjacent_cells(cell_location)
        adjacent_cell_values = [self.board[i][j] for i, j in adjacent_cells]
        print(f"Adjacent cell values for {cell_location}: {adjacent_cell_values}")
        
        cell_domain = self.unassigned_letters.copy()
        if adjacent_cell_values.count('-') == len(adjacent_cell_values):
            return cell_domain
        
        for adjacent_cell_value in adjacent_cell_values:
            if adjacent_cell_value != '-':
                if adjacent_cell_value in cell_domain:
                    cell_domain.remove(adjacent_cell_value)
        print(f"D>>> Domain for {cell_location}: {cell_domain}")
        return cell_domain
        

    def adjacent_letters_constraint(self, l1: str, l2: str) -> bool:
        """Check if two letters are adjacent"""
        
        return abs(ord(l1) - ord(l2)) == 1
    
            
    def forward_checking(self, cell_location: Tuple[int, int]) -> bool:
        """Forward checking
        """
        curr_cell_value = self.board[cell_location[0]][cell_location[1]]
        print(f"Forward checking at {cell_location}")
        
        for adjacent_cell in self.get_adjacent_cells(cell_location):
            i, j = adjacent_cell
            if self.board[i][j] == '-':
                domain = self.get_cell_domain(adjacent_cell)
                
                for letter in domain:
                    if not self.is_cell_consistent(adjacent_cell, letter) or letter == curr_cell_value:
                        domain.remove(letter)

                if len(domain) == 0:
                    return False
                
        return True
    
    def put_letter(self, letter: str, cell_location: Tuple[int, int]) -> bool:
        """Put a letter on the board at position (i, j) 
        """
        i, j = cell_location
        self.board[i][j] = letter
        self.assigned_letters.append(letter)
        self.unassigned_letters.remove(letter)
        
        self.domains[cell_location] = [letter]
        
        adjacent_cells = self.get_adjacent_cells(cell_location)
        print("Adjacent cells during insertion:", adjacent_cells)
        print("Performing domain reduction")
        
        return self.forward_checking(cell_location)
            
        
        # for adjacent_cell in adjacent_cells:
        #     if self.board[adjacent_cell[0]][adjacent_cell[1]] == '-':
        #         domain = self.get_cell_domain(adjacent_cell)
                
        #         if letter in domain:
        #             domain.remove(letter)
                    
        #         if len(domain) == 0:
        #             return False
                
        #         self.domains[adjacent_cell] = domain
                
        # return True
    
    def remove_letter(self, cell_location: Tuple[int, int]) -> None:
        
        i, j = cell_location        
        self.assigned_letters.remove(self.board[i][j])
        self.unassigned_letters.append(self.board[i][j])
        self.board[i][j] = '-'
        
        for adjacent_cell in self.get_adjacent_cells(cell_location):
            if self.board[adjacent_cell[0]][adjacent_cell[1]] == '-':
                self.domains[adjacent_cell] = self.get_cell_domain(adjacent_cell)
        

        
        

        
    def cells_mrv(self):
        """Minimum remaining value heuristic
        """
        unassigned_cells = self.get_empty_cells()
        return sorted (unassigned_cells, key=lambda cell_location: len(self.get_cell_domain(cell_location)))
    
    def backtracking(self) -> bool:
        """Backtracking algorithm
        """
        
        print(">>> Now at: ", self.assigned_letters)
        self.print_board()
        
        if len(self.assigned_letters) == self.size ** 2:
            return True
        
        cell_locations = self.cells_mrv()
        # if not cell_locations:
        #     return False
        
        cell_location = cell_locations[0]
        print(f">>> MRV: {cell_location}")
        
        print(f"Trying to put letter at {cell_location}")
        domain = self.get_cell_domain(cell_location)
        print(f"Domain: {domain}")
        for letter in domain:
            print(f"Trying letter {letter}")
            if self.put_letter(letter, cell_location):
                if self.backtracking():
                    return True
            self.remove_letter(cell_location)
            
        return False

    def print_board(self):
        """Prints the board
        """
        for i in range(self.size):
            for j in range(self.size):
                if j != self.size - 1:
                    print(f" {self.board[i][j]} ", end='|')
                else:
                    print(f" {self.board[i][j]} ", )
            print('-' * (self.size * 4 - 1))
        
        
b = Board(5)
b.print_board()
print(b.alphabet)

if b.backtracking():
    print("Solution found")
    b.print_board()
else:
    print("No solution found")

