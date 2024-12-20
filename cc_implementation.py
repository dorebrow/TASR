from selfish_operations import get_selfish_route
from process_network import Graph, Commodity, parse_tntp_net_file, parse_tntp_trips_file, find_paths, load_paths_from_file, assign_paths_to_commodities, assign_paths_to_single_commodity
from modify_attributes import Demand_Group, modify_demands, set_exp_vals, set_path_capacities, update_selfish_edge_flows, update_tasr_edge_flows, set_so_edge_flows
from volume_operations import BPR, parameterized_BPR
from frank_wolfe_so_flows import computeAssignment


'''This function sets up the network for and runs the single-commodity version of the CC (System Optimal or SO) algorithm, assuming a single commodity
has been passed to the script.'''
def run_sc_cc(GRAPH: str, SINGLE_COMMODITY: tuple, TOTAL_DEMAND: str):
    graph_net_file = str(GRAPH) + "_net.tntp"
    graph_trips_file = str(GRAPH) + "_trips.tntp"

    graph = Graph()

    edges = parse_tntp_net_file(graph_net_file)
    
    commodities = parse_tntp_trips_file(graph_trips_file)
    
    for edge in edges:
        graph.add_edge(edge)
        #Uncomment for debugging. Some files in the Traffic Networks database aren't clean and have capacities of 0 for some edges,
        #which will break the FW algorithm.
        #if edge.capacity == 0:
        #    print("zero edge capacity here: ", edge.init_node, edge.term_node)
        BPR(edge)

    for commodity in commodities:
        graph.add_commodity(commodity)

    paths_data = load_paths_from_file(GRAPH)
    assign_paths_to_single_commodity(graph, paths_data)

    #Setting attributes of single-commodity in the network
    sc_commodity_name = SINGLE_COMMODITY
    sc_commodity = next((commodity for commodity in graph.commodities if commodity.name == sc_commodity_name), None)
    sc_commodity_list = []
    sc_commodity_list.append(sc_commodity)

    sc_commodity_edges = []
    for path in sc_commodity.paths:
       for e in path.links:
               sc_commodity_edges.append(e)

    sc_graph = Graph()
    sc_graph.edges = sc_commodity_edges
    sc_graph.commodities = sc_commodity_list

    #Set actual demand for single-commodity
    modify_demands(sc_graph, sc_graph.commodities, TOTAL_DEMAND)

    total_demand = 0

    for commodity in sc_graph.commodities:
        total_demand += commodity.demand

    #Compute UE and SO results using FW for given commodity demands in the network
    UE_Results = computeAssignment(sc_graph.edges,
                             commodities=sc_graph.commodities,
                             algorithm="FW",
                             systemOptimal=False)

    SO_Results = computeAssignment(sc_graph.edges,
                             commodities=sc_graph.commodities,
                             algorithm="FW",
                             systemOptimal=True)

    SO_TT, SO_flows = SO_Results
    UE_TT, UE_flows = UE_Results

    network_demands = set_exp_vals(sc_graph, UE_flows)

    for demand in network_demands:
        print(demand.trust)

    for demand in network_demands:
        if demand.commodity.name == sc_commodity_name:
            sc_demand = demand
            sc_commodity.demand = demand.commodity.demand
    
    for edge in sc_graph.edges:
        edge.assigned_flow = SO_flows[(str(edge.init_node), str(edge.term_node))]

    path_bottlenecks = []

    for path in sc_commodity.paths:
        bottle_neck_edge_flow = float('inf')
        for edge in path.links:
            if edge.assigned_flow < bottle_neck_edge_flow:
                bottle_neck_edge_flow = edge.assigned_flow
        path_bottlenecks.append(bottle_neck_edge_flow)

    for path in sc_commodity.paths:
        for i in range(0, len(path.links)):
            sc_demand.assigned_path_volumes[i] = path_bottlenecks[i]

    #Computing regret values; Since demands can split along different paths, keeping track of all
    demand_ratios = [0] * len(sc_commodity.paths)
    demand_regrets = [0] * len(sc_commodity.paths)
    demand_updated_trusts = [0] * len(sc_commodity.paths)
    average_updated_trust = 0
    varepsilon = 0.05 #change as desired

    selfish_latencies = get_selfish_route(sc_commodity, sc_demand)
    sc_demand.selfish_latencies = selfish_latencies

    for i in range(0, len(sc_demand.assigned_path_volumes)):
        if sc_demand.assigned_path_volumes[i] == 0:
            demand_ratios[i] = 0
        else:
            demand_ratios[i] = sc_demand.assigned_path_volumes[i] / sc_demand.demand

    demand_selfish_path = min(sc_demand.selfish_latencies, key=sc_demand.selfish_latencies.get)

    for i in range(0, len(demand_ratios)):
        if demand_ratios[i] == 0:
            demand_regrets[i] = 0
            demand_updated_trusts[i] = sc_demand.trust
        else:
            #Get travel time of selfish path choice
            selfish_path_tt = 0
            for edge in demand_selfish_path.links:
                selfish_path_tt += parameterized_BPR(edge, edge.assigned_flow)

            #Get travel time of assinged path choice
            path_tt = 0
            for edge in sc_demand.paths[i].links:
                if sc_demand.assigned_path_volumes[i] > 0:
                    path_tt += parameterized_BPR(edge, edge.assigned_flow)
            demand_regrets[i] = path_tt - selfish_path_tt

            if demand_regrets[i] <= 0:
                if sc_demand.trust - (varepsilon*-1) >= 1:
                    demand_updated_trusts[i] = 1
                else:
                    demand_updated_trusts[i] = sc_demand.trust - (varepsilon*-1)
            else:
                if sc_demand.trust - (varepsilon*1) <= 0:
                    demand_updated_trusts[i] = 0
                else:
                    demand_updated_trusts[i] = sc_demand.trust - (varepsilon*1)

    for i in range(0, len(demand_ratios)):
        if demand_ratios[i] > 0:
            average_updated_trust += demand_ratios[i] * demand_updated_trusts[i]

    print(f"Total System Travel Time for SO: {SO_TT}")
    print("Total CC flow assigned: ", total_demand)
    print("Total selfish flow assigned: ", total_demand)
    print("Total System Travel Time for CC: ", SO_TT)
    print("Total System Travel Time for Selfish Best Response: ", UE_TT)

    print("Starting Trust Value: ", sc_demand.trust)
    print("Updated Trust Value:", average_updated_trust)



