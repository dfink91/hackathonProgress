#!/usr/bin/env python

import json
import EasyGA
import random
import numpy as np
from check_concrete_correctness import checkConcreteCorrectness
from checkStackCorrectness import checkStackCorrectness
from check_if_it_fits import check_if_bed_contains_valid_rectangles

ga = EasyGA.GA()
file_path = "sample_data_4.json"
f = open(file_path)
data = json.load(f)


bed_sizes = data["bed"]
max_stacks = data["maxStacks"]
maximum_bed_width = data["bed"]["width"]
maximum_bed_height = data["bed"]["height"]

elements = data["elements"]

elements_size = len(elements)


def convert_solution_to_output_format(solution):
    beds = []
    unique = np.unique(solution)

    # print(solution)

    for u in unique:
        output = []
        for i, s in enumerate(solution):
            if s == u:
                output.append(elements[i])
        beds.append({"id": int(u), "elements": output})
    output = {"beds": beds}
    output_json = json.dumps(output)
    return {"beds": beds}


def fitness_func(solution):

    solution = np.array(solution)

    solution = list(map(lambda x: int(x.value), solution))

    output_format = convert_solution_to_output_format(solution)

    unfitness = 0
    if not checkConcreteCorrectness(json.dumps(data), json.dumps(output_format)):
        unfitness = 10000000
    
    if not checkStackCorrectness(json.dumps(data), json.dumps(output_format)):
        unfitness += 1000000

    if not check_if_bed_contains_valid_rectangles(maximum_bed_width, maximum_bed_height, output_format):
        unfitness += 1000000

    unique = np.unique(solution)
    result = len(unique) + unfitness

    return result 


ga.fitness_function_impl = fitness_func
ga.population_size = 1000
ga.generation_goal = 10
ga.chromosome_length = elements_size
ga.target_fitness_type = "min"

random.seed(30)
ga.gene_impl = lambda: random.randint(0, elements_size)
ga.evolve()

# Print out the current generation and the population
# ga.print_generation()
# ga.print_population()

beds = []

solution = [s for s in ga.population[0]]
solution = list(map(lambda x: int(x.value), solution))
unique = np.unique(solution)

for u in unique:
    output = []
    for i, s in enumerate(solution):
        if s == u:
            output.append(elements[i])
    beds.append({"id": u, "elements": output})

print(solution)
# print(beds)
