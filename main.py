import pygame
from pygame.locals import *

import numpy as np
import os
import psutil
import sys


from object3d import Cube


# TODO: better take out stuff out of main loop and cube (e.g. in renderer)


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
        self.cube = Cube((WIN_WIDTH / 2, WIN_HEIGHT / 2, 0), 250)
        print(f"One cube is about {sys.getsizeof(self.cube)} bytes in memory")

    def run(self):
        self.is_running = True
        while self.is_running:

            frame_time_ms = self.clock.tick(TARGET_FPS)
            frame_time_s = frame_time_ms / 1000.

            self.process_stats_timer += frame_time_ms
            if self.process_stats_timer > 1000:
                print(f"CPU: {self.process.cpu_percent()}%\t"
                      f"RAM: {self.process.memory_info().rss / float(2**20):.2f} MB\t"
                      f"FPS: {self.clock.get_fps():.2f}")
                self.process_stats_timer = 0

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.stop()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.stop()

            # updates
            self.cube.angle += 0.25 * np.pi * frame_time_s

            # projected vertices are temporal
            projected_vertices = self.cube.vertices * self.cube.scale  # could be in init to save some calculations
            projected_vertices = projected_vertices.dot(get_rotation_x_matrix(self.cube.angle))
            projected_vertices = projected_vertices.dot(get_rotation_y_matrix(self.cube.angle))
            projected_vertices = projected_vertices.dot(get_rotation_z_matrix(self.cube.angle))
            projected_vertices += self.cube.center
            projected_vertices = projected_vertices.dot(PROJECTION_MATRIX)[:, :2]
            # print(self.projected_vertices)

            # drawings
            self.screen.fill((255, 255, 255))
            # connections
            for connection in self.cube.edges:
                pygame.draw.line(self.screen, (0, 0, 0),
                                 projected_vertices[connection[0]],
                                 projected_vertices[connection[1]])
            # vertices
            # for vertex in self.projected_vertices:
            #     pygame.draw.circle(self.screen, (0, 0, 0), (int(vertex[0]), int(vertex[1])), 1)
            pygame.display.update()

    def stop(self):
        self.is_running = False


if __name__ == '__main__':
    Application().run()
