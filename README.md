# N-Queens Genetic Algorithm Solution Finder
The following program is used to display all solutions for n-queen problems. 
The application allows for variables to be set from running in the command line, and outputs all solutions that it finds
into the terminal window.  It will time how long it took to find the last solution it found, and give up on finding
solutions after a specified amount of time has passed (applicable to higher n problems).

# Usage
To use, you can simply run main.py.  If no variables are passed in the command line, default values will be used for all
the inputs.  You can overwrite these defaults by passing them in the command line.

Below is the help page for the program, achieved by running `main.py -h`.
~~~~
usage: main.py [-h] [-m MUTATION_CHANCE] [-c CHILDREN_PER_GEN] [-p POP_SIZE]
               [-t THREAD_COUNT] [-n N_QUEENS] [-r RESET]

Runs the n-queen problem with given values, or defaults in case of missing
values

optional arguments:
  -h, --help            show this help message and exit
  -m MUTATION_CHANCE, --mutation_chance MUTATION_CHANCE
                        the mutation chance to use, which defaults to 0.02
  -c CHILDREN_PER_GEN, --children_per_gen CHILDREN_PER_GEN
                        the number of children to create each generation,
                        which must be less than half of the given population.
                        Defaults to 400
  -p POP_SIZE, --pop_size POP_SIZE
                        the size of populations to create, defaulting to 1000
  -t THREAD_COUNT, --thread_count THREAD_COUNT
                        the number of threads to create, defaulting to 1
  -n N_QUEENS, --n_queens N_QUEENS
                        the number of queens in the problem, defaulting to 8
  -r RESET, --reset RESET
                        the number of generations to run in a population
                        before resetting to a new population, defaulting to
                        250
~~~~
