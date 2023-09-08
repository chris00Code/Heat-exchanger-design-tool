import numpy as np
from matplotlib import patheffects


def l2r(array):
    flattened = []
    for i, row in enumerate(array):
        if i % 2 != 0:
            row = np.flip(row)
        try:
            for j, cell in enumerate(row):
                flattened.append(cell)
        except TypeError:
            flattened.append(row)
    return flattened


def flatten(matrix, order):
    flattened = []
    if isinstance(order, str):
        if isinstance(matrix, np.ndarray):
            if matrix.ndim == 1:
                match order[-3]:
                    case 'r':
                        for ex in reversed(matrix):
                            flattened.append(ex)
                    case 'l':
                        for ex in matrix:
                            flattened.append(ex)
            else:
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
        else:
            raise NotImplementedError
    else:
        raise NotImplementedError


def list_2_tuplelist(list):
    return [(list[i], list[i + 1]) for i in range(len(list) - 1)]


def id_repr(matrix):
    vectorized_get_id = np.vectorize(lambda obj: id(obj))
    output = vectorized_get_id(matrix)
    return output


def heat_flow_repr(matrix):
    vectorized_get_heat_flow = np.vectorize(lambda obj: abs(obj.heat_flows[0]))
    output = vectorized_get_heat_flow(matrix)
    return output


def add_arrows(ax, direction_list, start_point,text="", color='black'):

    for i,direction in enumerate(direction_list):

        end_point = start_point.copy()
        match len(direction):
            case 1:
                add = 1
            case 2:
                add = 0.5

        arrow_connectionstyle = "angle3"
        match direction[0]:
            case 'd':
                end_point[1] += add
            case 'u':
                end_point[1] -= add
            case 'l':
                end_point[0] -= add
                arrow_connectionstyle = "angle3,angleA=0, angleB=-90"
            case 'r':
                end_point[0] += add
                arrow_connectionstyle = "angle3,angleA=0, angleB=90"
        if len(direction) == 2:
            match direction[1]:
                case 'd':
                    end_point[1] += add
                case 'u':
                    end_point[1] -= add
                case 'l':
                    end_point[0] -= add
                case 'r':
                    end_point[0] += add

        start_point = tuple(start_point)
        end_point = tuple(end_point)



        txt = ax.annotate("", end_point, start_point,
                          arrowprops=dict(arrowstyle="->", connectionstyle=arrow_connectionstyle, lw=2, color=color),
                          size=20, ha="center", path_effects=[patheffects.withStroke(linewidth=3, foreground="w")])

        txt.arrow_patch.set_path_effects([
            patheffects.Stroke(linewidth=4, foreground="w"),
            patheffects.Normal()])

        if i ==0:
            ax.text(start_point[0]+0.05,start_point[1]-0.05,text,color=color,fontsize=12)


        start_point = list(end_point)



def get_direction_list(matrix, order):
    shape = matrix.shape
    direction_list = [order[-1]]
    n_same = (shape[0] - 2, shape[1] - 2)

    others = {'u': 'd', 'd': 'u', 'r': 'l', 'l': 'r'}

    if order[-1] in ['u', 'd']:
        _arrow_direction(direction_list, order[1], shape[1], order, others, n_same[0])
        match order[1]:
            case 'l':
                x = 0
            case 'r':
                x = shape[1] - 1
        match order[0]:
            case 'u':
                y = -0.5
            case 'd':
                y = shape[0] - 0.5
    elif order[-1] in ['r', 'l']:
        _arrow_direction(direction_list, order[0], shape[0], order, others, n_same[1])
        match order[1]:
            case 'l':
                x = -0.5
            case 'r':
                x = shape[1] - 0.5
        match order[0]:
            case 'u':
                y = 0
            case 'd':
                y = shape[0] - 1
    start_point = [x, y]

    return start_point, direction_list


def _arrow_direction(direction_list, arrow_direction, length, order, others, n_same):
    for i in range(length):
        if i % 2 == 0:
            filler = order[-1]
        else:
            filler = others[order[-1]]
        direction_list += [filler] * n_same
        if i < length - 1:
            direction_list.append(filler + others[arrow_direction])
            direction_list.append(others[arrow_direction] + others[filler])
    if length % 2 == 0:
        direction_list += others[order[-1]]
    else:
        direction_list += order[-1]
