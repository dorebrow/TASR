from process_network import Commodity
from modify_attributes import Demand_Group
from volume_operations import parameterized_BPR


''''This function computes the best-response path choice of a demand group assuming they choose their best response
selfishly (path with lowest total latency based on their prior belief [expected edge volumes]).'''
def get_selfish_route(commodity: Commodity, demand_group: Demand_Group):
    selfish_latencies = {}

    if len(commodity.paths) == 0:
        print("no paths")
    for path in commodity.paths:
        selfish_path_latency = 0.0
        for edge in path.links:
            expected_volume = demand_group.expected_volumes[edge]
            selfish_path_latency = selfish_path_latency + parameterized_BPR(edge, expected_volume)
        
        selfish_latencies[path] = selfish_path_latency
    
    return selfish_latencies