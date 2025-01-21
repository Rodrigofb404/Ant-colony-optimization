from __future__ import annotations
import random
import networkx as nx
import matplotlib.pyplot as plt


# Configurações do Algoritmo
Q_EDGE_VALUE = 1
Q_VERTEX_VALUE = 1
ITERATIONS = 100
EVAPORATION_RATE = 0.4
ALPHA = 1  # Peso do feromônio nas arestas
BETA = 1  # Peso do feromônio nos vértices
GAMMA = 1
DELTA = 1
FORMIGAS = 200


class Vertex:
    def __init__(self, vertex_pheromones=1, bonus=1, label=None):
        self.label = label
        self.bonus = bonus
        self.vertex_pheromones = vertex_pheromones
        self.adjacent_edges = []

    def update_pheromone(self, path_bonus):
        self.vertex_pheromones = (
            self.vertex_pheromones * (1 - EVAPORATION_RATE)
            + Q_VERTEX_VALUE * path_bonus
        )

    def __repr__(self):
        return f"{self.label}"

    def choose_next_vertex(
        self, initial_vertex: Vertex, visited_vertices: list[Vertex]
    ) -> tuple[bool, Vertex, Edge]:
        total, possible_vertices, possible_edges = next_vertices(
            self, self.adjacent_edges, visited_vertices, initial_vertex
        )
        probabilities = []
        if total == 0:
            probabilities.append(1)
        else:
            for i in range(len(possible_edges)):
                probabilities.append(
                    (
                        (
                            (
                                possible_edges[i].edge_pheromones ** ALPHA
                                * possible_vertices[i].vertex_pheromones ** GAMMA
                                * possible_vertices[i].bonus ** DELTA
                            )
                            / possible_edges[i].cost ** BETA
                        )
                    )
                    / total
                )

        probabilities = [p / sum(probabilities) for p in probabilities]

        random_number = random.random()
        choosing = 0
        for i in range(len(probabilities)):
            choosing += probabilities[i]
            if choosing >= random_number:
                vert = possible_vertices[i]
                if vert == initial_vertex:
                    return True, vert, possible_edges[i]
                else:
                    return False, vert, possible_edges[i]


class Edge:
    def __init__(
        self, edge_pheromones=1, cost=1, adjacent_vertices: list[Vertex] = None
    ):
        self.edge_pheromones = edge_pheromones
        self.cost = cost
        self.adjacent_vertices = adjacent_vertices

    def update_pheromone(self, path_distance):
        self.edge_pheromones = (
            self.edge_pheromones * (1 - EVAPORATION_RATE) + Q_EDGE_VALUE / path_distance
        )

    def __repr__(self):
        return f"{self.adjacent_vertices}"


class Graph:
    def __init__(self, vertices_list: list[Vertex]):
        self.vertices_list = vertices_list


def next_vertices(
    vertex: Vertex,
    adjacent_edges: list[Edge],
    visited_vertices: list[Vertex],
    initial_vertex,
):
    possible_vertices = []
    possible_edges = []
    total = 0
    for adjacent_edge in adjacent_edges:
        for adj_vertex in adjacent_edge.adjacent_vertices:
            if vertex == initial_vertex:
                possible_vertices.append(adj_vertex)
                possible_edges.append(adjacent_edge)
            if (vertex != adj_vertex) and vertex_not_visited(
                visited_vertices, adj_vertex
            ):
                possible_vertices.append(adj_vertex)
                possible_edges.append(adjacent_edge)
                total += (
                    adjacent_edge.edge_pheromones**ALPHA
                    * adj_vertex.vertex_pheromones**GAMMA
                    * adj_vertex.bonus**DELTA
                ) / adjacent_edge.cost**BETA
    if (
        total == 0
    ):  # This is important for the case where all the remaining edges are impossible (or incredibly inefficient). It will choose any of the remaining
        edg = random.choice(adjacent_edges)
        possible_edges.append(edg)
        for vert in edg.adjacent_vertices:
            if vert != vertex:
                possible_vertices.append(vert)
    return total, possible_vertices, possible_edges


def vertex_not_visited(visited_vertices: list[Vertex], vertex: Vertex):
    return vertex not in visited_vertices


def make_path(initial_vertex: Vertex):
    distance = 0
    bonus = 0
    visited_vertices = []
    stop, chosen_vertex, chosen_edge = initial_vertex.choose_next_vertex(
        initial_vertex=initial_vertex, visited_vertices=visited_vertices
    )
    path = [initial_vertex]
    if chosen_edge:
        path.append(chosen_edge)
        path.append(chosen_vertex)
        distance += chosen_edge.cost
        bonus += chosen_vertex.bonus
        visited_vertices.append(chosen_vertex)

    while not stop:
        stop, chosen_vertex, chosen_edge = chosen_vertex.choose_next_vertex(
            initial_vertex=initial_vertex, visited_vertices=visited_vertices
        )
        if chosen_edge:
            path.append(chosen_edge)
            path.append(chosen_vertex)
            distance += chosen_edge.cost
            bonus += chosen_vertex.bonus
            visited_vertices.append(chosen_vertex)
    if len(path) == 3:
        path.pop(1)
        path.pop(1)
        distance = 0
    return path, distance, bonus


