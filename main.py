from chess_board import ChessBoard
import numpy as np
from threading import Thread
import sys


def run_genetic_algorithm(population_size, mutation_chance, number_of_children):
    """Runs a genetic algorithm.

    Args:
        population_size (int): The size of the population to create
        mutation_chance (int): The chance in which a mutation can occur. Value between 0 and 1.
        number_of_children (int): The number of children to breed each round.
    """

    # Create the weighted probability for roulette wheel selection to be used in breeding
    breed_weights = [0.4, 0.2, 0.15, 0.15, 0.1]

    # Create the population
    population = []
    for i in range(population_size):
        population.append(ChessBoard(mutation_chance))

    # Loop endlessly to run the genetic algorithm
    while True:
        # Sort population by fitness, with most fit candidates first in the list
        population.sort(reverse=True)
        # Check the list to see if any of the population is a solution
        for board in population:
            # Checks to see if the board is a solution
            if board:
                # TODO add to solution list
                pass
            # Breaks if the current board was not a solution, as nothing after it in the sorted list will be
            else:
                break

    # Pick the parents for the next generation
    # TODO
    pass


if __name__ == '__main__':
    # Get population size and mutation chance
    if len(sys.argv) != 4:
        print('Please give population size, mutation chance, and thread count as command line arguments')
        exit(-1)
    size = sys.argv[1]
    chance = sys.argv[2]
    thread_count = sys.argv[3]

    # The list of solutions that were found
    solutions = []

    # Create threads for the different populations equal to the number given
    # TODO
    pass
