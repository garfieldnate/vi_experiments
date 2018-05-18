import sys

# Argument: path to wikipedia_unigrams.txt (from previous project)

def main():
    file = sys.argv[1]
    total_length = 0
    total_tokens = 0
    with open(file, 'r') as f:
        for line in f:
            word, freq = line.split("\t")
            total_tokens += int(freq)
            total_length += len(word) * int(freq)

    print(f"Normalized character total: {total_length}")
    print(f"Tokens: {total_tokens}")
    print(f"Average: {total_length / total_tokens}")

if __name__ == '__main__':
    main()
