import numpy as np
import pandas as pd

from edgecompare import compare_edges  # , euclidean_distance

table = pd.read_csv("./data-verified.tsv", delimiter="\t", lineterminator="\n")

pieces = {
    # white
    "Bw": 1,
    "Kw": 2,
    "Nw": 3,
    "Pw": 4,
    "Qw": 5,
    "Rw": 6,
    # black
    "Bb": 7,
    "Kb": 8,
    "Nb": 9,
    "Pb": 10,
    "Qb": 11,
    "Rb": 12,
}

# get unique frequencies
frequencies = table["frequency"].unique()
frequencies.sort()
# print("Unique frequencies:", len(frequencies))
# for i in frequencies:
#     print(i)

# pandas code to drop duplicate entries - ignoring frequency for now (I don't trust data integrity in that column)
trim_table = table.drop_duplicates(subset=["board", "fill", "hasQR"], keep="first")
# print(trim_table.shape)



# grab the column we need for mass_list specifically
mass_list_pd = trim_table["board"]
mass_list_np = mass_list_pd.to_numpy()
# print(mass_list_np)

# make the complete mass_list
mass_list = []
# for each row of the numpy table
for row in mass_list_np:
    arr = row.split(",")
    board = np.zeros((64))
    for index, piece in enumerate(arr):
        if piece != "":
            board[index] = pieces[piece]
    board = board.reshape((8, 8))
    mass_list.append(board)

mass_list_hash = {} #dictionary because apparently that's python's best hash table
for i in range(len(mass_list)): 
    mass_list_hash[table.iloc[i, table.columns.get_loc('id')]] = mass_list[i]


# print(mass_list[0])
print(compare_edges(mass_list[0], mass_list))
