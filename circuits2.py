from abc import ABC, abstractmethod

class Node(ABC):
    wires_in, wires_out = [], []

    def __init__(wires_in, wires_out)

class Wire:
    resistance = 0

    def __init__(self, nodes=[]):
        self.nodes = nodes

class Resistor(Node):

