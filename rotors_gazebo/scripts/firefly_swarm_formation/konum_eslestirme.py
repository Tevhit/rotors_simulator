from hungarian_algorithm import algorithm
import networkx as nx
from networkx.algorithms import bipartite
import math

class KonumEslestirme:

    def dist(self, position1, position2):
        sum = 0
        for i in range(len(position1)):
            diff = position1[i] - position2[i]
            sum += diff * diff
        return math.sqrt(sum)

    def getBipartiteMatchingResult(self, current_points, target_points):

        B = nx.Graph()

        top_nodes = []
        for i in range(0, len(current_points)):
            top_nodes.append(current_points[i].iha_id)

        bottom_nodes = []
        for i in range(0, len(target_points)):
            bottom_nodes.append(target_points[i][0])

        for i in range(0, len(current_points)):
            for j in range(0, len(target_points)):
                my_weight = self.dist([current_points[i].pose_x, current_points[i].pose_y],
                                      [target_points[j][1][0], target_points[j][1][1]])
                B.add_edge(current_points[i].iha_id, target_points[j][0][0], weight=my_weight)

        my_matching = bipartite.matching.minimum_weight_full_matching(B, top_nodes, "weight")
        return my_matching

