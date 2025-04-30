import numpy as np


def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    distance = np.linalg.norm(a - b)
    return float(distance)


def compare_edges(grid: np.ndarray):
    # dummy numbers to be compared to
    best_top_dist = 9999
    best_bottom_dist = 9999
    best_left_dist = 9999
    best_right_dist = 9999
    # to be replaced; tracks index of best pair on that edge
    best_top_index = -1
    best_bottom_index = -1
    best_left_index = -1
    best_right_index = -1
    # finds each edge of the 2d array
    self_top_edge = np.ndarray.flatten(grid[0, :])  # first row
    self_bottom_edge = np.ndarray.flatten(grid[-1, :])  # last row
    self_left_edge = np.ndarray.flatten(grid[:, 0])  # first column
    self_right_edge = np.ndarray.flatten(grid[:, -1])  # last column

    # list comprehension to eliminate self from mass list when called, then iterate through it
    self_removed = [item for item in mass_list if not np.array_equal(item, grid)]
    for i in range(len(self_removed)):
        # repeat the process with grid, but for other, which is the other array being compared to
        other = self_removed[i]
        other_top_edge = np.ndarray.flatten(other[0, :])  # first row
        other_bottom_edge = np.ndarray.flatten(other[-1, :])  # last row
        other_left_edge = np.ndarray.flatten(other[:, 0])  # first column
        other_right_edge = np.ndarray.flatten(other[:, -1])  # last column

        # if the current best distance to that direction is that one (said well me), update to that
        if euclidian_distance(self_top_edge, other_bottom_edge) < best_top_dist:
            best_top_dist = euclidian_distance(self_top_edge, other_bottom_edge)
            # enumerate because .index() doesnt work for arrays
            for j, arr in enumerate(mass_list):
                if np.array_equal(arr, other):
                    best_top_index = j
        elif euclidian_distance(self_bottom_edge, other_top_edge) < best_bottom_dist:
            best_bottom_dist = euclidian_distance(self_bottom_edge, other_top_edge)
            # enumerate because .index() doesnt work for arrays
            for j, arr in enumerate(mass_list):
                if np.array_equal(arr, other):
                    best_bottom_index = j
        elif euclidian_distance(self_left_edge, other_right_edge) < best_left_dist:
            best_left_dist = euclidian_distance(self_left_edge, other_right_edge)
            # enumerate because .index() doesnt work for arrays
            for j, arr in enumerate(mass_list):
                if np.array_equal(arr, other):
                    best_left_index = j
        elif euclidian_distance(self_right_edge, other_left_edge) < best_right_dist:
            best_right_dist = euclidian_distance(self_right_edge, other_left_edge)
            # enumerate because .index() doesnt work for arrays
            for j, arr in enumerate(mass_list):
                if np.array_equal(arr, other):
                    best_right_index = j
    print("best top distance: " + str(best_top_dist))
    print("best bottom distance: " + str(best_bottom_dist))
    print("best left distance: " + str(best_left_dist))
    print("best right distance: " + str(best_right_dist))
    return best_top_index, best_bottom_index, best_left_index, best_right_index


if __name__ == "__main__":
    mass_list = [
        np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
        np.array([[-1, -1, -1], [-1, -1, -1], [1, 2, 3]]),
        np.array([[-1, 8, 11], [4, 12, -1], [7, 3, -333]]),
    ]
    print(compare_edges(mass_list[0]))
