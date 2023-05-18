import networkx as nx
import matplotlib.pyplot as plt

# TODO:
# add visualization for undirected AND directed graphs
# add weighted graphs
# make the dots be draggable

class Graph:
    def __init__(self, vertices: list, edges: list[tuple] | list[set]):
        self.vertices = vertices
        self.edges = edges
        self.directed = all(isinstance(edge, set) for edge in edges)
        
    def is_directed(self):
        pass
        
    def visualize(self):
        G = nx.DiGraph()  # Use DiGraph for directed edges

        G.add_nodes_from(self.vertices)
        G.add_edges_from(self.edges)

        pos = nx.spring_layout(G)  # Layout algorithm for node positioning

        nx.draw_networkx_nodes(G, pos)
        
        # Draw edges with curved arrows for bidirectional edges
        for edge in self.edges:
            if (edge[1], edge[0]) in self.edges:
                nx.draw_networkx_edges(G, pos, edgelist=[edge], arrowstyle='->', connectionstyle='arc3,rad=0.2')
            else:
                nx.draw_networkx_edges(G, pos, edgelist=[edge], arrowstyle='->')
        
        nx.draw_networkx_labels(G, pos)  # Add labels to the nodes
        
        plt.show()

graph = Graph([1, 2, 3, 5], [(1, 2), (2, 3), (3, 1), (1, 3)])
print(graph.directed)
graph.visualize()

graph2 = Graph([1, 2, 3, 5], [{1, 2}, {2, 3}])
print(graph2.directed)

