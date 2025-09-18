import networkx as nx

def read_sparse6_stream(filename):
    """
    Stream sparse6 graphs one at a time from a file.
    Yields NetworkX graphs without loading the entire file into memory.
    """
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line and line.startswith(':'):
                try:
                    # Parse single sparse6 string using NetworkX
                    graph = nx.from_sparse6_bytes(line.encode('ascii'))
                    yield graph
                except Exception as e:
                    print(f"Warning: Could not parse line '{line[:20]}...': {e}")
                    continue

def count_graphs_in_file(filename):
    """Count total number of graphs in sparse6 file without loading them all."""
    count = 0
    with open(filename, 'r') as f:
        for line in f:
            if line.strip() and line.strip().startswith(':'):
                count += 1
    return count