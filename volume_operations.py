from process_network import Edge
import math

BPR_ALPHA = 0.15
BPR_BETA = 4

'''This function computes the travel time of an edge using the Bureau of Public Roads (BPR) function.'''
def BPR(current_edge: Edge):
    if current_edge.volume == 0.0:
        current_edge.travel_time = current_edge.fft

    else:
        current_edge.travel_time = round(
            current_edge.fft * (1 + (BPR_ALPHA * math.pow((current_edge.volume / current_edge.capacity), BPR_BETA))), 9)


'''This function computes the travel time of an edge using the Bureau of Public Roads (BPR) function, given an expected edge volume.'''
def parameterized_BPR(current_edge: Edge, expected_edge_volume: float) -> float:
    edge_latency = 0.0

    if expected_edge_volume == 0.0:
        edge_latency += current_edge.fft
    else:
        edge_latency += round(current_edge.fft * (1 + (BPR_ALPHA * math.pow((expected_edge_volume / current_edge.capacity), BPR_BETA))), 9)
    return edge_latency