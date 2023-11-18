from abc import ABC


class CodeBlock(ABC):
    def __init__(self, name):
        self.name = name
