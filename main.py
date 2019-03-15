from chess_board import ChessBoard
import argparse
import numpy as np
from threading import Thread, Lock
from time import sleep, time


# The list of solutions to the n-queen problem
solutions = []
# The lock to use when adding solutions to the list of solutions
solution_lock = Lock()

# Create the weighted probability for roulette wheel selection to be used in breeding
breed_weights = [0.4, 0.2, 0.15, 0.15, 0.1]

# The time the last solution was found, for use in outputting the time it took to complete the program
# Updated whenever a new solution has been found
last_solution = None


def run_genetic_algorithm(population_size, number_of_children, reset):
    """Runs a genetic algorithm.

    Args:
        population_size (int): The size of the population to create.
        number_of_children (int): The number of children to breed each round.
        reset (int): The number of generations to reset after.
    """

    # Loop endlessly
    while True:
        # Create the initial population
        population = []
        for i in range(population_size):
            population.append(ChessBoard())

        generation_num = 1

        # Loop until the reset number is reached
        while generation_num <= reset:
            # Sort population by fitness, with most fit candidates first in the list
            population.sort(reverse=True)
            # Check the list to see if any of the population is a solution
            for board in population:
                # Checks to see if the board is a solution
                if bool(board):
                    add_solution(board.chromosome, generation_num)
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
                                                       # Parents are removed so they cannot be selected again, and will be added back later
                                                       parents.append(population.pop(parent_index))

            # Breed new children with the parents
            children = []
            for i in range(number_of_children):
                                                   # Create the new child
                                                   children.append(
                                                   ChessBoard(parent1=parents[i], parent2=parents[0 - (i + 1)])
                                                   )

            # Add the parents back into the population
            population += parents

            # Delete a number of boards from the population equal to the number of children to be added from the bottom
            # half
            for i in range(number_of_children):
                population.pop(np.random.randint(-int(len(population) / 2), -1))

            # Add the children to the population to replace the killed population
            population += children

            # Increase generation number
            generation_num += 1


def add_solution(solution, generation_num):
    """Adds a solution to the global list of solutions in a thread-safe manner, checking for duplicates as well.

    Args:
        solution (list): The chessboard chromosome that is a solution to the problem.
        generation_num (list): The generation number the solution was found at.

    Todo:
        - Put the solutions into a csv file while the lock is acquired.
    """

    # Acquire the lock
    solution_lock.acquire()
    # Check for duplicates, inserting into the list if there are no duplicates
    if solution not in solutions:
        global last_solution
        last_solution = time()
        solutions.append(solution)
        print("solution found at generation {}: {}".format(generation_num, solution))
        print("there are now {} solutions found".format(len(solutions)))
    # Release the lock so the other threads can add solutions
    solution_lock.release()


def main():
    # Argument variable defaults
    mutation_chance_def = 0.02
    children_per_gen_def = 400
    pop_size_def = 1000
    thread_count_def = 1
    n_queens_def = 8
    reset_def = 250

    # Setup argument variable parser
    parser = argparse.ArgumentParser(description='Runs the n-queen problem with given values, or defaults in case of '
                                                 'missing values')
    parser.add_argument('-m', '--mutation_chance', help='the mutation chance to use, which defaults to {}'
                        .format(mutation_chance_def))
    parser.add_argument('-c', '--children_per_gen',
                        help='the number of children to create each generation, which must be less than half of the '
                             'given population. Defaults to {}'.format(children_per_gen_def))
    parser.add_argument('-p', '--pop_size', help='the size of populations to create, defaulting to {}'
                        .format(pop_size_def))
    parser.add_argument('-t', '--thread_count', help='the number of threads to create, defaulting to {}'
                        .format(thread_count_def))
    parser.add_argument('-n', '--n_queens', help='the number of queens in the problem, defaulting to {}'
                        .format(n_queens_def))
    parser.add_argument('-r', '--reset', help='the number of generations to run in a population before resetting to a '
                                              'new population, defaulting to {}'.format(reset_def))

    # Parse argument variables
    args = parser.parse_args()
    # Set mutation chance
    if args.mutation_chance:
        try:
            mutation_chance = float(args.mutation_chance)
            if mutation_chance <= 0 or mutation_chance > 1:
                raise ValueError
        except ValueError:
            print('mutation chance must be a float such that 0 < mutation chance <= 1')
            exit(-1)
    else:
        mutation_chance = mutation_chance_def
    # Set population size
    if args.pop_size:
        try:
            pop_size = int(args.pop_size)
            if pop_size <= 1:
                raise ValueError
        except ValueError:
            print('population size must be greater than 1')
            exit(-2)
    else:
        pop_size = pop_size_def
    # Set children per gen
    if args.children_per_gen:
        try:
            children_per_gen = int(args.children_per_gen)
            if children_per_gen * 2 > pop_size or children_per_gen <= 0:
                raise ValueError
        except ValueError:
            print('the number of children to generate must be less than half the population size and greater than 0')
            exit(-3)
    else:
        children_per_gen = children_per_gen_def
    # Set dimension of the problem
    if args.n_queens:
        try:
            n_queens = int(args.n_queens)
            if n_queens <= 0:
                raise ValueError
        except ValueError:
            print('the dimension of the problem must be greater than 0')
            exit(-4)
    else:
        n_queens = n_queens_def
    # Set the number of threads to use
    if args.thread_count:
        try:
            thread_count = int(args.thread_count)
            if thread_count <= 0:
                raise ValueError
        except ValueError:
            print('the thread count must be greater than 0')
            exit(-5)
    else:
        thread_count = thread_count_def
    if args.reset:
        try:
            reset = int(args.reset)
            if reset <= 0:
                raise ValueError
        except ValueError:
            print('the number of generations to reset after must be greater than 0')
            exit(-6)
    else:
        reset = reset_def

    # Setup static variables for the ChessBoard
    ChessBoard.setup_statics(dimensions=n_queens, mutation_chance=mutation_chance)

    # Genetic algorithm starts now, so the timer should start
    start_time = time()

    # Create threads for the different populations equal to the number requested
    threads = []
    for i in range(thread_count):
        new_thread = Thread(target=run_genetic_algorithm, args=(pop_size, children_per_gen, reset))
        # Start the thread, and add it to the thread list
        new_thread.start()
        threads.append(new_thread)

    # This loop will be exited after enough time has passed without a solution being found, terminating the
    # program
    finding_solutions = True
    while finding_solutions:
        # Save the size of the list to use to check if the solution list size has changed, to exit the program
        num_solutions = len(solutions)
        # Sleep to allow new updates
        sleep(120)
        # If the number of solutions hasn't increased, then end the program
        if num_solutions == len(solutions):
            finding_solutions = False

    # The program has finished
    print('The program found {} solutions, with these being the solutions:'.format(len(solutions)))
    for solution in solutions:
        print(solution)
    print('The program finished in approximately {} seconds'.format(last_solution - start_time))
    exit(0)


if __name__ == '__main__':
    main()
