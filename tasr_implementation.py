from selfish_operations import get_selfish_route
from process_network import Graph, Commodity, parse_tntp_net_file, parse_tntp_trips_file, find_paths, load_paths_from_file, assign_paths_to_commodities, assign_paths_to_single_commodity
from modify_attributes import Demand_Group, modify_demands, set_exp_vals, set_path_capacities, update_selfish_edge_flows, update_tasr_edge_flows, set_so_edge_flows
from volume_operations import BPR, parameterized_BPR
from frank_wolfe_so_flows import computeAssignment


"""A function that performs the TASR algorithm for a single commodity. It accepts two parameters: a graph object 
representing the traffic network, and a commodity object which contains relevant attributes 
such as demand."""
def TASR(graph_object: Graph, commodity_object: Commodity, demand_group: Demand_Group):

    #Sort paths by increasing latency given SO flows
    ordered_paths = sorted(commodity_object.paths, key=lambda path: path.system_optimal_latency)

    #Selfish demand allocation
    selfish_latencies = get_selfish_route(commodity_object, demand_group)
    selfish_path_choice = min(selfish_latencies, key=selfish_latencies.get)
    demand_group.selfish_latencies = selfish_latencies

    remaining_demand = demand_group.demand * demand_group.trust
    non_compliant_demand = demand_group.demand * (1 - demand_group.trust)

    exceeded_so_edges = set()
    saturated_paths = set()

    for path in commodity_object.paths:
        if path == selfish_path_choice:
            path.assigned_flow += non_compliant_demand
            
            for i in range(0, len(commodity_object.paths)):
                if path == commodity_object.paths[i]:
                    demand_group.assigned_path_volumes[i] = non_compliant_demand
                else:
                    demand_group.assigned_path_volumes[i] = 0

            for edge in path.links:
                edge.assigned_flow += non_compliant_demand
                        
            for edge in path.links:
                if edge.assigned_flow >= edge.system_optimal_flow:
                    exceeded_so_edges.add(edge)
                    saturated_paths.add(path)
        else:
            continue

    non_compliant_demand = 0 

    #Allocate remaining demand to paths
    for path in ordered_paths:
        if remaining_demand <= 0:
            break

        if path in saturated_paths:
            continue

        #Calculate the actual allowable flow for the path
        actual_allowable_flow = float('inf')
        for edge in path.links:
            if edge not in exceeded_so_edges:
                actual_allowable_flow = min(actual_allowable_flow, edge.system_optimal_flow - edge.assigned_flow)
        
        #Skip if no flow can be assigned to this path
        if actual_allowable_flow <= 0:
            continue

        #Allocate flow to the path
        if remaining_demand <= actual_allowable_flow:
            path.assigned_flow += remaining_demand
            for i in range(0, len(commodity_object.paths)):
                if path == commodity_object.paths[i]:
                    demand_group.assigned_path_volumes[i] += remaining_demand
            for edge in path.links:
                edge.assigned_flow += remaining_demand
            remaining_demand = 0
            for edge in path.links:
                if edge.assigned_flow >= edge.system_optimal_flow:
                    exceeded_so_edges.add(edge)
                    saturated_paths.add(path)
        else:
            flow_to_allocate = actual_allowable_flow
            path.assigned_flow += flow_to_allocate
            for i in range(0, len(commodity_object.paths)):
                if path == commodity_object.paths[i]:
                    demand_group.assigned_path_volumes[i] += flow_to_allocate
            for edge in path.links:
                edge.assigned_flow += flow_to_allocate
            remaining_demand -= flow_to_allocate

            for edge in path.links:
                if edge.assigned_flow >= edge.system_optimal_flow:
                    exceeded_so_edges.add(edge)
                    saturated_paths.add(path)

    #Updates the selfish flow attribute of the selfishly chosen path
    for path in commodity_object.paths:
        if selfish_path_choice == path:
            path.selfish_flow = path.selfish_flow + demand_group.demand

    graph_object.total_selfish_flow += selfish_path_choice.selfish_flow

    for path in commodity_object.paths:
        demand_group.demand_serviced += path.assigned_flow
        demand_group.selfish_path = selfish_path_choice


