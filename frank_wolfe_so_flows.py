import heapq
import math
import time
import numpy as np
import networkx as nx
import scipy
from process_network import Edge


class FlowTransportNetwork:
    def __init__(self):
        self.linkSet = {}
        self.nodeSet = {}
        self.tripSet = {}
        self.zoneSet = {}
        self.originZones = {}
        self.networkx_graph = None

    def to_networkx(self):
        if self.networkx_graph is None:
            self.networkx_graph = nx.DiGraph([(int(begin), int(end)) for (begin, end) in self.linkSet.keys()])
        return self.networkx_graph

    def reset_flow(self):
        for link in self.linkSet.values():
            link.reset_flow()

    def reset(self):
        for link in self.linkSet.values():
            link.reset()


class Demand:
    def __init__(self, init_node: str, term_node: str, demand: float):
        self.fromZone = init_node
        self.toNode = term_node
        self.demand = float(demand)


class Link:
    def __init__(self, edge: Edge):
        self.init_node = edge.init_node
        self.term_node = edge.term_node
        self.capacity = edge.capacity
        self.fft = edge.fft
        self.beta = 4
        self.alpha = 0.15
        self.curr_capacity_percentage = 1
        self.flow = 0.0
        self.cost = self.fft

    def reset(self):
        self.curr_capacity_percentage = 1
        self.flow = 0.0
        self.cost = self.fft

    def reset_flow(self):
        self.flow = 0.0
        self.cost = self.fft


class Node:
    """
    This class has attributes associated with any node
    """
    def __init__(self, nodeId: str):
        self.Id = nodeId

        self.lat = 0
        self.lon = 0

        self.outLinks = []
        self.inLinks = []

        self.label = np.inf
        self.pred = None


class Zone:
    def __init__(self, zoneId: str):
        self.zoneId = zoneId

        self.lat = 0
        self.lon = 0
        self.destList = []


def BPRcostFunction(optimal: bool,
                    fft: float,
                    flow: float,
                    capacity: float) -> float:
    if capacity < 1e-3:
        return np.finfo(np.float32).max
    if optimal:
        return fft * (1 + (0.15 * math.pow((flow / capacity), 9)) * (4 + 1))
    return fft * (1 + 0.15 * math.pow((flow / capacity), 9))


def readNetwork(edges, network: FlowTransportNetwork):
    for edge in edges:
        init_node = edge.init_node
        term_node = edge.term_node
        link = Link(edge)
        network.linkSet[(init_node, term_node)] = link
        
        if init_node not in network.nodeSet:
            network.nodeSet[init_node] = Node(init_node)
        if term_node not in network.nodeSet:
            network.nodeSet[term_node] = Node(term_node)

        if term_node not in network.nodeSet[init_node].outLinks:
            network.nodeSet[init_node].outLinks.append(term_node)
        if init_node not in network.nodeSet[term_node].inLinks:
            network.nodeSet[term_node].inLinks.append(init_node)


def readDemand(commodities, network: FlowTransportNetwork):
    for commodity in commodities:
        init_node = str(commodity.init_node)
        term_node = str(commodity.term_node)
        demand = commodity.demand
        if init_node not in network.originZones:
            network.originZones[init_node] = True
            if init_node not in network.nodeSet:
                network.nodeSet[init_node] = Node(init_node)

        if term_node not in network.nodeSet:
            network.nodeSet[term_node] = Node(term_node)

        network.tripSet[(init_node, term_node)] = Demand(init_node, term_node, demand)
        if init_node not in network.zoneSet:
            network.zoneSet[init_node] = Zone(init_node)
        if term_node not in network.zoneSet:
            network.zoneSet[term_node] = Zone(term_node)
        if term_node not in network.zoneSet[init_node].destList:
            network.zoneSet[init_node].destList.append(term_node)


def load_network(edges: list) -> FlowTransportNetwork:
    network = FlowTransportNetwork()
    readNetwork(edges, network)

    return network


