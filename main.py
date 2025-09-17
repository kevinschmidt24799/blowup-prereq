import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

n = 9
count = 0

G = nx.read_graph6(f"graphs/graph{n}.g6")
for g in G:
    arr = nx.adjacency_spectrum(g)
    arr.sort()
    v = (arr[n-3].real+1)/n
    if v >= 1/3.001:
        print(arr)
        count += 1
        print(g)
        print(v)
        nx.draw(g)
        plt.show()
print (count)