'''This function sets up the network for and runs the single-commodity version of the TASR algorithm, assuming a single commodity
has been passed to the script.'''
def run_sc_tasr(GRAPH: str, SINGLE_COMMODITY: tuple, TOTAL_DEMAND: str):
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
               if e not in sc_commodity_edges:
                   sc_commodity_edges.append(e)
    
    sc_graph = Graph()
    sc_graph.edges = sc_commodity_edges
    sc_graph.commodities = sc_commodity_list

    #Set actual demand for single-commodity
    modify_demands(sc_graph, sc_graph.commodities, TOTAL_DEMAND)

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

    print(f"Total System Travel Time for SO: {SO_TT}")

    #Uncomment below to see information on UE of network under complete compliance of all drivers
    #print(f"Total System Travel Time for UE: {UE_TT}")
    #print("UE - SO = ", UE_TT - SO_TT)

    network_demands = set_exp_vals(sc_graph, UE_flows)

    for demand in network_demands:
        if demand.commodity.name == sc_commodity_name:
            sc_demand = demand
            sc_commodity.demand = demand.commodity.demand

    #Single demand group, so no need to sort demand groups

    set_path_capacities(sc_graph.commodities)
    set_so_edge_flows(sc_graph, SO_flows)

    TASR(sc_graph, sc_commodity, sc_demand)

    #Update assigned path flows for current demand group
    for i in range (0, len(sc_demand.paths)):
        sc_demand.assigned_path_volumes[i] = sc_demand.paths[i].assigned_flow

    #Computing regret values; Since demands can split along different paths, keeping track of all
    demand_ratios = [0] * len(sc_commodity.paths)
    demand_regrets = [0] * len(sc_commodity.paths)
    demand_updated_trusts = [0] * len(sc_commodity.paths)
    average_updated_trust = 0
    varepsilon = 0.05 #change as desired

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

    total_selfish_travel_time = 0.0

    for path in sc_commodity.paths:
        for edge in path.links:
            selfish_edge_latency = parameterized_BPR(edge, path.selfish_flow)
            total_selfish_travel_time += round(selfish_edge_latency * path.selfish_flow, 9)
    
    graph.br_travel_time = total_selfish_travel_time

    total_network_travel_time = 0.0

    for edge in sc_graph.edges:
        edge_travel_time = parameterized_BPR(edge, edge.assigned_flow)
        total_network_travel_time += round(edge_travel_time * edge.assigned_flow, 9)

    total_tasr_flow_assigned = 0

    for commodity in sc_graph.commodities:
        if len(commodity.paths) > 0:
            for path in commodity.paths:
                total_tasr_flow_assigned = total_tasr_flow_assigned + path.assigned_flow 
                total_br_flow_assigned = total_tasr_flow_assigned + path.selfish_flow

    print("Total TASR flow assigned: ", total_tasr_flow_assigned)
    print("Total selfish flow assigned: ", total_br_flow_assigned)
    print("Total System Travel Time for TASR: ", total_network_travel_time)
    print("Total System Travel Time for Selfish Best Response: ", graph.br_travel_time)

    print("Starting Trust Value: ", sc_demand.trust)
    print("Updated Trust Value:", average_updated_trust)



''''This function runs the multi-commodity version of TASR, assuming no specific commodity has been passed to the script.'''
def run_mc_tasr(GRAPH: str, TOTAL_DEMAND: str):
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

    #Uncomment below to see information on UE of network under complete compliance of all drivers
    #print(f"Total System Travel Time (TSTT) for UE: {UE_TT}")
    #print("UE - SO = ", UE_TT - SO_TT)

    network_demands = set_exp_vals(constrained_graph, UE_flows)

    #Sort demand groups by increasing trust
    ordered_demand_groups = sorted(network_demands, key=lambda dg: dg.trust)

    #Soring by decreasing trust gives TASR less control over compensating for flows of noncompliant (or less compliant) demand
    #ordered_demand_groups = sorted(network_demands, key=lambda dg: dg.trust, reverse=True)

    #Set path capacities and so_flows
    set_path_capacities(constrained_graph.commodities)
    set_so_edge_flows(constrained_graph, SO_flows)

    #instead of sorting commodities by greatest ratio of noncompliant demand to compliant demand,
    #since we're only dealing with partially compliant demands, sort by increasing trust (essentially the same thing)

    for demand_group in ordered_demand_groups:
        # Skip commodities that don't actually have any paths connecting them
        if len(demand_group.commodity.paths) == 0:
            continue
        TASR(constrained_graph, demand_group.commodity, demand_group)
        
        for i in range (0, len(demand_group.paths)):
            demand_group.assigned_path_volumes[i] = demand_group.paths[i].assigned_flow

    total_selfish_travel_time = 0.0

    update_selfish_edge_flows(constrained_graph)
    update_tasr_edge_flows(constrained_graph)

    total_selfish_travel_time = 0.0
    total_br_flow_assigned = 0

    for edge in constrained_graph.edges:
        selfish_edge_latency = parameterized_BPR(edge, edge.selfish_flow)
        total_selfish_travel_time += (selfish_edge_latency * edge.selfish_flow)

    for commodity in constrained_graph.commodities:
        if len(commodity.paths) > 0:
            for path in commodity.paths:
                total_br_flow_assigned = total_br_flow_assigned + path.selfish_flow
        
    constrained_graph.br_travel_time = total_selfish_travel_time

    total_network_travel_time = 0.0
    total_tasr_flow_assigned = 0

    for edge in constrained_graph.edges:
        tasr_edge_latency = parameterized_BPR(edge, edge.tasr_flow)
        total_network_travel_time += (tasr_edge_latency * edge.tasr_flow)

    for commodity in constrained_graph.commodities:
        if len(commodity.paths) > 0:
            for path in commodity.paths:
                total_tasr_flow_assigned = total_tasr_flow_assigned + path.assigned_flow

    total_true_tt = 0

    for dem in ordered_demand_groups:
        demand_unserviced = dem.unscaled_demand - dem.demand_serviced
        for path in dem.commodity.paths:
            if path != dem.selfish_path_choice:
                for edge in path.links:
                    total_true_tt += edge.assigned_flow * parameterized_BPR(edge, edge.assigned_flow)
            else:
                for edge in path.links:
                    total_true_tt += (edge.assigned_flow + demand_unserviced) * parameterized_BPR(edge, edge.assigned_flow + demand_unserviced)

    print("Total TASR flow assigned: ", total_tasr_flow_assigned)
    print("Total selfish flow assigned: ", total_br_flow_assigned)
    print("Total System Travel Time for TASR: ", total_network_travel_time)
    print("Total System Travel Time for Selfish Best Response: ", constrained_graph.br_travel_time)
    print("Total System Travel Time for All Demand:", total_true_tt)