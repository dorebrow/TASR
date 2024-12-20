import random
import json
from collections import defaultdict, deque

'''Edge class; Creates Edge objects from the attributes of road links in standard .tntp files.'''
class Edge:
    def __init__(self, 
                 init_node: str,
                 term_node: str,
                 capacity: float,
                 volume: float,
                 length: float,
                 fft: float,
                 b: float,
                 power: float,
                 speed_limit: float,
                 toll: float,
                 link_type: float,
                 travel_time: float):
        self.init_node = str(init_node)
        self.term_node = str(term_node)
        self.capacity = capacity
        self.volume = volume
        self.length = length
        self.fft = fft
        self.b = b
        self.power = power
        self.speed_limit = speed_limit
        self.toll = toll
        self.link_type = link_type
        self.travel_time = travel_time
        self.selfish_flow = 0
        self.tasr_flow = 0
        self.assigned_flow = 0

    def __repr__(self):
        return f"({self.init_node},{self.term_node})"


'''Path class; Creates Path objects with relevant attributes.'''
class Path:
    def __init__(self, 
                 links: list,
                 system_optimal_flow: float,
                 assigned_flow: float,
                 true_flow: float,
                 true_latency: float,
                 system_optimal_latency: float):
        self.links = links
        self.system_optimal_flow = 0.0
        self.assigned_flow = 0.0
        self.selfish_flow = 0.0
        self.true_flow = 0.0
        self.true_latency = 0.0
        self.system_optimal_latency = 0.0
        self.capacity = 0.0

    def __repr__(self):
        return f"{self.links}"


'''Commodity class; Creates Commodity objects with relevant attributes.'''
class Commodity:
    def __init__(self, name: tuple, init_node: str, term_node: str, paths=None, demand=0.0):
        self.name = name  #(init_node, term_node)
        self.init_node = init_node
        self.term_node = term_node
        self.paths = paths if paths is not None else []
        self.demand = demand

'''Graph class; Creates Graph object (usually only one) with relevant attributes.'''
class Graph:
    def __init__(self):
        self.edges = []
        self.commodities = []
        self.so_travel_time = 0.0 
        self.tasr_travel_time = 0.0
        self.br_travel_time = 0.0
        self.total_selfish_flow = 0
        self.total_so_flow = 0

    def add_edge(self, edge):
        self.edges.append(edge)

    def add_commodity(self, commodity):
        self.commodities.append(commodity)

    def __repr__(self):
        return f"Graph(edges={len(self.edges)}, commodities={len(self.commodities)}, travel_time={self.travel_time})"


'''This function parses a .tntp net file to create Edge objects for each edge in the file.'''
def parse_tntp_net_file(filename):
    edges = []
    with open(filename, 'r') as file:
        header = next(file).strip().split('\t')
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) < 10:
                continue  
            
            try:
                edge = Edge(
                    init_node=parts[0].strip(),
                    term_node=parts[1].strip(),
                    capacity=float(parts[2].strip()),
                    length=float(parts[3].strip()),
                    volume=random.uniform(0, 2000),
                    fft=float(parts[4].strip()),
                    b=float(parts[5].strip()),
                    power=float(parts[6].strip()),
                    speed_limit=float(parts[7].strip()),
                    toll=float(parts[8].strip()),
                    link_type=float(parts[9].strip()),
                    travel_time=0.0
                )
                edges.append(edge)
            except ValueError as e:
                continue
    return edges


'''This function parses a .tntp trips file to create a list of Commodity objects.'''
def parse_tntp_trips_file(filename):
    commodities = []
    with open(filename, 'r') as file:
        lines = file.readlines()

        index = 0
        while lines[index].strip() != "<END OF METADATA>":
            index += 1
        index += 1

        while index < len(lines):
            line = lines[index].strip()
            if line.startswith("Origin"):
                origin = int(line.split()[1])
                index += 1 
                
                while index < len(lines) and lines[index].strip():
                    demand_line = lines[index].strip()
                    demands = demand_line.split(';')
                    for demand in demands:
                        dest_demand = demand.split(':')
                        
                        if len(dest_demand) != 2:
                            continue
                        
                        try:
                            destination = int(dest_demand[0].strip())
                            demand_value = float(dest_demand[1].strip().replace(';', ''))

                            if origin == destination:
                                continue

                            commodity = Commodity(
                                name=(origin, destination),
                                init_node=origin,
                                term_node=destination,
                                demand=demand_value
                            )
                            commodities.append(commodity)
                        except ValueError as e:
                            continue
                    index += 1
            index += 1

    return commodities


