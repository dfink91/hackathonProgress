#!/usr/bin/env python
import json
import rectangle_packing_solver as rps

def check_if_bed_contains_valid_rectangles(maximum_bed_width, maximum_bed_height, solution):
    # https://pypi.org/project/rectangle-packing-solver/

    beds = solution["beds"]

    solution_is_good = True
    solution_beds = []
    for candidate_bed in beds:
        boxes = []

        for candidate_element in candidate_bed["elements"]:
            w = candidate_element["width"]
            h = candidate_element["height"]
            boxes.append({"width": w, "height": h, "rotatable": True})
            
        if len(boxes)==1:
            return True

        problem = rps.Problem(rectangles=boxes)

        solution = rps.Solver().solve(problem=problem, width_limit = maximum_bed_width, height_limit = maximum_bed_height, show_progress=True, seed=1111, simanneal_minutes=.001)
        
        if solution.floorplan.bounding_box[0] > maximum_bed_width:
            solution_is_good = False
            break
        if solution.floorplan.bounding_box[1] > maximum_bed_height:
            solution_is_good = False
            break

        solution_beds.append(solution)

        # rps.Visualizer().visualize(solution=solution, path="./floorplan_limit.png")
        
    return solution_is_good

# with open("./sample_data_1.json") as s:
#     data = json.load(s)

# # Convert input format into a dict
# all_elements_as_json = data["elements"]
# all_elements = {}
# for e in all_elements_as_json:
#     all_elements[e["id"]] = {"width" : e["width"], "height" : e["height"]}

# maximum_bed_width = data["bed"]["width"]
# maximum_bed_height = data["bed"]["height"]

# print(f"Maximum width {maximum_bed_width}")
# print(f"Maximum height {maximum_bed_height}")

# with open("./outputFormat.json") as f:
#     solution = json.load(f)



# check_if_bed_contains_valid_rectangles(maximum_bed_width, maximum_bed_height, solution)