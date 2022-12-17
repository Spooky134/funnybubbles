import math
import numpy as np


class Point:
    def __init__(self, point):
        self.number = point[0]+1
        self.x = point[1]
        self.y = point[2]
        self.z = point[3]

    def distance_to_point(self, point):
        return math.sqrt((point.x - self.x) ** 2
                         + (point.y - self.y) ** 2
                         + (point.z - self.z) ** 2)

    def distance_to_points(self, points):
        return np.array(list(map(self.distance_to_point, points)))

    def params(self):
        return np.array([self.number, self.x, self.y, self.z])

    @staticmethod
    def reformat(point):
        return Point(point)


class Cluster:
    def __init__(self, name, points=np.zeros(0)):
        self.name = name
        self.points = np.copy(points)
        self.__center = None
        self.distances = np.zeros(points.size)
        self.differences = np.zeros(points.size)

    @property
    def center(self):
        self.__center = Point([0, self.x.sum()/self.points.size,
                               self.y.sum()/self.points.size, self.z.sum()/self.points.size])
        return self.__center

    @property
    def x(self):
        return np.array([point.x for point in self.points])

    @property
    def y(self):
        return np.array([point.y for point in self.points])

    @property
    def z(self):
        return np.array([point.z for point in self.points])

    @property
    def number(self):
        return np.array([point.number for point in self.points])

    def params(self):
        return np.concatenate([self.number[:, None], self.x[:, None], self.y[:, None], self.z[:, None],
                               self.distances[:, None], self.differences[:, None]], axis=1)

    def max_cord(self, var='x'):
        coords = {'x': self.x, 'y': self.y, 'z': self.z}
        return np.max(coords[var])

    def min_cord(self, var='x'):
        coords = {'x': self.x, 'y': self.y, 'z': self.z}
        return np.min(coords[var])

    def radius(self, var='x'):
        return abs(self.max_cord(var) - self.min_cord(var))/2

    def cord_center(self, var='x'):
        return self.min_cord(var)+self.radius(var)

    def expected_size(self):
        rad = np.sort(np.array([self.radius('x'), self.radius('y'), self.radius('z')]))
        center_coords = np.array([self.cord_center('x'), self.cord_center('y'), self.cord_center('z')])
        return np.array(np.concatenate([center_coords, rad]))

    def add_point(self, point, distance):
        self.points = np.append(self.points, point)
        self.distances = np.append(self.distances, distance)
        if self.points.size > 2:
            self.differences = np.append(self.differences, abs(self.distances[-2]-self.distances[-1]))
        else:
            self.differences = np.append(self.differences, 0)

    def spectre(self, count):
        rem_points = self.points.copy()
        np.random.shuffle(rem_points)
        cluster = Cluster(name=0)
        cluster.add_point(rem_points[0], 0)
        rem_points = np.delete(rem_points, 0)

        while np.size(rem_points) != 0:
            distances = cluster.center.distance_to_points(rem_points)
            near_point = rem_points[np.argmin(distances)]
            near_point_distance = np.amin(distances)
            cluster.add_point(near_point, near_point_distance)
            rem_points = [point for point in rem_points if point.number != near_point.number]

        clusters_borders = self.special_max(cluster.differences, count - 1)
        clusters_borders = np.sort(clusters_borders)
        groups = np.split(cluster.points, clusters_borders)
        clusters = [Cluster(self.name+str(i), points) for i, points in enumerate(groups, 1)]
        self.differences = np.copy(cluster.differences)
        self.distances = np.copy(cluster.distances)
        return clusters

    @staticmethod
    def special_max(array, count):
        max_values = np.sort(array[1:-1])[-count:]
        return [i for i, el in enumerate(array) if el in max_values]







