from dataclasses import dataclass

from model.nodes import Node


@dataclass
class Edge:
    n1: Node
    n2: Node
    weight: float