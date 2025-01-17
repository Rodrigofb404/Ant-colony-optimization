class Node:
  def __init__(self, id: str):
    self.id = id
    self.edges = {}
    
    self.bonus = 0
    
  def add_edge(self, neighbor: str, distance: float):
    self.edges[neighbor] = {"distance": distance}
    
  def get_edge(self, neighbor: str):
    return self.edges.get(neighbor, {})
  
  def get_neighbors(self):
    return list(self.edges.keys())
  
  def get_edge_list(self):
    return self.edges
  

if __name__ == "__main__":
  node0 = Node('0')
  node0.add_edge('1', 10.0)
  node0.add_edge('2', 5.0)
  print(node0.get_neighbors())
  print(node0.get_edge('1'))
  print(node0.get_edge('2'))
  print(node0.get_edge_list())