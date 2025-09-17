import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

n = 10
count = 0

if n == 11:
    G = nx.read_sparse6(f"graphs/graph{n}.is6")
else:
    G = nx.read_graph6(f"graphs/graph{n}.g6")

print("done reading graph6 file.")
progress = 0
for g in G:
    arr = nx.adjacency_spectrum(g)
    arr.sort()
    v = (arr[n-3].real+1)/n
    if v >= 1/3.1:
        print(arr)
        count += 1
        print(g)
        print(v)
        nx.draw(g)
        plt.show()
    progress+=1
    if progress % 1000 == 0:
        print(progress)
print (count)