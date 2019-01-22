from abc import ABC, abstractmethod

class Node(ABC):
    ins, outs = [], []

    def __init__(ins, outs):
        self.ins = ins
        self.outs = outs

class Resistor(Node):

    def __init__()
