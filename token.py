import sys

if len(sys.argv) != 3:
    print("Usage: token.py <input filename> <output filename>")
    sys.exit(1)

input_filename = sys.argv[1]
output_filename = sys.argv[2]

try:
    with open(input_filename, "r") as i, open(output_filename, "w") as o:
        for line in i:
            tokens = line.split()
            for token in tokens:
                if token.isalpha() or token.isdigit():
                    o.write(token + "\n")
except Exception as e:
    print(e)
    sys.exit(1)