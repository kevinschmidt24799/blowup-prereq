import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import multiprocessing as mp
from functools import partial

n = 10
k = 3

def process_graph(g, n, k):
    """Process a single graph and return result if it meets criteria"""
    arr = nx.adjacency_spectrum(g)
    arr.sort()
    v = (arr[n - k].real + 1) / n
    if v >= 1 / (k + 0.01):
        return {
            'graph': g,
            'spectrum': arr,
            'value': v,
            'meets_criteria': True
        }
    return {'meets_criteria': False}

def main():
    count = 0

    if n == 11:
        G = nx.read_sparse6(f"graphs/graph{n}.is6")
    else:
        G = nx.read_graph6(f"graphs/graph{n}.g6")

    print("done reading graph6 file.")

    # Convert generator to list for parallel processing
    graphs = list(G)
    total_graphs = len(graphs)
    print(f"Processing {total_graphs} graphs...")

    # Create partial function with fixed parameters
    process_func = partial(process_graph, n=n, k=k)

    # Use multiprocessing to process graphs in parallel
    with mp.Pool() as pool:
        results = []
        processed = 0

        # Process graphs in batches to show progress
        batch_size = 1000
        for i in range(0, len(graphs), batch_size):
            batch = graphs[i:i+batch_size]
            batch_results = pool.map(process_func, batch)
            results.extend(batch_results)
            processed += len(batch)
            # print(f"Processed {processed}/{total_graphs} graphs")

    # Display results
    for result in results:
        if result['meets_criteria']:
            print(result['spectrum'])
            count += 1
            print(result['graph'])
            print(result['value'])
            nx.draw(result['graph'])
            plt.show()

    print(count)

if __name__ == "__main__":
    main()
