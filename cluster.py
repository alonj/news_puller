import sys
import metrics

class cluster:
    def __init__(self):
        self.id = 0
        self.points = {}
        self.single_link(self, )

    def single_link(self, other_cluster):
        distances = []
        for p_key in self.points.keys():
            min = sys.maxsize
            for p_key2 in other_cluster.points.keys():
                if min > metrics.distance_cos(self.points[p_key], other_cluster.points[p_key2]):
                    min = metrics.distance_cos(self.points[p_key], other_cluster.points[p_key2])
            distances.append(min)
        distances.sort()
        return distances[0]

