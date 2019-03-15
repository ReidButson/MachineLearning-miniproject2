import numpy as np
import random


class ChessBoard:
    """Class representing a chess board. The chess board contains a list of queens on the chess board."""

    # The lookup table to use when calculating collisions, which holds all the diagonals to increment given any queen
    # For a description of the index values, see the check_collision function. The lookup table is created using
    # gen_lookup, and is done inside of setup_statics automatically.
    lookup_table = None

    dimensions = 8
    mutation_chance = 0.2

    def __init__(self, parent1=None, parent2=None):
        """Initializes a new chess board with random queen locations or with parents if the parents are given.

        Args:
            parent1 (ChessBoard): The object representing parent 1 of the node.
            parent2 (ChessBoard): The object representing parent 2 of the node.
        """

        # Generate using genetics
        if parent1 is not None and parent2 is not None:
            self.chromosome = self.create_child(parent1.chromosome, parent2.chromosome)
        # If only one parent is None, throw error as this should never occur
        elif (parent1 is not None and parent2 is None) or (parent1 is None and parent2 is not None):
            raise ValueError('One of the given parents was None', parent1, parent2)
        # Create a random chess board
        else:
            self.chromosome = random.sample(range(1, ChessBoard.dimensions + 1), ChessBoard.dimensions)

        # Creates the variable for fitness, which will be overwritten with the check_collisions function below
        self.fitness = None
        # Calculate the fitness of the board
        self.check_collisions()

    @staticmethod
    def setup_statics(dimensions=8, mutation_chance=0.02):
        """Sets the dimension for the problem, which also sets up the lookup table for the class.

        Args:
            dimensions (int): The dimensions for the board, as well as the number of queens on the board. Defaults to 8.
            mutation_chance (float): The percent chance for mutation to occur. Defaults to 0.02.
        """

        # Set all the static variables
        ChessBoard.dimensions = dimensions
        ChessBoard.mutation_chance = mutation_chance

        # Generate the lookup table for the chessboard, and set it to the global lookup table, using the given dimension
        ChessBoard.lookup_table = ChessBoard.gen_lookup(ChessBoard.dimensions)

    @staticmethod
    def gen_lookup(x):
        """
        Creates an array containing indexes that represent the diagonal
            3x3 example:
            (0, 7)  (1, 8)  (2, 9)
            (1, 6)  (2, 7)  (3, 8)
            (2, 5)  (3, 6)  (4, 7)

        Args:
            x (int): The number of queens in the problem
        Returns:
            Array: An x * x * 2 array containing indices for diagonals
        """

        # d is half the amount of diagonals
        d = 2 * x - 1

        # Empty x * x * 2 array
        table = np.array([[(0, 0)] * x] * x)

        for i in range(x):
            for j in range(x):
                # Labels each tile with the diagonal in the negative direction
                table[x - i - 1, j][0] = d + j + i
                # Labels each tile with the diagonal in the positive direction
                table[i, j][1] = j + i

        return table

    def check_collisions(self):
        """Checks and returns the number of collisions, and sets the fitness"""

        # Create the list to store collisions in columns.  Columns are mapped to indexes in the following ways:
        # Positive slope lists
        # a7p = 0
        # a6p = 1
        # a5p = 2
        # a4p = 3
        # a3p = 4
        # a2p = 5
        # a1p = 6
        # b1p = 7
        # c1p = 8
        # d1p = 9
        # e1p = 10
        # f1p = 11
        # g1p = 12
        # Negative slope lists
        # a2n = 13
        # a3n = 14
        # a4n = 15
        # a5n = 16
        # a6n = 17
        # a7n = 18
        # a8n = 19
        # b8n = 20
        # c8n = 21
        # d8n = 22
        # e8n = 23
        # f8n = 24
        # g8n = 25
        # Arbitrary indexes for the corner increments, to increase for loop speed
        # left = 26
        # right = 27

        # Collision list is proportional to the dimension of the problem
        diagonal_collision_list = [0] * (4 * ChessBoard.dimensions - 2)

        # The number of collisions that have occurred.
        collisions = 0

        # Loop through each gene to determine its diagonal
        for index, gene in enumerate(self.chromosome):
            # Get diagonals
            diagonals = ChessBoard.lookup_table[index, gene - 1]
            # Determine collisions in diagonals

            # Increment the first diagonal's collision value
            diagonal_collision_list[diagonals[0]] += 1
            if diagonal_collision_list[diagonals[0]] > 1:
                collisions += diagonal_collision_list[diagonals[0]] - 1
            # Increment the second diagonal's collision value
            diagonal_collision_list[diagonals[1]] += 1
            if diagonal_collision_list[diagonals[1]] > 1:
                collisions += diagonal_collision_list[diagonals[1]] - 1

        # The maximum number of collisions that can occur is 28, so inverse for fitness
        self.fitness = 28 - collisions

        return collisions

    @staticmethod
    def crossover(parent1, parent2):
        """
        creates a new child chromosome from two parents

        Args:
            parent1 (list): first chromosome
            parent2 (list): second chromosome

        Returns:
            list: a new chromosome from the parents genes
        """

        # Creates child as first half of parent1
        cross_point = random.randint(0, len(parent1))
        child_head = parent1[:cross_point]

        # takes remaining genes from second parent
        child_tail = [gene for gene in parent2 if gene not in child_head]

        return child_head + child_tail

    @staticmethod
    def mutate(chromosome):
        """
        Mutates a chromosome by flipping two random genes

        Args:
            chromosome (list) the chromosome to mutate

        Returns:
            list: the original chromosome with two random genes flipped
        """

        # random element index
        mutation_point = random.randint(0, len(chromosome) - 1)

        # Swaps the two genes, note any list at -1 is the last element in the list so no out of bound check is required
        chromosome[mutation_point], chromosome[mutation_point - 1] = \
            chromosome[mutation_point - 1], chromosome[mutation_point]
        return chromosome

    @staticmethod
    def create_child(parent1, parent2):
        """
        creates a new child and mutates it based on the mutation probability

        Args:
            parent1 (list): first chromosome
            parent2 (list): second chromosome

        Returns:
            list: a new chromosome from the parents genes, possibly mutated
        """

        child = ChessBoard.crossover(parent1, parent2)

        # rolls a number between 0 and 1
        roll = random.random()

        # if roll is below the mutation probability it mutates the child
        if roll < ChessBoard.mutation_chance:
            return ChessBoard.mutate(child)

        else:
            return child

    def __lt__(self, other):
        """Used to sort lists of chest boards by their fitness values.

        Args:
            other (ChessBoard): The other ChessBoard to compare the fitness value with.

        Returns:
            bool: Whether self is less than the other ChessBoard's fitness values.
        """

        return self.fitness < other.fitness

    def __bool__(self):
        """Tells you if the board is a solution to the queens problem."""

        return self.fitness == 28
