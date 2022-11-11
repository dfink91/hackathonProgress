
#!/usr/bin/env python3

import EasyGA
import numpy as np
import xml.etree.ElementTree as ET
import networkx as nx
import random
import logging 

def get_graph(xml):
    def node_exists(index):
        result = [a for a in nodes if a.attrib["index"] == str(index)]
        return result != []

    def get_node_name(index):
        result = [a for a in nodes if a.attrib["index"] == str(index)]
        return result[0].attrib["activity"]

    root = ET.parse(xml)
    edges = root.findall("./Edges/Edge")
    nodes = root.findall("./Nodes/Node")

    graph = nx.Graph()
    for node_index in range(len(nodes)):
        for edge in edges:
            source = int(edge.attrib["sourceIndex"])
            target = int(edge.attrib["targetIndex"])

            if source == node_index and node_exists(source) and node_exists(target):
                frequency = int(edge.find("./Frequency").attrib["total"])
                graph.add_node(source, name=get_node_name(source))
                graph.add_node(target, name=get_node_name(target))
                graph.add_edge(source, target, weight=frequency)

    return graph

def calculate_average_inter_microservice_weight(graph, solution, microservice):
    nodes_present_in_current_microservice = []
    for index in range(len(solution)):
        if solution[index] == microservice:
            nodes_present_in_current_microservice.append(index)

    nodes_present_in_current_microservice = graph.subgraph(nodes_present_in_current_microservice)
    if (not nx.is_connected(nodes_present_in_current_microservice) and len(nodes_present_in_current_microservice)>1):
        return -1000

    if len(nodes_present_in_current_microservice)==1:
        return -1000

    inter_microservice_weights = [0]
    for edge in nx.edges(nodes_present_in_current_microservice):
        source = edge[0]
        target = edge[1]
        inter_microservice_weights.append(graph[source][target]["weight"])
    result = np.mean(inter_microservice_weights)
    return result

def fitness_function_for_microservice(graph, solution, currently_evaluated_microservice):
    # Calculate the value of the proposed microservice
    average_inter_microservice_weight = calculate_average_inter_microservice_weight(graph, solution, currently_evaluated_microservice)

    intra_microservice_distances = [0]
    for node_index, m in enumerate(solution):
        if m == currently_evaluated_microservice:
            neighbours = nx.neighbors(graph, node_index)
            for n in neighbours:
                microservice_to_which_the_neighbour_belongs = solution[n]
                if(microservice_to_which_the_neighbour_belongs != currently_evaluated_microservice):
                    source = node_index
                    target = n

                    microservice_to_which_source_belongs = solution[source]
                    average_inter_microservice_weight_of_microservice_to_which_source_belongs = calculate_average_inter_microservice_weight(graph, solution, microservice_to_which_source_belongs)
                    
                    outbound_weight = graph[source][target]["weight"]
                    distance = average_inter_microservice_weight_of_microservice_to_which_source_belongs - outbound_weight
                    intra_microservice_distances.append(distance)

    average_intra_microservice_weights = np.mean(intra_microservice_distances)

    result = average_inter_microservice_weight + average_intra_microservice_weights
    return result

def main():
    logging.basicConfig(format="%(message)s", level=1 * 10)
    logging.info("Loading XML...")
    graph = get_graph("simulated20220218_2.xml")

    # This function receives solutions in the format of [[1][2][3]] and each element is of type Gene.
    def fitness_func(solution):
        solution = np.array(solution).flatten()
        solution = list(map(lambda x: int(x.value), solution))
        unique = np.unique(solution)
        
        fitness_function_for_cluster = np.vectorize(lambda microservice: fitness_function_for_microservice(graph, solution, microservice))
        result = np.sum(fitness_function_for_cluster(unique))
        return result

    logging.info(f"Found {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges.")
       
    ga = EasyGA.GA()
    ga.fitness_function_impl = fitness_func
    ga.population_size = 1000
    ga.generation_goal = 100
    ga.chromosome_length = graph.number_of_nodes()
    ga.target_fitness_type = 'max'
        
    nodes_list = [n for n in graph.nodes]    
    ga.gene_impl = lambda: random.choice(nodes_list)

    ga.evolve()

    # Print out the current generation and the population
    ga.print_generation()
    ga.print_population()
    #print(ga.population[0])

    solution = [s for s in ga.population[0]]
    print(solution)

    node_names = nx.get_node_attributes(graph, "name")
    
    solution = np.array(solution).flatten()
    solution = list(map(lambda x: int(x.value), solution))
    unique = np.unique(solution)
    
    for unique_microservice in unique:
        print(f"Looking at microservice {unique_microservice}: ", end = "")
        for index, current_microservice in enumerate(solution):
            if unique_microservice == current_microservice:
                print(node_names[index], end = ' ')
        print("")






if __name__ == "__main__":
    main()


