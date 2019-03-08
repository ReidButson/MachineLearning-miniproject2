import random

def crossover(parent1, parent2):
    """
    creates a new child chromosome from two parents

    Args:
        parent1 (list): first chromosome
        parent2 (list): second chromosome

    Returns:
        list: a new chromosome from the parents genes
    """
    if len(parent1) != len(parent2):
        raise ValueError("Both Parents should have the same length")

    #Creates child as first half of parent1
    cross_point = random.randint(0, len(parent1))
    child_head = parent1[:cross_point]

    #takes remaining genes from second parent
    child_tail = [gene for gene in parent2 if gene not in child_head]

    return child_head + child_tail

def mutate(chromosome):
    """
    Mutates a chromosome by flipping two random genes

    Args:
        chromosome (list) the chromosome to mutate

    Returns:
        list: the original chromosome with two random genes flipped
    """
    if type(chromosome) != list:
        raise TypeError("Chromosomes should be of type list")

    # random element index
    mutation_point = random.randint(0, len(chromosome))

    # Swaps the two genes, note any list at -1 is the last element in the list so no out of bound check is required
    chromosome[mutation_point], chromosome[mutation_point - 1] = chromosome[mutation_point - 1], chromosome[mutation_point]

def createChild(parent1, parent2, mutate_chance):
    """
    creates a new child and mutates it based on the mutation probability

    Args:
        parent1 (list): first chromosome
        parent2 (list): second chromosome

        mutate_chance (float): probability of mutation between 0 and 1

    Returns:
        list: a new chromosome from the parents genes, possibly mutated
    """

    if mutate_chance < 0 or mutate_chance > 1:
        raise ValueError("Mutate probability should be between 0 and 1")

    if len(parent1) != len(parent2):
        raise ValueError("Length of parent chromosomes should be the same")

    child = crossover(parent1, parent2)

    # rolls a number between 0 and 1
    roll = random.random()

    # if roll is below the mutation probability it mutates the child
    if roll < mutate_chance:
        return mutate(child)

    else:
        return child


if __name__ == '__main__':
    print('hello')
