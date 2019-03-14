import random
from threading import Lock


class ChessBoard:
    """Class representing a chess board. The chess board contains a list of queens on the chess board."""

    # The lookup table to use when calculating collisions, which holds all the diagonals to increment given any queen
    # For a description of the index values, see the check_collision function
    lookup_table = {
        '11': (6, 26),
        '12': (5, 13),
        '13': (4, 14),
        '14': (3, 15),
        '15': (2, 16),
        '16': (1, 17),
        '17': (0, 18),
        '18': (19, 26),

        '21': (7, 13),
        '22': (6, 14),
        '23': (5, 15),
        '24': (4, 16),
        '25': (3, 17),
        '26': (2, 18),
        '27': (1, 19),
        '28': (0, 20),

        '31': (8, 14),
        '32': (7, 15),
        '33': (6, 16),
        '34': (5, 17),
        '35': (4, 18),
        '36': (3, 19),
        '37': (2, 20),
        '38': (1, 21),

        '41': (9, 15),
        '42': (8, 16),
        '43': (7, 17),
        '44': (6, 18),
        '45': (5, 19),
        '46': (4, 20),
        '47': (3, 21),
        '48': (2, 22),

        '51': (10, 16),
        '52': (9, 17),
        '53': (8, 18),
        '54': (7, 19),
        '55': (6, 20),
        '56': (5, 21),
        '57': (4, 22),
        '58': (3, 23),

        '61': (11, 17),
        '62': (10, 18),
        '63': (9, 19),
        '64': (8, 20),
        '65': (7, 21),
        '66': (6, 22),
        '67': (5, 23),
        '68': (4, 24),

        '71': (12, 18),
        '72': (11, 19),
        '73': (10, 20),
        '74': (9, 21),
        '75': (8, 22),
        '76': (7, 23),
        '77': (6, 24),
        '78': (5, 25),

        '81': (19, 27),
        '82': (12, 20),
        '83': (11, 21),
        '84': (10, 22),
        '85': (9, 23),
        '86': (8, 24),
        '87': (7, 25),
        '88': (6, 27)
    }

    chromosome = []

    fitness = None

    def __init__(self, mutation_chance, parent1=None, parent2=None):
        """Initializes a new chess board with random queen locations."""

        # Set mutation chance
        self.mutation_chance = mutation_chance

        # Generate using genetics
        if parent1 is not None and parent2 is not None:
            self.chromosome = self.create_child(parent1.chromosome, parent2.chromosome)
        # If only one parent is None, throw error as this should never occur
        elif (parent1 is not None and parent2 is None) or (parent1 is None and parent2 is not None):
            raise ValueError('One of the given parents was None', parent1, parent2)
        # Create a random chess board
        else:
            self.chromosome = random.sample(range(1, 9), 8)

        # Calculate the fitness of the board
        self.check_collisions()

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

        diagonal_collision_list = [0] * 28

        # The number of collisions that have occurred.
        collisions = 0

        # Loop through each gene to determine its diagonal
        for index, gene in enumerate(self.chromosome):
            # Get diagonals
            diagonals = ChessBoard.lookup_table['{}{}'.format(index + 1, gene)]
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

    def create_child(self, parent1, parent2):
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
        if roll < self.mutation_chance:
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
