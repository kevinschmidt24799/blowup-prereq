import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp


G = nx.complete_graph(5)
H = nx.path_graph(2)

P = nx.tensor_product(G,H)
nx.draw(P)
plt.show()
