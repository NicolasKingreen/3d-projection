import numpy as np


class Object3D:
    def __init__(self, center, scale, angle):
        self.center = center
        self.scale = scale
        self.angle = angle
        self.vertices = None
        self.edges = None


class Cube(Object3D):
    def __init__(self, center, scale, angle=0):
        super().__init__(center, scale, angle)
        self.vertices = np.array([
            # front
            [-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],
            [0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5],
            # back
            [-0.5, -0.5, -0.5],
            [0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
            [-0.5, 0.5, -0.5],
        ])
        self.edges = np.array([
            # front
            [0, 1], [1, 2], [2, 3], [3, 0],
            # back
            [4, 5], [5, 6], [6, 7], [7, 4],
            # sides
            [0, 4], [1, 5], [2, 6], [3, 7],
        ])

