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

    # Create the initial population
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
        parents = []
        for i in range(number_of_children * 2):
            # Select the portion of the population to grab a parent from
            portion = np.random.choice([0, 1, 2, 3, 4], p=breed_weights)
            # Select the parent from the designated portion
            parent_index = np.random.choice(range(
                int(portion * len(population) / 5), int((portion + 1) * len(population) / 5)
            ))
            # Parents are removed so they cannot be selected again, and will be added later
            parents.append(population.pop(parent_index))

        # Breed new children with the parents
        children = []
        for i in range(number_of_children):
            # Create the new child
            children.append(
                ChessBoard(mutation_chance, parent1=parents[i], parent2=parents[0 - (i + 1)])
            )

        # Add the parents back into the population
        population += parents

        # Delete a number of boards from the population equal to the number of children to be added from the bottom half
        for i in range(number_of_children):
            population.pop(np.random.randint(-int(len(population) / 2), -1))

        # Add the children to the population to replace the killed population
        population += children


def main():
    # Get population size and mutation chance
    if len(sys.argv) != 5:
        print('Please give population size, mutation chance, number of children each generation, and thread count as '
              'command line arguments in that order')
        exit(-1)
    size = int(sys.argv[1])
    chance = float(sys.argv[2])
    thread_count = int(sys.argv[3])
    num_children = int(sys.argv[4])

    # The list of solutions that were found
    solutions = []

    # Create threads for the different populations equal to the number given
    threads = []
    for i in range(thread_count):
        new_thread = Thread(target=run_genetic_algorithm, args=(size, chance, num_children))
        # Start the thread, and add it to the thread list
        new_thread.start()
        threads.append(new_thread)


if __name__ == '__main__':
    main()
