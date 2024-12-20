import json, sys
from process_network import Graph, find_paths, parse_tntp_net_file, parse_tntp_trips_file
from volume_operations import BPR

GRAPH = sys.argv[1] #Graph file location
LENGTH = int(sys.argv[2]) #Maximum path length of paths found in the network

def save_paths_to_file(graph_name: str, output_filename: str, max_length=LENGTH):
    graph_net_file = str(graph_name) + "_net.tntp"
    graph_trips_file = str(graph_name) + "_trips.tntp"

    graph = Graph()
    edges = parse_tntp_net_file(graph_net_file)
    commodities = parse_tntp_trips_file(graph_trips_file)

    for edge in edges:
        graph.add_edge(edge)
        BPR(edge)

    for commodity in commodities:
        graph.add_commodity(commodity)

    all_paths = {}

    for commodity in graph.commodities:
        init_node = commodity.init_node
        term_node = commodity.term_node

        key = str(init_node) + "," + str(term_node)
        paths = find_paths(init_node, term_node, edges, max_length)
        all_paths[key] = paths

    with open(output_filename, "w") as file:
        json.dump(all_paths, file, indent=4)
    
    print(f"Paths saved to {output_filename}")


def main():
    if GRAPH == "TNTP_Networks/SiouxFalls":
        outputfile_name = "SiouxFallsPaths.json"
    elif GRAPH == "TNTP_Networks/EMA":
        outputfile_name = "EMAPaths.json"
    elif GRAPH == "TNTP_Networks/ChicagoSketch":
        outputfile_name = "ChicagoSketchPaths.json"
    elif GRAPH == "TNTP_Networks/Test":
        outputfile_name = "TestPaths.json"
    elif GRAPH == "TNTP_Networks/Anaheim":
        outputfile_name = "AnaheimPaths.json"
    elif GRAPH == "TNTP_Networks/Barcelona":
        outputfile_name = "BarcelonaPaths.json"
    elif GRAPH == "TNTP_Networks/Braess":
        outputfile_name = "BraessPaths.json"
    elif GRAPH == "TNTP_Networks/Sydney":
        outputfile_name = "SydneyPaths.json"
    elif GRAPH == "TNTP_Networks/Pigou":
        outputfile_name = "PigouPaths.json"
    elif GRAPH == "TNTP_Networks/Austin":
        outputfile_name = "AustinPaths.json"
    #Add more as needed

    save_paths_to_file(GRAPH, outputfile_name)


if __name__ == '__main__':
    main()