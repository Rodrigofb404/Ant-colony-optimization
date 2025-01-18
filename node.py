from edge import Edge

class Node:
  def __init__(self, id: str):
    self.id = id
    self.edges = [] # Lista de arestas que inclue esta aresta
    self.bonus = 0

  def add_edge(self, edge: Edge):
    """Adiciona uma aresta ao vértice, se estiver conectada a ele"""
    if self.id in edge.nodes:
      self.edges.append(edge)

  def get_edge_info(self, neighbor: str):
    """Retorna os detalhes da aresta que conecta o nó atual ao vizinho"""
    for edge in self.edges:
      if neighbor in edge.nodes:
        return {"distance": edge.distance, "nodes": edge.nodes}
    return {}

  def get_neighbors(self):
    """Retorna os vizinhos do nó atual"""
    neighbors = []
    for edge in self.edges:
      neighbor = edge.get_other_node(self.id)
      if neighbor:
        neighbors.append(neighbor)
    return neighbors

  def get_edge_list(self):
    """Retorna as arestas conectadas a este vértice"""
    return [{"neighbor": edge.get_other_node(self.id), "distance": edge.distance} for edge in self.edges]


if __name__ == "__main__":
  node0 = Node('0')
  node1 = Node('1')
  node2 = Node('2')
  
  edge0_1 = Edge(10.0, '0', '1')
  edge0_2 = Edge(5.0, '0', '2')
  
  node0.add_edge(edge0_1)
  node0.add_edge(edge0_2)
  node1.add_edge(edge0_1)
  node2.add_edge(edge0_2)
  
  print("Vizinhos de node0:", node0.get_neighbors())
  print("Detalhes da aresta edge0_1:", node0.get_edge_info('1'))
  print("Lista de arestas de node0:", node0.get_edge_list())