def get_TSTT(network: FlowTransportNetwork, costFunction=BPRcostFunction):
    TSTT = round(sum([network.linkSet[a].flow * costFunction(optimal=False, fft=network.linkSet[a].fft,
                                                             flow=network.linkSet[a].flow,
                                                             capacity=network.linkSet[a].capacity) for a in network.linkSet]), 12)
    return TSTT


def DijkstraHeap(origin, network: FlowTransportNetwork):
    for n in network.nodeSet:
        n = str(n)
        network.nodeSet[n].label = np.inf
        network.nodeSet[n].pred = None
    
    origin = str(origin)
    network.nodeSet[origin].label = 0.0
    network.nodeSet[origin].pred = None
    SE = [(0.0, origin)] 

    while SE:
        currentLabel, currentNode = heapq.heappop(SE) 
        currentLabel = float(currentLabel)
        currentNode = str(currentNode) 

        for toNode in network.nodeSet[currentNode].outLinks:
            toNode = str(toNode)
            link = (currentNode, toNode)
            cost = float(network.linkSet[link].cost)
            newLabel = currentLabel + cost 

            existingLabel = float(network.nodeSet[toNode].label) 

            if newLabel < existingLabel:
                heapq.heappush(SE, (newLabel, toNode))
                network.nodeSet[toNode].label = newLabel
                network.nodeSet[toNode].pred = currentNode


def tracePreds(dest, network: FlowTransportNetwork):
    """
    This method traverses predecessor nodes in order to create a shortest path.
    """
    prevNode = network.nodeSet[dest].pred
    spLinks = []
    while prevNode is not None:
        spLinks.append((prevNode, dest))
        dest = prevNode
        prevNode = network.nodeSet[dest].pred
    return spLinks


def loadAON(network: FlowTransportNetwork, computeXbar: bool = True):
    """
    This method produces auxiliary flows for all or nothing loading.
    """

    #initialization of x_bar and SPTT
    x_bar = {l: 0.0 for l in network.linkSet}
    #Dictionary where the auxiliary flows (initialized to zero) for each link 
    #will be stored. This dictionary will eventually hold the total demand assigned 
    #along each link according to the shortest paths.
    SPTT = 0.0
    #Represents the sum of travel times along shortest paths for all origin-destination 
    #pairs, weighted by demand.

    #Loops through all origin zones, computing shortest paths from r
    #to all destinations in the network.
    for r in network.originZones:
        #Computes a shortest path label (distance) from origin r to each destination
        #representing minimum travel cost from origin r to that destination
        DijkstraHeap(r, network=network)

        for s in network.zoneSet[r].destList:
            dem = network.tripSet[r, s].demand
            #For each origin-destination pair, computes shortest
            #path travel time from r to s by multiplying minimum travel
            #cost by the demand

            SPTT = SPTT + network.nodeSet[s].label * dem

            #Computes auxiliary flows - gets edges in shortest path from r to s, and
            #gets demand on each of those links
            if computeXbar and r != s:
                for spLink in tracePreds(s, network):
                    x_bar[spLink] = x_bar[spLink] + dem

    #Returns initial cost estimate SPTT and auxiliary flow (initial direction) to be used in flow adjustment
    return SPTT, x_bar


def findAlpha(x_bar, network: FlowTransportNetwork, optimal: bool = False, costFunction=BPRcostFunction):
    """
    This uses unconstrained optimization to calculate the optimal step size required
    for Frank-Wolfe Algorithm. Minimizes the derivative of the BPR function using unconstrained
    optimization.
    """

    def df(alpha):
        assert 0 <= alpha <= 1
        sum_derivative = 0  #Derivative of the objective function
        for l in network.linkSet:
            tmpFlow = alpha * x_bar[l] + (1 - alpha) * network.linkSet[l].flow
            tmpCost = costFunction(optimal,
                                   network.linkSet[l].fft,
                                   tmpFlow,
                                   network.linkSet[l].capacity,
                                   )
            sum_derivative = sum_derivative + (x_bar[l] - network.linkSet[l].flow) * tmpCost
        return sum_derivative

    sol = scipy.optimize.root_scalar(df, x0=np.array([0.5]), bracket=(0, 1))
    assert 0 <= sol.root <= 1
    return sol.root


