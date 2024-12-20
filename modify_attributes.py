"""
File: modify_attributes.py
Purpose: Stores Demand_Group class definition along with any functions
         that are used to modify any class member variables.
"""

from process_network import Graph, Commodity
from volume_operations import parameterized_BPR
import random
import math

TRUSTS = [0.25, 0.5, 0.75] #Can modify these values, but must be between 0 and 1 inclusive
TRUST_PROBABILITIES = [1/3, 1/3, 1/3]  #Can modify these values, but probabilities must sum to 1

LOW_DEMAND_FRACTION = 0.25
MED_DEMAND_FRACTION = 0.75
HIGH_DEMAND_FRACTION = 1.50

class Demand_Group:
    """
    Description: Demand_Group class with member variables for
    the Commodity object that a demand group corresponds to, the list of paths
    (Path objects) of that commodity (Commodity object), the amount of demand 
    seeking a path for the given commodity, the list of edges (Edge objects) 
    of the given commodity, the expected volumes of traffic on each edge in 
    the given commodity, the trust of the demand group (\alpha), the amount 
    of demand that has been assigned to each path in the commodity, and the 
    latencies of each path in the given commodity with respect to the demand group's
    expected_volumes.
    """
    def __init__(self, commodity: Commodity, paths: list, expected_volumes: dict, demand: int):
        self.commodity = commodity
        self.paths = commodity.paths if commodity.paths is not None else []
        self.demand = demand
        self.unscaled_demand = 0
        self.edge_list = []
        
        for path in commodity.paths:
            for edge in path.links:
                self.edge_list.append(edge)

        self.expected_volumes = expected_volumes
        self.trust = random.choices(TRUSTS, weights=TRUST_PROBABILITIES, k=1)[0]
        self.assigned_path_volumes = [0] * len(self.paths)
        self.selfish_latencies = {}
        self.demand_serviced = 0
        self.selfish_path_choice = None


def strip_network(graph: Graph, constrained_graph: Graph):
    """
    This function takes a graph object and makes a new graph object with the same commodities, 
    excluding those commodities with no paths (invalid).
    """

    commodities_with_paths = [commodity for commodity in graph.commodities if len(commodity.paths) > 0]
    num_commodities_with_paths = len(commodities_with_paths)
  
    if num_commodities_with_paths == 0:
        raise ValueError("No commodities with valid paths to allocate demand.")
    
    for comm in graph.commodities:
        if comm.demand > 0:
           constrained_graph.add_commodity(comm)

    constrained_graph.edges = graph.edges
    constrained_graph.so_travel_time = graph.so_travel_time
    constrained_graph.tasr_travel_time = graph.tasr_travel_time
    constrained_graph.br_travel_time = graph.br_travel_time
    constrained_graph.total_selfish_flow = graph.total_selfish_flow
    constrained_graph.total_so_flow = graph.total_so_flow


def modify_demands(graph: Graph, commodities: list, TOTAL_DEMAND: str):
    """
    This function sets the demand of each commodity object to a scaled version of the 
    largest bottleneck capacity from all commodity paths. TOTAL_DEMAND of LOW scales the
    largest bottleneck capacity by 25%, MED scales the largest bottleneck capacity by 50%,
    and HIGH scales the largest bottleneck capcity by 150%. For use with the TASR, LLF, 
    and ALOOF algorithms.
    """
    
    commodities_with_paths = [commodity for commodity in graph.commodities if len(commodity.paths) > 0]
    num_commodities_with_paths = len(commodities_with_paths)
    
    if num_commodities_with_paths == 0:
        raise ValueError("No commodities with valid paths to allocate demand.")
    
    largest_bottleneck_edge = None

    for commodity in graph.commodities:
        commodity.demand = 0
        largest_bottleneck_edge = None
        if commodity in commodities_with_paths:
            for path in commodity.paths:
                #Find the bottleneck edge for this path
                bottleneck_edge = min(path.links, key=lambda edge: edge.capacity)
                
                #Compare with the largest bottleneck edge found
                if largest_bottleneck_edge is None or bottleneck_edge.capacity > largest_bottleneck_edge.capacity:
                    largest_bottleneck_edge = bottleneck_edge

            if TOTAL_DEMAND == "LOW" or TOTAL_DEMAND == "Low" or TOTAL_DEMAND == "low":
                commodity.demand = LOW_DEMAND_FRACTION * largest_bottleneck_edge.capacity
            elif TOTAL_DEMAND == "MED" or TOTAL_DEMAND == "Med" or TOTAL_DEMAND == "med":
                commodity.demand = MED_DEMAND_FRACTION * largest_bottleneck_edge.capacity
            elif TOTAL_DEMAND == "HIGH" or TOTAL_DEMAND == "High" or TOTAL_DEMAND == "high":
                commodity.demand = HIGH_DEMAND_FRACTION * largest_bottleneck_edge.capacity
            else:
                print("Invalid demand amount entered. Please use LOW, MED, or HIGH.")
    

