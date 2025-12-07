import numpy as np

Mat = np.ndarray


def sort_points(shape: Mat) -> list[Mat]:
    points = shape.reshape(4, 2)
    sums = points.sum(axis=1)
    diffs = np.diff(points, axis=1)

    top_left = np.argmin(sums)
    bottom_right = np.argmax(sums)
    top_right = np.argmin(diffs)
    bottom_left = np.argmax(diffs)

    return [
        points[top_left],
        points[top_right],
        points[bottom_right],
        points[bottom_left],
    ]