'''This function gets paths for each commodity using a BFS with memoization that avoids cycles. Can choose 
max length of paths, but 5 by default.'''
def find_paths(start_node, destination_node, edges, max_length=5):
    start_node = str(start_node)
    destination_node = str(destination_node)
    
    graph = defaultdict(list)
    for edge in edges:
        graph[edge.init_node].append(edge.term_node)

    memo = {}

    def bfs_paths(current_node, destination_node, path):
        if (current_node, destination_node) in memo:
            return memo[(current_node, destination_node)]

        paths = []
        queue = deque([(current_node, path)])

        while queue:
            node, current_path = queue.popleft()

            if node == destination_node and len(current_path) > 1:
                paths.append(current_path)

            if len(current_path) < max_length + 1:
                for neighbor in graph[node]:
                    if neighbor not in current_path:
                        queue.append((neighbor, current_path + [neighbor]))

        memo[(current_node, destination_node)] = paths
        return paths

    all_paths = bfs_paths(start_node, destination_node, [start_node])
    
    valid_paths = [path for path in all_paths if path[0] == start_node and path[-1] == destination_node]

    return valid_paths


'''This function loads a dictionary of all network paths from a .json file, given the network provided as an argument when running main.py.
To execute properly, graph_name must be a valid string matching one of the networks that has already
been preprocessed.'''
def load_paths_from_file(graph_name: str):
    if graph_name == "TNTP_Networks/SiouxFalls":
        outputfile_name = "Processed_Networks/SiouxFallsPaths.json"
    elif graph_name == "TNTP_Networks/EMA":
        outputfile_name = "Processed_Networks/EMAPaths.json"
    elif graph_name == "TNTP_Networks/ChicagoSketch":
        outputfile_name = "Processed_Networks/ChicagoSketchPaths.json"
    elif graph_name == "TNTP_Networks/Test":
        outputfile_name = "Processed_Networks/TestPaths.json"
    elif graph_name == "TNTP_Networks/Anaheim":
        outputfile_name = "Processed_Networks/AnaheimPaths.json"
    elif graph_name == "TNTP_Networks/Barcelona":
        outputfile_name = "Processed_Networks/BarcelonaPaths.json"
    elif graph_name == "TNTP_Networks/Braess":
        outputfile_name = "Processed_Networks/BraessPaths.json"
    elif graph_name == "TNTP_Networks/Winnipeg":
        outputfile_name = "Processed_Networks/WinnipegPaths.json"
    elif graph_name == "TNTP_Networks/Sydney":
        outputfile_name = "Processed_Networks/SydneyPaths.json"
    elif graph_name == "TNTP_Networks/Pigou":
        outputfile_name = "Processed_Networks/PigouPaths.json"
    elif graph_name == "TNTP_Networks/Austin":
        outputfile_name = "Processed_Networks/AustinPaths.json"
    else:
        raise ValueError(f"Graph {graph_name} not recognized.")

    # Load paths from the JSON file
    with open(outputfile_name, "r") as file:
        return json.load(file)



def assign_paths_to_single_commodity(graph: Graph, paths_data: dict):
    for commodity in graph.commodities:
            init_node = commodity.init_node
            term_node = commodity.term_node

            # Convert init_node, term_node to match JSON key format
            key = f"{init_node},{term_node}"
            found_paths = paths_data.get(key, [])

            commodity.paths = []
            for path in found_paths:
                path_links = []
                for i in range(len(path) - 1):
                    edge = next((edge for edge in graph.edges if edge.init_node == path[i] and edge.term_node == path[i + 1]), None)
                    if edge:
                        path_links.append(edge)

                path_object = Path(
                    links=path_links,
                    system_optimal_flow=0.0,
                    assigned_flow=0.0,
                    true_flow=0.0,
                    true_latency=0.0,
                    system_optimal_latency=0.0
                )
                commodity.paths.append(path_object)


def assign_paths_to_commodities(graph: Graph, constrained_graph: Graph, paths_data: dict):
    for commodity in graph.commodities:
        init_node = commodity.init_node
        term_node = commodity.term_node

        # Convert init_node, term_node to match JSON key format
        key = f"{init_node},{term_node}"
        found_paths = paths_data.get(key, [])

        commodity.paths = []
        for path in found_paths:
            path_links = []
            for i in range(len(path) - 1):
                edge = next((edge for edge in graph.edges if edge.init_node == path[i] and edge.term_node == path[i + 1]), None)
                if edge:
                    path_links.append(edge)

            path_object = Path(
                links=path_links,
                system_optimal_flow=0.0,
                assigned_flow=0.0,
                true_flow=0.0,
                true_latency=0.0,
                system_optimal_latency=0.0
            )
            commodity.paths.append(path_object)

            for edge in path_links:
                if edge not in constrained_graph.edges:
                    constrained_graph.add_edge(edge)
 
        constrained_graph.add_commodity(commodity)