def modify_demands_ascaled(graph: Graph, commodities: list, TOTAL_DEMAND: str):
    """
    This function sets the demand of each commodity object to a scaled version of the 
    largest bottleneck capacity from all commodity paths. TOTAL_DEMAND of LOW scales the
    largest bottleneck capacity by 25%, MED scales the largest bottleneck capacity by 50%,
    and HIGH scales the largest bottleneck capcity by 150%. For use with the ASCALE algorithm.
    """

    #problem in here: not setting demands correctly and making most demands 0

    network_demands = []

    for commodity in graph.commodities:
        demand = Demand_Group(
                    commodity=commodity,
                    paths=commodity.paths,
                    expected_volumes={},
                    demand = commodity.demand
                )
            
        network_demands.append(demand)

    commodities_with_paths = [commodity for commodity in graph.commodities if len(commodity.paths) > 0]
    num_commodities_with_paths = len(commodities_with_paths)
    
    if num_commodities_with_paths == 0:
        raise ValueError("No commodities with valid paths to allocate demand.")
    
    for commodity in graph.commodities:
        largest_bottleneck_edge = None

        for dem in network_demands:
            if dem.commodity == commodity:
                fraction_of_compliant = dem.trust
                beta = 1 + math.sqrt(1 - fraction_of_compliant)

        if commodity in commodities_with_paths:
            for path in commodity.paths:
                #Find the bottleneck edge for this path
                bottleneck_edge = min(path.links, key=lambda edge: edge.capacity)
                
                #Compare with the largest bottleneck edge found
                if largest_bottleneck_edge is None or bottleneck_edge.capacity > largest_bottleneck_edge.capacity:
                    largest_bottleneck_edge = bottleneck_edge
            
            if TOTAL_DEMAND == "LOW" or TOTAL_DEMAND == "Low" or TOTAL_DEMAND == "low":
                commodity.unscaled_demand = LOW_DEMAND_FRACTION * largest_bottleneck_edge.capacity
                commodity.demand = LOW_DEMAND_FRACTION * largest_bottleneck_edge.capacity * beta
            elif TOTAL_DEMAND == "MED" or TOTAL_DEMAND == "Med" or TOTAL_DEMAND == "med":
                commodity.unscaled_demand = MED_DEMAND_FRACTION * largest_bottleneck_edge.capacity
                commodity.demand = MED_DEMAND_FRACTION * largest_bottleneck_edge.capacity * beta
            elif TOTAL_DEMAND == "HIGH" or TOTAL_DEMAND == "High" or TOTAL_DEMAND == "high":
                commodity.unscaled_demand = HIGH_DEMAND_FRACTION * largest_bottleneck_edge.capacity
                commodity.demand = HIGH_DEMAND_FRACTION * largest_bottleneck_edge.capacity * beta
            else:
                print("Invalid demand amount entered. Please use LOW, MED, or HIGH.")

    for dem in network_demands:
        matching_commodity = next((c for c in graph.commodities if c == dem.commodity), None)
        if matching_commodity:
            dem.unscaled_demand = matching_commodity.unscaled_demand
            dem.demand = matching_commodity.demand

    return network_demands 


