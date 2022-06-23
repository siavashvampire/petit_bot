from typing import Callable

from anytree import RenderTree, NodeMixin
from anytree.node.util import _repr


class Node(NodeMixin):
    # children: tuple[Node]
    # parent: Optional[Node]
    name: str

    def __init__(self, name: str, function: Callable = None, parent=None, children=None):
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
