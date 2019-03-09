from chess_board import ChessBoard
import random
import timeit
import time

def test_ours():
    board = ChessBoard(0.2)
    board.check_collisions()
    return board.fitness

def test_theirs():
    chromosome = random.sample(range(1, 9), 8)
    fitness = 0
    for i in range(len(chromosome)):
        for j in range(i + 1, len(chromosome)):
            if (abs(chromosome[i] - chromosome[j] == (j - i))):
                fitness += 1
    return fitness

def sleepy():
    time.sleep(0.1)
    return True

lookup_table = {
        '11': (7, 0),
        '12': (6, 15),
        '13': (5, 16),
        '14': (4, 17),
        '15': (3, 18),
        '16': (2, 19),
        '17': (1, 20),
        '18': (21, 0),

        '21': (8, 15),
        '22': (7, 16),
        '23': (6, 17),
        '24': (5, 18),
        '25': (4, 19),
        '26': (3, 20),
        '27': (2, 21),
        '28': (1, 22),

        '31': (9, 16),
        '32': (8, 17),
        '33': (7, 18),
        '34': (6, 19),
        '35': (5, 20),
        '36': (4, 21),
        '37': (3, 22),
        '38': (2, 23),

        '41': (10, 17),
        '42': (9, 18),
        '43': (8, 19),
        '44': (7, 20),
        '45': (6, 21),
        '46': (5, 22),
        '47': (4, 23),
        '48': (3, 24),

        '51': (11, 18),
        '52': (10, 19),
        '53': (9, 20),
        '54': (8, 21),
        '55': (7, 22),
        '56': (6, 23),
        '57': (5, 24),
        '58': (4, 25),

        '61': (12, 19),
        '62': (11, 20),
        '63': (10, 21),
        '64': (9, 22),
        '65': (8, 23),
        '66': (7, 24),
        '67': (6, 25),
        '68': (5, 26),

        '71': (13, 20),
        '72': (12, 21),
        '73': (11, 22),
        '74': (10, 23),
        '75': (9, 24),
        '76': (8, 25),
        '77': (7, 26),
        '78': (6, 27),

        '81': (21, 0),
        '82': (13, 22),
        '83': (12, 23),
        '84': (11, 24),
        '85': (10, 25),
        '86': (9, 26),
        '87': (8, 27),
        '88': (7, 14)
    }

def generate_lookup():
    diagonals = [0]*28

    chromosome = random.sample(range(1, 9), 8)

    # The number of collisions that have occurred.
    collisions = 0
    # Loop through each gene to determine its diagonal
    for index, gene in enumerate(chromosome):
        # Get diagonals
        id = lookup_table['{}{}'.format(index + 1, gene)]
        # Determine collisions in diagonals

        diagonals[id[0]] += 1
        diagonals[id[1]] += 1

        if diagonals[id[0]] > 1:
            collisions += diagonals[id[0]] -1

        if diagonals[id[1]] > 1:
            collisions += diagonals[id[1]] -1
        # Increment collisions if applicable

    # The maximum number of collisions that can occur is 28, so inverse for fitness
    return collisions, chromosome


x = timeit.timeit('generate_lookup()', number=1000000, setup='from __main__ import generate_lookup')

#print(timeit.timeit('test_ours()', number=50000, setup='from __main__ import test_ours'))

y = timeit.timeit('test_theirs()', number=1000000, setup='from __main__ import test_theirs')

print("\n\n{} <---- Your smelly double for loop (;´༎ຶД༎ຶ`)\n\n ༼ つ ͡° ͜ʖ ͡° ༽つ {} <---- Our Speedy boi lookup table\n".format(y, x))

if x > y:
    print("Fuck")

else:
    print("Fuck Yeah")

    print('       ___------__\n'
    '   |\__-- /\       _-\n'
    '   |/    __      -\n'
    '  //\  /  \    /__\n'
    '  |  o|  0|__     --_\n'
    '  \\\\____-- __ \   ___-\n'
    '  (@@    __/  / /_\n'
    '   -_____---   --_\n'
    '    //  \ \\\\   ___-\n'
    '  //|\__/  \\\\  \ \n'
    ' \_-\_____/  \-\ \n'
    '      // \\\\--\|   -Han J. Lee-\n'
    ' ____//  ||_\n'
    '/_____\ /___\ \n'
    '______________________\n')