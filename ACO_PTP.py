from __future__ import annotations
import random


# Configurações do Algoritmo
Q_EDGE_VALUE = 1 # Parâmetro de importância de atualização dos feromônios dos arestas
Q_VERTEX_VALUE = 1 # Parâmetro de importância de atualização dos feromônios dos vértices
ITERATIONS = 100 # Número de iterações do algoritmo
EVAPORATION_RATE = 0.4 # taxa de evaporação dos feromônios
ALPHA = 1  # Peso do feromônio nas arestas
BETA = 1  # Peso do custo
GAMMA = 1 # Peso do feromôonio dos vértices
DELTA = 1 # Peso dos bônus
FORMIGAS = 100 # Número de formigas que irão procurar um caminho numa iteração


class Vertex: #Classe dos vértices
    def __init__(self, vertex_pheromones=1, bonus=1, label=None):
        self.label = label
        self.bonus = bonus
        self.vertex_pheromones = vertex_pheromones
        self.adjacent_edges = []

    def update_pheromone(self, path_bonus): #Função que atualiza os feromônios do vértice, com base nos bônus obtidos pelo caminho
        self.vertex_pheromones = (
            self.vertex_pheromones * (1 - EVAPORATION_RATE)
            + Q_VERTEX_VALUE * path_bonus
        )

    def __repr__(self):
        return f"{self.label}"

    def choose_next_vertex( #Função que, a partir dos possíveis vértices obtidos em next_vertices, calcula suas respectivas probabilidades e escolhe um vértice aleatoriamente.
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
                probabilities.append( # Calcula a probabilidade que cada possível vértice terá
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
        for i in range(len(probabilities)): # Aqui, obtemos um número aleatório e pegamos o vértice condizente
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

    def update_pheromone(self, path_distance): #Função que atualiza os valores dos feromônios das arestas
        self.edge_pheromones = (
            self.edge_pheromones * (1 - EVAPORATION_RATE) + Q_EDGE_VALUE / path_distance
        )

    def __repr__(self):
        return f"{self.adjacent_vertices}"


class Graph:
    def __init__(self, vertices_list: list[Vertex]):
        self.vertices_list = vertices_list


def next_vertices( # Essa função retorna quais os possíveis vértices que a formiga pode escolher ir para
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
            if (vertex != adj_vertex) and vertex_not_visited( # Verifica se o vértice já foi visitado
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


def vertex_not_visited(visited_vertices: list[Vertex], vertex: Vertex): # Verifica se o vértice já foi visitado
    return vertex not in visited_vertices


def make_path(initial_vertex: Vertex): # Nessa função, temos a construção do caminho escolhido pela formiga
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


def ant_colony(graph: Graph): # Função principal que roda o algoritmo
    best_path = None
    best_distance = float("inf")
    best_bonus = 0

    for it in range(ITERATIONS):
        distances = []
        bonuses = []
        iteration_paths = []

        for i in range(len(graph.vertices_list)):  # FORMIGAS // len(graph.vertices_list) //
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


def create_graph_from_matrices(cost_matrix, bonus_matrix): # Função que, a partir de matrizes de custo e bônus, produzem os objetos para o funcionamento do código
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