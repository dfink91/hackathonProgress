from platform import node
import pygad
import numpy
import xml.etree.ElementTree as ET
import networkx as nx
from functools import reduce

xml_path = 'simulated20220218.xml'
root = ET.parse(xml_path)
edges = root.findall('./Edges/Edge')
nodes = root.findall('./Nodes/Node')

def node_exists(index): 
    result = [a for a in nodes if a.attrib["index"] == str(index)]
    return result != []

def get_node_name(index):
    result = [a for a in nodes if a.attrib["index"] == str(index)]
    return result[0].attrib["activity"]

def get_graph():    
    graph = nx.Graph()
    for node_index in range(len(nodes)):
        for edge in edges:
            source = int(edge.attrib['sourceIndex'])
            target = int(edge.attrib['targetIndex'])

            if(source == node_index and node_exists(source) and node_exists(target)):
                frequency = int(edge.find('./Frequency').attrib['total'])
                graph.add_edge(source, target, weight=frequency)

    return graph

def fitness_function_for_microservice(graph, solution, microservice):
    nodes_present_in_solution = []
    for index in range(len(solution)):
        if solution[index] == microservice:
            nodes_present_in_solution.append(index)
    
    nodes_present_in_solution = graph.subgraph(nodes_present_in_solution)
    return len(nodes_present_in_solution) * len(nodes_present_in_solution)

    

    # 
    # if (not nx.is_connected(nodes_present_in_solution) and len(nodes_present_in_solution)>1):
    #     return -100000

    # all_weights = []
    # for i in nx.edges(nodes_present_in_solution):
    #     all_weights.append((graph[i[0]][i[1]]["weight"]))
    # mean_all_weights = sum(all_weights)/len(all_weights)

    # #number_of_nodes = solution.count(microservice)
    # # print(microservice_G)

    # #microservice_G_mst = nx.minimum_spanning_tree(microservice_G)
    # #e = nx.eccentricity(microservice_G_mst)
    # #longest_path = max(e.values())
    # inter_weight = []
    # # print(solution)
    # i = 0
    # # print(list(microservice_G.nodes))
    # for ms in solution:
    #     if ms == microservice:
    #         neighbours = nx.neighbors(graph, i)
    #         for n in neighbours:
    #             if(solution[n] != microservice):
    #                 inter_weight.append(graph[i][n]["weight"])
    #     i += 1
    # mean_inter_weight = sum(inter_weight)/len(inter_weight)
    # result = mean_all_weights - mean_inter_weight



def fitness_func(solution, _):
    # We assume that a solution has the format [1, 1, 2, 3, 4, 4, 1]
    # unique = numpy.unique(solution)
    # fitness_function_for_cluster = numpy.vectorize(lambda microservice: fitness_function_for_microservice(graph, solution, microservice))
    # result = numpy.sum(fitness_function_for_cluster(unique))
    # return result
    unique, counts = numpy.unique(0, return_counts=True)
    return 1

graph = get_graph()

num_generations = 10
num_parents_mating = 1

parent_selection_type = "random"

crossover_type = "single_point"

mutation_type = "random"
mutation_percent_genes = 0

def on_generation(ga_instance):   
    print("=======")
    print(ga_instance.population)





ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_func,
                       sol_per_pop=10,
                       num_genes=len(nodes),
                       init_range_low=0,
                       init_range_high=len(nodes),
                       parent_selection_type=parent_selection_type,
                       keep_parents=1,
                       crossover_type=crossover_type,
                       mutation_type=None,
                       mutation_percent_genes=mutation_percent_genes,
                       gene_type=int,
                       callback_generation=on_generation,
                       save_best_solutions=True
                       )

print(ga_instance.initial_population)

ga_instance.run()
# #ga_instance.plot_fitness()

# solution, solution_fitness, solution_idx = ga_instance.best_solution()
# print("Parameters of the best solution : {solution}".format(solution=solution))
# print("Fitness value of the best solution = {solution_fitness}".format(
#     solution_fitness=solution_fitness))

# if ga_instance.best_solution_generation != -1:
#     print("Best fitness value reached after {best_solution_generation} generations.".format(best_solution_generation=ga_instance.best_solution_generation))


# print(len(nodes))
# for g in range(len(nodes)):
#     header_printed = False

#     for index, s in enumerate(solution):
#         if s == g:
#             if not header_printed:
#                 header_printed = True
#                 print(f"Cluster {g}:")

#             print(get_node_name(index))


# #prediction = numpy.sum(numpy.array(function_inputs)*solution)
# #print("Predicted output based on the best solution : {prediction}".format(prediction=prediction))