def updateTravelTime(network: FlowTransportNetwork, optimal: bool = False, costFunction=BPRcostFunction):
    """
    This method updates the travel time on the links with the current flow
    """
    for l in network.linkSet:
        network.linkSet[l].cost = costFunction(optimal, network.linkSet[l].fft, network.linkSet[l].flow, network.linkSet[l].capacity)


def assignment_loop(network: FlowTransportNetwork,
                    algorithm: str = "FW",
                    systemOptimal: bool = False,
                    costFunction=BPRcostFunction,
                    accuracy: float = 0.001,
                    maxIter: int = 1000,
                    maxTime: int = 120):
    """
    Uses step size from findAlpha to update link flows by combining current
    flow and auxiliary flow with alpha. Iterates until gap between TSTT and SPTT is within acceptable
    threshold or maximum number of iterations have passed.
    """
    
    network.reset_flow()

    iteration_number = 1
    gap = np.inf
    TSTT = np.inf
    assignmentStartTime = time.time()

    while gap > accuracy:

        _, x_bar = loadAON(network=network)

        if algorithm == "MSA" or iteration_number == 1:
            alpha = (1 / iteration_number)
        elif algorithm == "FW":
            alpha = findAlpha(x_bar,
                              network=network,
                              optimal=systemOptimal,
                              costFunction=costFunction)
        else:
            print("Terminating the program.....")
            print("The solution algorithm ", algorithm, " does not exist!")
            raise TypeError('Algorithm must be MSA or FW')

        #Sets the new flow on each link to incrementally move towards system optimal solution.
        for l in network.linkSet:
            network.linkSet[l].flow = alpha * x_bar[l] + (1 - alpha) * network.linkSet[l].flow

        updateTravelTime(network=network,
                         optimal=systemOptimal,
                         costFunction=costFunction)

        SPTT, _ = loadAON(network=network, computeXbar=False)
        SPTT = round(SPTT, 12)
        TSTT = round(sum([network.linkSet[a].flow * network.linkSet[a].cost for a in
                          network.linkSet]), 12)

        if SPTT == 0:
            print("SPTT is zero. No flow can be assigned.")
            edge_flows = {edge: link.flow for edge, link in network.linkSet.items()}
            return TSTT, edge_flows

        gap = (TSTT / SPTT) - 1
        if gap < 0:
            print("Error, gap is less than 0, this should not happen")
            print("TSTT", "SPTT", TSTT, SPTT)

        TSTT = get_TSTT(network=network, costFunction=costFunction)

        iteration_number += 1
        if iteration_number > maxIter:
            edge_flows = {edge: link.flow for edge, link in network.linkSet.items()}
            return TSTT, edge_flows
        if time.time() - assignmentStartTime > maxTime:
            edge_flows = {edge: link.flow for edge, link in network.linkSet.items()}
            return TSTT, edge_flows

    edge_flows = {edge: link.flow for edge, link in network.linkSet.items()}

    return TSTT, edge_flows


def computeAssignment(edges:list,
                      commodities: list,
                      algorithm: str = "FW", 
                      costFunction=BPRcostFunction,
                      systemOptimal: bool = False,
                      accuracy: float = 0.0001,
                      maxIter: int = 1000,
                      maxTime: int = 60) -> float:

    network = load_network(edges)

    readDemand(commodities, network)

    TSTT = assignment_loop(network=network, algorithm=algorithm, systemOptimal=systemOptimal, costFunction=costFunction,
                           accuracy=accuracy, maxIter=maxIter, maxTime=maxTime)


    return TSTT
