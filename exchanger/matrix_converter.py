import numpy as np


def l2r(array):
    flattened = []
    for i, row in enumerate(array):
        if i % 2 != 0:
            row = np.flip(row)
        for j, cell in enumerate(row):
            flattened.append(cell)
    return flattened


def flatten(matrix, order):
    flattened = []
    match order:
        case 'ul2r':  # beginning up left to right
            flattened = l2r(matrix)
        case 'dl2r':  # beginning down left to right
            flattened = l2r(np.flipud(matrix))
        case 'ur2l':
            flattened = l2r((np.fliplr(matrix)))
        case 'dr2l':
            flattened = l2r(np.flipud(np.fliplr(matrix)))
        case 'ul2d':
            flattened = l2r(matrix.T)
        case 'ur2d':
            flattened = l2r(np.flipud(matrix.T))
        case 'dl2u':
            flattened = l2r((np.fliplr(matrix.T)))
        case 'dr2u':
            flattened = l2r(np.flipud(np.fliplr(matrix.T)))
        case _:
            raise NotImplementedError("Flattening order not defined")
    return flattened


def list_2_tuplelist(list):
    return [(list[i], list[i + 1]) for i in range(len(list) - 1)]


def id_repr(matrix):
    vectorized_get_id = np.vectorize(lambda obj: id(obj))
    output = vectorized_get_id(matrix)
    return output


def heat_flow_repr(matrix):
    vectorized_get_heat_flow = np.vectorize(lambda obj: obj.heat_flows[0])
    output = vectorized_get_heat_flow(matrix)
    return output
