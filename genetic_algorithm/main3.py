from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.factory import get_algorithm, get_crossover, get_mutation, get_sampling
from pymoo.optimize import minimize
from pymoo.core.callback import Callback
from pymoo.core.problem import ElementwiseProblem
import numpy as np
import xml.etree.ElementTree as ET
import networkx as nx
import logging 

np.set_printoptions(linewidth=np.inf)


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


class MyProblem(ElementwiseProblem):
    def __init__(self, graph):
        self.graph = graph
        super().__init__(n_var=2, n_obj=1, n_constr=0, xl=0, xu=10, type_var=int)

    def _evaluate(self, x, out, *args, **kwargs):
        #print(x)
        out["F"] = -np.sum(x)
        #print(out["F"])


class MyCallback(Callback):
    def notify(self, algorithm):
        print(algorithm.pop[0].X)


method = get_algorithm(
    "ga",
    pop_size=10,
    sampling=get_sampling("int_random"),
    crossover=get_crossover("int_sbx", prob=1.0, eta=3.0),
    mutation=get_mutation("int_pm", eta=3.0),
    eliminate_duplicates=True,
    # callback=MyCallback()
)

logging.basicConfig(format="%(message)s", level=1 * 10)
logging.info("Loading XML...")
graph = get_graph("simulated20220218.xml")

logging.info(f"Found {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges.")


res = minimize(MyProblem(graph), method, termination=("n_gen", 40), seed=1, save_history=True)

# print("Best solution found: %s" % res.X)
# print("Function value: %s" % res.F)






