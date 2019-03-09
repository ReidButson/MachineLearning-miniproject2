import random


class ChessBoard:
    """Class representing a chess board. The chess board contains a list of queens on the chess board."""

    # Create the lists to store values, allowing us to check for clashes easily
    # Positive slope lists
    a7p = []
    a6p = []
    a5p = []
    a4p = []
    a3p = []
    a2p = []
    a1p = []
    b1p = []
    c1p = []
    d1p = []
    e1p = []
    f1p = []
    g1p = []
    # Negative slope lists
    a2n = []
    a3n = []
    a4n = []
    a5n = []
    a6n = []
    a7n = []
    a8n = []
    b8n = []
    c8n = []
    d8n = []
    e8n = []
    f8n = []
    g8n = []

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

        lookup_table = self.generate_lookup()

        # The number of collisions that have occurred.
        collisions = 0

        # Loop through each gene to determine its diagonal
        for index, gene in enumerate(self.chromosome):
            # Get diagonals
            diagonals = lookup_table['{}{}'.format(index + 1, gene)]
            # Determine collisions in diagonals
            for diagonal in diagonals:
                diagonal.append((index + 1, gene))
                # Increment collisions if applicable
                if len(diagonal) > 1:
                    collisions += len(diagonal) - 1

        # The maximum number of collisions that can occur is 28, so inverse for fitness
        self.fitness = 28 - collisions

        return collisions

    def generate_lookup(self):
        """Generates the lookup table that is to be used when checking collisions at board creation time.

        Returns:
            dict: The dictionary
        """
        return {
            '11': (self.a1p, ),
            '12': (self.a2p, self.a2n),
            '13': (self.a3p, self.a3n),
            '14': (self.a4p, self.a4n),
            '15': (self.a5p, self.a5n),
            '16': (self.a6p, self.a6n),
            '17': (self.a7p, self.a7n),
            '18': (self.a8n, ),

            '21': (self.b1p, self.a2n),
            '22': (self.a1p, self.a3n),
            '23': (self.a2p, self.a4n),
            '24': (self.a3p, self.a5n),
            '25': (self.a4p, self.a6n),
            '26': (self.a5p, self.a7n),
            '27': (self.a6p, self.a8n),
            '28': (self.a7p, self.b8n),

            '31': (self.c1p, self.a3n),
            '32': (self.b1p, self.a4n),
            '33': (self.a1p, self.a5n),
            '34': (self.a2p, self.a6n),
            '35': (self.a3p, self.a7n),
            '36': (self.a4p, self.a8n),
            '37': (self.a5p, self.b8n),
            '38': (self.a6p, self.c8n),

            '41': (self.d1p, self.a4n),
            '42': (self.c1p, self.a5n),
            '43': (self.b1p, self.a6n),
            '44': (self.a1p, self.a7n),
            '45': (self.a2p, self.a8n),
            '46': (self.a3p, self.b8n),
            '47': (self.a4p, self.c8n),
            '48': (self.a5p, self.d8n),

            '51': (self.e1p, self.a5n),
            '52': (self.d1p, self.a6n),
            '53': (self.c1p, self.a7n),
            '54': (self.b1p, self.a8n),
            '55': (self.a1p, self.b8n),
            '56': (self.a2p, self.c8n),
            '57': (self.a3p, self.d8n),
            '58': (self.a4p, self.e8n),

            '61': (self.f1p, self.a6n),
            '62': (self.e1p, self.a7n),
            '63': (self.d1p, self.a8n),
            '64': (self.c1p, self.b8n),
            '65': (self.b1p, self.c8n),
            '66': (self.a1p, self.d8n),
            '67': (self.a2p, self.e8n),
            '68': (self.a3p, self.f8n),

            '71': (self.g1p, self.a7n),
            '72': (self.f1p, self.a8n),
            '73': (self.e1p, self.b8n),
            '74': (self.d1p, self.c8n),
            '75': (self.c1p, self.d8n),
            '76': (self.b1p, self.e8n),
            '77': (self.a1p, self.f8n),
            '78': (self.a2p, self.g8n),

            '81': (self.a8n, ),
            '82': (self.g1p, self.b8n),
            '83': (self.f1p, self.c8n),
            '84': (self.e1p, self.d8n),
            '85': (self.d1p, self.e8n),
            '86': (self.c1p, self.f8n),
            '87': (self.b1p, self.g8n),
            '88': (self.a1p, )
        }

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
        mutation_point = random.randint(0, len(chromosome))

        # Swaps the two genes, note any list at -1 is the last element in the list so no out of bound check is required
        chromosome[mutation_point], chromosome[mutation_point - 1] = chromosome[mutation_point - 1], chromosome[
            mutation_point]

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
