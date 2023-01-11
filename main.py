import pygame
from pygame.locals import *

import numpy as np
import os
import psutil
import random
import sys
import timeit


from object3d import Cube


# TODO: better take out stuff out of main loop and cube (e.g. in renderer), add depth (z coordinate)


WIN_SIZE = 1280, 720
WIN_WIDTH, WIN_HEIGHT = WIN_SIZE
TARGET_FPS = 120


PROJECTION_MATRIX = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
])


def get_rotation_x_matrix(angle):
    return np.array([
        [1, 0, 0],
        [0, np.cos(angle), -np.sin(angle)],
        [0, np.sin(angle), np.cos(angle)]
    ])

def get_rotation_y_matrix(angle):
    return np.array([
        [np.cos(angle), 0, np.sin(angle)],
        [0, 1, 0],
        [-np.sin(angle), 0, np.cos(angle)]
    ])

def get_rotation_z_matrix(angle):
    return np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])


class Application:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("3D Projection")
        self.screen = pygame.display.set_mode(WIN_SIZE)
        self.pid = os.getpid()
        self.process = psutil.Process(self.pid)
        print(f"Starting app... (PID {self.pid})")
        self.process_stats_timer = 0
        self.is_running = False

        # project specific stuff
        # self.cube = Cube((WIN_WIDTH / 2, WIN_HEIGHT / 2, 0), 250)
        # print(f"One cube is about {sys.getsizeof(self.cube)} bytes in memory")

        self.cubes = [Cube((random.uniform(0, WIN_WIDTH),                   # x
                            random.uniform(0, WIN_HEIGHT),                  # y
                            0),                                             # z
                           random.uniform(25, 250),                         # scale
                           random.uniform(0, 359)) for _ in range(100)]     # angle

    def run(self):
        self.is_running = True
        while self.is_running:

            frame_time_ms = self.clock.tick(TARGET_FPS)
            frame_time_s = frame_time_ms / 1000.

            self.process_stats_timer += frame_time_ms
            if self.process_stats_timer > 1000:
                print(f"CPU: {self.process.cpu_percent()}%\t"
                      f"RAM: {self.process.memory_info().rss / float(2**20):.2f} MB\t"
                      f"FPS: {int(self.clock.get_fps())}")
                self.process_stats_timer = 0

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.stop()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.stop()

            # updates
            for cube in self.cubes:
                cube.angle += 0.25 * np.pi * frame_time_s

            # projected vertices are temporal
            projected_vertices_list = []
            for cube in self.cubes:
                projected_vertices = cube.vertices * cube.scale  # could be in init to save some calculations
                projected_vertices = projected_vertices.dot(get_rotation_x_matrix(cube.angle))
                projected_vertices = projected_vertices.dot(get_rotation_y_matrix(cube.angle))
                projected_vertices = projected_vertices.dot(get_rotation_z_matrix(cube.angle))
                projected_vertices += cube.center
                projected_vertices = projected_vertices.dot(PROJECTION_MATRIX)[:, :2]
                projected_vertices_list.append(projected_vertices)
            # print(self.projected_vertices)

            # drawings
            self.screen.fill((255, 255, 255))
            # connections
            for i, cube in enumerate(self.cubes):
                for connection in cube.edges:
                    pygame.draw.line(self.screen, (0, 0, 0),
                                     projected_vertices_list[i][connection[0]],
                                     projected_vertices_list[i][connection[1]])
                # vertices
                # for vertex in self.projected_vertices:
                #     pygame.draw.circle(self.screen, (0, 0, 0), (int(vertex[0]), int(vertex[1])), 1)
            pygame.display.update()

    def stop(self):
        self.is_running = False


if __name__ == '__main__':
    # cast vs format time comparison
    # cast_time = timeit.timeit("print(f'{int(112.15)}')")
    # format_time = timeit.timeit("print(f'{112.15:.0f}')")
    # print(f"Cast time: {cast_time}\tFormat time: {format_time}")
    # print(f"Cast is {format_time / cast_time:.2f} times faster than format")  # 5% faster to cast
    Application().run()
