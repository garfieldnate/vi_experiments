# Generate random tuples (web queries) from a word list
# Apparently the same method for generating web queries as is used in BootCat

import argparse
import sys
import random

def get_random_tuple(seeds, order=3):
    picked = set()
    seed = random.choice(seeds)
    for _ in range(order):
        while seed in picked and len(picked) < order:
            seed = random.choice(seeds)
        picked.add(seed)

    sorted_tuple = list(picked)
    sorted_tuple.sort()
    return ' '.join(sorted_tuple)

def generate_queries(seeds, order=3, num_tuples=10):
    queries = set()
    while len(queries) < num_tuples:
        queries.add(get_random_tuple(seeds, order))
    return queries


def main():
    parser = argparse.ArgumentParser(description='Generate random tuples from word list')
    parser.add_argument('word_file', help='Path to file containing words, one per line')
    parser.add_argument('order', type=int, help='Size of n-tuples to generate')
    parser.add_argument('num_tuples', type=int, help='Size of list of n-tuples to generate')
    parser.add_argument('-s', '--seed_random', type=int, default=0, help="Number to seed Python's pseud-random number generator with")
    args = vars(parser.parse_args())
    if all([not args[x] for x in ['word_file', 'order', 'num_tuples']]):
        parser.print_help()
        exit(1)

    with open(args['word_file']) as f:
        seeds = f.readlines()
    seeds = [s.strip() for s in seeds]
    random.seed(args['seed_random'])

    # optimial order for Vietnamese was 4
    queries = list(generate_queries(seeds, args['order'], args['num_tuples']))
    queries.sort()
    print("\n".join(queries))


if __name__ == '__main__':
    main()