def ant_colony(graph: Graph):
    best_path = None
    best_distance = float("inf")
    best_bonus = 0

    for _ in range(ITERATIONS):
        distances = []
        bonuses = []
        iteration_paths = []

        for i in range(FORMIGAS):  # FORMIGAS // len(graph.vertices_list) //
            path, distance, bonus = make_path(graph.vertices_list[0])
            iteration_paths.append(path)
            distances.append(distance)
            bonuses.append(bonus)

            if bonus - distance > best_bonus - best_distance:
                best_path = path
                best_distance = distance
                best_bonus = bonus

        for path, distance, bonus in zip(iteration_paths, distances, bonuses):
            for element in path:
                if isinstance(element, Edge):
                    element.update_pheromone(distance)
                elif isinstance(element, Vertex):
                    element.update_pheromone(bonus)

    return best_path, best_distance, best_bonus


def create_graph_from_matrices(cost_matrix, bonus_matrix):
    num_vertices = len(bonus_matrix)
    vertices = []
    for i in range(num_vertices):
        bonus = bonus_matrix[i]
        vertices.append(Vertex(label=(i + 1), vertex_pheromones=1, bonus=bonus))

    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if cost_matrix[i][j] != 0:
                cost = cost_matrix[i][j]
                edge = Edge(
                    edge_pheromones=1,
                    cost=cost,
                    adjacent_vertices=[vertices[i], vertices[j]],
                )
                vertices[i].adjacent_edges.append(edge)
                vertices[j].adjacent_edges.append(edge)

    return Graph(vertices_list=vertices)


def main():
    cost_matrix = [
        [0, 3, 10, 4, 12, 8, 5, 7, 15, 3],
        [3, 0, 3, 12, 15, 4, 12, 7, 6, 8],
        [10, 3, 0, 11, 12, 14, 20, 15, 5, 17],
        [4, 12, 11, 0, 10, 13, 9, 5, 13, 9],
        [12, 15, 12, 10, 0, 1, 5, 12, 10, 15],
        [8, 4, 14, 13, 1, 0, 17, 8, 9, 14],
        [5, 12, 20, 9, 5, 17, 0, 16, 3, 11],
        [7, 7, 15, 5, 12, 8, 16, 0, 10, 10],
        [15, 6, 5, 13, 10, 9, 3, 10, 0, 15],
        [3, 8, 17, 9, 15, 14, 11, 10, 15, 0],
    ]

    cost_matrix2 = [
        [
            0,
            9.1,
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            15.4,
            9.7,
            float("inf"),
            float("inf"),
        ],
        [
            9.1,
            0,
            6.8,
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
        ],
        [
            float("inf"),
            6.8,
            0,
            6.1,
            8.2,
            float("inf"),
            27,
            18.7,
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
        ],
        [
            float("inf"),
            float("inf"),
            6.1,
            0,
            3.7,
            9.5,
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
        ],
        [
            float("inf"),
            float("inf"),
            8.2,
            3.7,
            0,
            10.4,
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
        ],
        [
            float("inf"),
            float("inf"),
            float("inf"),
            9.5,
            10.4,
            0,
            28.2,
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
        ],
        [
            float("inf"),
            float("inf"),
            27,
            float("inf"),
            float("inf"),
            28.1,
            0,
            14.5,
            float("inf"),
            float("inf"),
            float("inf"),
            14.4,
        ],
        [
            float("inf"),
            float("inf"),
            18.7,
            float("inf"),
            float("inf"),
            float("inf"),
            14.5,
            0,
            6.4,
            float("inf"),
            8.4,
            7.3,
        ],
        [
            15.4,
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            6.4,
            0,
            7,
            10.8,
            float("inf"),
        ],
        [
            9.7,
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            7,
            0,
            float("inf"),
            8.1,
        ],
        [
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            8.4,
            10.8,
            float("inf"),
            0,
            6.3,
        ],
        [
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            float("inf"),
            14.4,
            7.3,
            float("inf"),
            8.1,
            6.3,
            0,
        ],
    ]
    bonus_matrix = [11, 46, 45, 67, 86, 37, 31, 53, 89, 40]
    bonus_matrix2 = [0, 29, 5, 22, 150, 51, 27, 19, 119, 35, 138, 147]
    graph = create_graph_from_matrices(cost_matrix2, bonus_matrix2)
    final_path, final_distance, final_bonus = ant_colony(graph)

    print(
        "Final path:",
        final_path,
        "\nFinal distance:",
        final_distance,
        "\nFinal bonus:",
        final_bonus,
        "\nFinal profit:",
        final_bonus - final_distance,
    )


if __name__ == "__main__":
    main()
