#!/usr/bin/env python
import json
import rectangle_packing_solver as rps

def check_if_bed_contains_valid_rectangles(maximum_bed_width, maximum_bed_height, solution):
    # https://pypi.org/project/rectangle-packing-solver/

    beds = solution["beds"]

    problem = rps.Problem(rectangles=[
        [4, 6],  # Format: [width, height] as list. Default rotatable: False
        (4, 4),  # Format: (width, height) as tuple. Default rotatable: False
        {"width": 2.1, "height": 3.2, "rotatable": False},  # Or can be defined as dict.
        {"width": 1, "height": 5, "rotatable": True}
    ])
    print("problem:", problem)

    solution_is_good = True
    solution_beds = []
    for candidate_bed in beds:
        boxes = []

        for candidate_element in candidate_bed["elements"]:
            id = candidate_element["id"]
            w = all_elements[id]["width"]
            h = all_elements[id]["height"]
            boxes.append({"width": w, "height": h, "rotatable": True})
            
        problem = rps.Problem(rectangles=boxes)
        solution = rps.Solver().solve(problem=problem, width_limit = maximum_bed_width, height_limit = maximum_bed_height, show_progress=True, seed=1111, simanneal_minutes=.01)
        
        if solution.floorplan.bounding_box[0] > maximum_bed_width:
            solution_is_good = False
            break
        if solution.floorplan.bounding_box[1] > maximum_bed_height:
            solution_is_good = False
            break

        solution_beds.append(solution)

        # rps.Visualizer().visualize(solution=solution, path="./floorplan_limit.png")


with open("./sample_data_1.json") as s:
    data = json.load(s)

# Convert input format into a dict
all_elements_as_json = data["elements"]
all_elements = {}
for e in all_elements_as_json:
    all_elements[e["id"]] = {"width" : e["width"], "height" : e["height"]}

maximum_bed_width = data["bed"]["width"]
maximum_bed_height = data["bed"]["height"]

print(f"Maximum width {maximum_bed_width}")
print(f"Maximum height {maximum_bed_height}")

with open("./outputFormat.json") as f:
    solution = json.load(f)



check_if_bed_contains_valid_rectangles(maximum_bed_width, maximum_bed_height, solution)