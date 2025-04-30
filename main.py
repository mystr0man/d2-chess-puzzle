import numpy as np
import csv

# from .edgecompare import compare_edges, euclidian_distance

data_file = "data.tsv"

# Read the TSV file
with open(data_file, "r") as file:
    reader = csv.reader(file, delimiter="\t")

    # get "board" column only
    board_column = [row[2] for row in reader]

pieces = {
    # white
    "Bw": 0,
    "Kw": 1,
    "Nw": 2,
    "Pw": 3,
    "Qw": 4,
    "Rw": 5,
    # black
    "Bb": 6,
    "Kb": 7,
    "Nb": 8,
    "Pb": 9,
    "Qb": 10,
    "Rb": 11,
    "": None,
}

for row in board_column[1:]:
    row_pieces = row.split(",")
    for i in range(len(row_pieces)):
        row_pieces[i] = pieces[row_pieces[i]]
    # create a 2d array
    row_pieces = np.array(row_pieces).reshape(8, 8)
    print(row_pieces)