def modify_demands_scaled(graph: Graph, commodities: list, TOTAL_DEMAND: str):
    """
    This function sets the demand of each commodity object to a scaled version of the 
    largest bottleneck capacity from all commodity paths. TOTAL_DEMAND of LOW scales the
    largest bottleneck capacity by 25%, MED scales the largest bottleneck capacity by 50%,
    and HIGH scales the largest bottleneck capcity by 150%. For use with the SCALE algorithm.
    """

    network_demands = []

    for commodity in graph.commodities:
        commodity.demand = 0

    for commodity in graph.commodities:
        demand = Demand_Group(
                    commodity=commodity,
                    paths=commodity.paths,
                    expected_volumes={},
                    demand = commodity.demand,
                )
            
        network_demands.append(demand)

    commodities_with_paths = [commodity for commodity in graph.commodities if len(commodity.paths) > 0]
    num_commodities_with_paths = len(commodities_with_paths)
    
    if num_commodities_with_paths == 0:
        raise ValueError("No commodities with valid paths to allocate demand.")
    
    largest_bottleneck_edge = None

    for commodity in graph.commodities:
        largest_bottleneck_edge = None

        for dem in network_demands:
            if dem.commodity == commodity:
                fraction_of_compliant = dem.trust

        if commodity in commodities_with_paths:
            for path in commodity.paths:
                #Find the bottleneck edge for this path
                bottleneck_edge = min(path.links, key=lambda edge: edge.capacity)
                
                #Compare with the largest bottleneck edge found
                if largest_bottleneck_edge is None or bottleneck_edge.capacity > largest_bottleneck_edge.capacity:
                    largest_bottleneck_edge = bottleneck_edge

            if TOTAL_DEMAND == "LOW" or TOTAL_DEMAND == "Low" or TOTAL_DEMAND == "low":
                commodity.unscaled_demand = LOW_DEMAND_FRACTION * largest_bottleneck_edge.capacity
                commodity.demand = LOW_DEMAND_FRACTION * largest_bottleneck_edge.capacity * fraction_of_compliant
            elif TOTAL_DEMAND == "MED" or TOTAL_DEMAND == "Med" or TOTAL_DEMAND == "med":
                commodity.unscaled_demand = MED_DEMAND_FRACTION * largest_bottleneck_edge.capacity
                commodity.demand = MED_DEMAND_FRACTION * largest_bottleneck_edge.capacity * fraction_of_compliant
            elif TOTAL_DEMAND == "HIGH" or TOTAL_DEMAND == "High" or TOTAL_DEMAND == "high":
                commodity.unscaled_demand = HIGH_DEMAND_FRACTION * largest_bottleneck_edge.capacity
                commodity.demand = HIGH_DEMAND_FRACTION * largest_bottleneck_edge.capacity * fraction_of_compliant
            else:
                print("Invalid demand amount entered. Please use LOW, MED, or HIGH.")

    for dem in network_demands:
        matching_commodity = next((c for c in graph.commodities if c == dem.commodity), None)
        if matching_commodity:
            dem.unscaled_demand = matching_commodity.unscaled_demand
            dem.demand = matching_commodity.demand

    return network_demands 
    


def set_exp_vals_scaled(graph: Graph, ue_flows: dict, demands: list[Demand_Group]):
    """
    This function updates the expected volume of each edge in the graph with respect 
    to the prior belief of each demand group, assuming the demand groups have already 
    been created.

    Note: For use with Aloof and ASCALE. Code is nearly identical to taht of set_exp_vals(),
    but here it is assumed that demand_group objects have already been created.

    Note: Contains a noise_percentage variable that can be adjusted to make the expected
    values of each demand vary from the user equilibrium of the network.
    """
    for demand in demands:
        for edge in demand.edge_list:
            edge_init_index = edge.init_node
            edge_term_index = edge.term_node
            lookup_edge = (str(edge_init_index), str(edge_term_index))
            original_volume = ue_flows[lookup_edge]
            noise_percentage = random.uniform(0, 0)  #Can adjust noise range here
            noisy_volume = original_volume * (1 + noise_percentage)
            noisy_volume = max(noisy_volume, 0)
            demand.expected_volumes[edge] = noisy_volume

    return demands


def set_exp_vals(graph: Graph, ue_flows: dict):
    """
    This function sets the expected volume of each edge in the graph with respect 
    to the prior belief of each demand group. 
    
    Note: Contains a noise_percentage variable that can be adjusted to make the expected
    values of each demand vary from the user equilibrium of the network.
    """
    demands = []

    for commodity in graph.commodities:
        demand = Demand_Group(
                    commodity=commodity,
                    paths=commodity.paths,
                    expected_volumes={},
                    demand = commodity.demand,
                )
            
        demands.append(demand)

    for demand in demands:
        for edge in demand.edge_list:
            edge_init_index = edge.init_node
            edge_term_index = edge.term_node
            lookup_edge = (str(edge_init_index), str(edge_term_index))
            original_volume = ue_flows[lookup_edge]
            noise_percentage = random.uniform(0, 0)  #Can adjust noise range here
            noisy_volume = original_volume * (1 + noise_percentage)
            noisy_volume = max(noisy_volume, 0)
            demand.expected_volumes[edge] = noisy_volume

    return demands


def set_exp_vals(graph: Graph, ue_flows: dict):
    """
    This function sets the expected volume of each edge in the graph with respect 
    to the prior belief of each demand group. 
    
    Note: Contains a noise_percentage variable that can be adjusted to make the expected
    values of each demand vary from the user equilibrium of the network.
    """
    demands = []

    for commodity in graph.commodities:
        demand = Demand_Group(
                    commodity=commodity,
                    paths=commodity.paths,
                    expected_volumes={},
                    demand = commodity.demand,
                )
            
        demands.append(demand)

    for demand in demands:
        for edge in demand.edge_list:
            edge_init_index = edge.init_node
            edge_term_index = edge.term_node
            lookup_edge = (str(edge_init_index), str(edge_term_index))
            original_volume = ue_flows[lookup_edge]
            noise_percentage = random.uniform(0, 0)  #Can adjust noise range here
            noisy_volume = original_volume * (1 + noise_percentage)
            noisy_volume = max(noisy_volume, 0)
            demand.expected_volumes[edge] = noisy_volume

    return demands


