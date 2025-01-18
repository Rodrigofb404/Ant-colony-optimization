class Edge:
  def __init__(self, distance: float, node_1: str, node_2: str):
    self.distance = distance
    self.nodes = (node_1, node_2)
  
  def get_other_node(self, current_node: str):
    """Retorna o nó oposto ao nó atual nesta aresta"""
    if current_node == self.nodes[0]:
      return self.nodes[1]
    elif current_node == self.nodes[1]:
      return self.nodes[0]
    return None