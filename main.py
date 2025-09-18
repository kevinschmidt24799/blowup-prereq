import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import multiprocessing as mp
from functools import partial
from sparse6_stream import read_sparse6_stream, count_graphs_in_file

n = 11
k = 3

def process_graph(g, n, k, max_value, max_graph, max_seen, lock):
    """Process a single graph and return result if it meets criteria"""
    arr = nx.adjacency_spectrum(g)
    arr.sort()
    v = (arr[n - k].real + 1) / n

    # Update global max with thread safety
    with lock:
        if v > max_value.value:
            max_value.value = v
            max_seen.value = False
            max_graph.value = g

    if v >= 1 / (k + 0.01):
        return {
            'graph': g,
            'spectrum': arr,
            'value': v,
            'meets_criteria': True
        }
    return {'meets_criteria': False,
            'value': v }

def main():
    count = 0

    # Create shared variables for multiprocessing
    with mp.Manager() as manager:
        max_value = manager.Value('d', 0.0)  # shared double
        max_graph = manager.Value('O', None)  # shared object
        max_seen = manager.Value('d', False)
        lock = manager.Lock()

        if n == 11:
            filename = f"graphs/graph{n}.s6"
            print(f"Counting graphs in {filename}...")
            # total_graphs = count_graphs_in_file(filename)
            total_graphs = 1
            # print(f"Found {total_graphs} graphs. Starting streaming processing...")

            # Use streaming parser instead of loading all at once
            G = read_sparse6_stream(filename)
        else:
            print(f"graphs/graph{n}.g6")
            G = nx.read_graph6(f"graphs/graph{n}.g6")
            # For g6 files, still need to count
            graphs = list(G)
            total_graphs = len(graphs)
            G = iter(graphs)  # Convert back to iterator

        print(f"Processing {total_graphs} graphs...")

        # Create partial function with fixed parameters
        process_func = partial(process_graph, n=n, k=k, max_value=max_value, max_graph=max_graph, max_seen=max_seen, lock=lock)

        # Process graphs in streaming batches to avoid memory issues
        with mp.Pool() as pool:
            results = []
            processed = 0
            batch_size = 100000  # Smaller batch size for streaming

            batch = []
            for graph in G:
                batch.append(graph)

                if len(batch) >= batch_size:
                    # Process current batch
                    batch_results = pool.map(process_func, batch)
                    results.extend([r for r in batch_results if r['meets_criteria']])
                    processed += len(batch)
                    print(f"Processed {processed}/{total_graphs} graphs, max value so far: {max_value.value:.6f}")
                    if not max_seen.value:
                        nx.draw(max_graph.value)
                        plt.show()
                        max_seen.value = True
                        # print(nx.adjacency_matrix(max_graph.value).todense())

                    batch = []  # Clear batch to free memory

            # Process remaining graphs in the last batch
            if batch:
                batch_results = pool.map(process_func, batch)
                results.extend([r for r in batch_results if r['meets_criteria']])
                processed += len(batch)
                print(f"Processed {processed}/{total_graphs} graphs, max value so far: {max_value.value:.6f}")

        # Display results
        for result in results:
            if result['meets_criteria']:
                print(result['spectrum'])
                count += 1
                print(result['graph'])
                print(result['value'])
                nx.draw(result['graph'])
                plt.show()

        print(f"Found {count} graphs meeting criteria")
        print(f"Maximum value found: {max_value.value:.6f}")
        if max_graph.value:
            print(f"Maximum graph has {max_graph.value.number_of_nodes()} nodes and {max_graph.value.number_of_edges()} edges")
            print(nx.adjacency_matrix(max_graph.value).todense())

if __name__ == "__main__":
    main()
