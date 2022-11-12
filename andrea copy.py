#!/usr/bin/env python
import json
import rectangle_packing_solver as rps

with open("./sample_data_1.json") as s:
    data = json.load(s)
    
all_elements = data["elements"]

bed_width = data["bed"]["width"]
bed_height = data["bed"]["height"]

print(f"Maximum width {bed_width}")
print(f"Maximum height {bed_height}")

# https://pypi.org/project/rectangle-packing-solver/

with open("./outputFormat.json") as f:
    solution = json.load(f)

beds = solution["beds"]

solution_is_good = True
for candidate_bed in beds:
    rectangles = []

    for candidate_element in candidate_bed["elements"]:
        id = candidate_element["id"]
        w = all_elements[id]
        
        
    # rectangles = []
    # problem = rps.Problem(rectangles=[
    #     {"width": 10, "height": 10, "rotatable": True},
    #     {"width": 10, "height": 10, "rotatable": True},
    #     {"width": 10, "height": 10, "rotatable": True},
    #     {"width": 10, "height": 10, "rotatable": True},
    # ])


# problem = rps.Problem(rectangles=[
#    {"width": 10, "height": 10, "rotatable": True},
#    {"width": 10, "height": 10, "rotatable": True},
#    {"width": 10, "height": 10, "rotatable": True},
#    {"width": 10, "height": 10, "rotatable": True},
#])
# print("problem:", problem)
# 
# solution = rps.Solver().solve(problem=problem, width_limit = bed_width, height_limit = bed_height, show_progress=True, seed=1111, simanneal_minutes=.01)
# print(solution.floorplan.bounding_box)


# rps.Visualizer().visualize(solution=solution, path="./floorplan_limit.png")