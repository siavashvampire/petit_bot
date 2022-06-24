from typing import Callable, Optional

from anytree import RenderTree, NodeMixin
from anytree.node.util import _repr


class NodeCore(NodeMixin):
    name: str

    def __init__(self, name: str, function: Callable = None, parent: NodeMixin = None, children=None):
        self.name = name

        self.parent = parent

        self.function = function

        if children:
            self.children = children

    def get_child_by_name(self, name: str):
        for child in self.children:
            if child.name == name:
                return child
        print(f'child with name {name} not found!!')  # TODO:bayad y exception ro ham seda bezane
        return None

    def get_child_by_id(self, id_in: int):
        if id_in < len(self.children):
            return self.children[id_in]

        print(f'child with id {id_in} not found!!')  # TODO:bayad y exception ro ham seda bezane
        return None

    def __repr__(self):
        args = ["%r" % self.separator.join([""] + [str(node.name) for node in self.path])]
        return _repr(self, args=args, nameblacklist=["name"])

    def render(self):
        print(RenderTree(self))


class Node(NodeCore):
    children: tuple[NodeCore]
    parent: Optional[NodeCore]
    name: str

    def __init__(self, name: str, function: Callable = None, parent: NodeCore = None, children: tuple[NodeCore] = None):
        super().__init__(name, function, parent, children)
        self.name = name

        self.parent = parent

        self.function = function

        if children:
            self.children = children

    def get_child_by_id(self, id_in: int) -> Optional[NodeCore]:
        if id_in < len(self.children):
            return self.children[id_in]

        print(f'child with id {id_in} not found!!')  # TODO:bayad y exception ro ham seda bezane
        return None

    def get_child_by_name(self, name: str) -> Optional[NodeCore]:
        for child in self.children:
            if child.name == name:
                return child
        print(f'child with name {name} not found!!')  # TODO:bayad y exception ro ham seda bezane
        return None