''''This function runs the multi-commodity version of the CC (System Optimal or SO) algorithm, assuming no specific commodity has been passed to the script.'''
def run_mc_cc(GRAPH: str, TOTAL_DEMAND: str):
    graph_net_file = str(GRAPH) + "_net.tntp"
    graph_trips_file = str(GRAPH) + "_trips.tntp"

    graph = Graph()

    edges = parse_tntp_net_file(graph_net_file)
    commodities = parse_tntp_trips_file(graph_trips_file)
    
    for edge in edges:
        graph.add_edge(edge)
        BPR(edge)

    for commodity in commodities:
        graph.add_commodity(commodity)

    constrained_graph = Graph()

    paths_data = load_paths_from_file(GRAPH)
    assign_paths_to_commodities(graph, constrained_graph, paths_data)

    #Set actual demands for each commodity
    modify_demands(constrained_graph, commodities, TOTAL_DEMAND)

    total_demand = 0

    for commodity in constrained_graph.commodities:
        total_demand += commodity.demand

    #Compute UE and SO results using FW for given commodity demands in the network
    UE_Results = computeAssignment(constrained_graph.edges,
                             commodities=constrained_graph.commodities,
                             algorithm="FW",
                             systemOptimal=False)

    SO_Results = computeAssignment(constrained_graph.edges,
                             commodities=constrained_graph.commodities,
                             algorithm="FW",
                             systemOptimal=True)

    SO_TT, SO_flows = SO_Results
    UE_TT, UE_flows = UE_Results

    print(f"Total System Travel Time for SO: {SO_TT}")
    print("Total CC flow assigned: ", total_demand)
    print("Total selfish flow assigned: ", total_demand)
    print("Total System Travel Time for CC: ", SO_TT)
    print("Total System Travel Time for Selfish Best Response: ", UE_TT)
    print("Total System Travel Time for All Demand:", SO_TT)