def set_path_so_flow(graph: Graph, commodity: Commodity, SO_flows: dict):
    """
    This function gets the system optimal flows of each path given the system 
    optimal edge flows.
    """
    # Create a copy of the SO_flows dictionary to avoid modifying the original
    edge_flows_copy = SO_flows.copy()

    path_flags = {}

    #Flag paths that should have 0.0 flow based on SO edge flows
    for path in commodity.paths:
        zero_flag = any(
            edge_flows_copy.get((str(edge.init_node), str(edge.term_node)), 0.0) == 0.0
            for edge in path.links)
        path_flags[path] = zero_flag

    #Calculate and assign flow for each path
    remaining_demand = commodity.demand
    for path in commodity.paths:
        if remaining_demand == 0:
            path.system_optimal_flow = 0.0
            continue

        if path_flags[path]:
            #This path can't carry flow because one of its edges has no SO flow
            path.system_optimal_flow = 0.0
        else:
            # Determine the maximum flow this path can carry
            min_edge_val = min(
                edge_flows_copy.get((str(edge.init_node), str(edge.term_node)), float("inf"))
                for edge in path.links)

            #The flow assigned to this path is the lesser of remaining demand or min_edge_val
            path_flow = min(remaining_demand, min_edge_val)
            path.system_optimal_flow = path_flow

            # Decrement remaining demand
            remaining_demand -= path_flow

            #Update the edge flows in the copied dictionary
            for edge in path.links:
                edge_key = (str(edge.init_node), str(edge.term_node))
                edge_flows_copy[edge_key] -= path_flow

    #Update the total system optimal flow in the graph
    graph.total_so_flow += sum(path.system_optimal_flow for path in commodity.paths)


def set_so_travel_times(graph: Graph, commodities: list, SO_flows: dict):
    """
    This function iterates through all paths in the network and sets the 
    system_optimal_latency attribute given the SO_flows for each edge in 
    the network have been computed.
    """
    for commodity in commodities:
        for path in commodity.paths:
            if path != []:
                for edge in path.links:
                    edge_key = (str(edge.init_node), str(edge.term_node))
                    if edge_key in SO_flows:
                        edge_latency = parameterized_BPR(current_edge=edge, expected_edge_volume=SO_flows[edge_key])
                        path.system_optimal_latency += edge_latency * SO_flows[edge_key]
                    
                    graph.so_travel_time += edge.travel_time * SO_flows.get(edge_key, 0)


def set_path_capacities(commodities: list):
    """
    This function sets the capcity of each path to the capacity of the edge with minimum capacity within the path.
    Used to uphold bottleneck model of path flows.
    """
    for commodity in commodities:
        for path in commodity.paths:
            if path != []:
                min_edge_cap = float("inf")
                for edge in path.links:
                    if edge.capacity < min_edge_cap:
                        min_edge_cap = edge.capacity
                path.capacity = min_edge_cap


def update_selfish_edge_flows(graph):
    """
    This function sets the selfish_flow attributes of each edge from the SO_flows 
    results after calling Frank Wolfe algorithm.
    """
    for edge in graph.edges:
        edge.selfish_flow = 0.0
    
    #Aggregate selfish path flows into selfish edge flows
    for commodity in graph.commodities:
        for path in commodity.paths:
            for edge in path.links:
                edge.selfish_flow += path.selfish_flow


def update_tasr_edge_flows(graph):
    """
    This function sets the tasr_flow attributes of each edge from the 
    assiged_flow attribute of each path.
    """
    for edge in graph.edges:
        edge.tasr_flow = 0.0
    
    #Aggregate selfish path flows into selfish edge flows
    for commodity in graph.commodities:
        for path in commodity.paths:
            for edge in path.links:
                edge.tasr_flow += path.assigned_flow


def set_so_edge_flows(graph: Graph, so_flows: dict):
    """
    This function sets the system_optimal_flow attribute of all edges 
    in the graph, given the flows in so_flows resulting from the 
    Frank Wolfe algorithm.
    """
    for edge in graph.edges:
        edge.system_optimal_flow = 0.0

    for edge_id, flow in so_flows.items():
        for edge in graph.edges:
            if edge_id == (edge.init_node, edge.term_node):
                edge.system_optimal_flow = flow
                break


def set_scaled_so_edge_flows(graph: Graph, so_flows: dict):
    """
    This function sets the scaled system_optimal_flow attribute of all 
    edges in the graph, given the flows in so_flows resulting from 
    the Frank Wolfe algorithm.
    """
    for edge in graph.edges:
        edge.system_optimal_flow = 0.0

    for edge_id, flow in so_flows.items():
        for edge in graph.edges:
            if edge_id == (edge.init_node, edge.term_node):
                edge.system_optimal_flow = flow
                break