from typing import Callable, Optional
from anytree import RenderTree, NodeMixin, TreeError


def _repr(node, args=None, nameblacklist=None):
    classname = node.__class__.__name__
    args = args or []
    nameblacklist = nameblacklist or []
    for key, value in filter(lambda item: not item[0].startswith("_") and item[0] not in nameblacklist,
                             sorted(node.__dict__.items(),
                                    key=lambda item: item[0])):
        if callable(value):
            args.append("%s=%s" % (key, value.__name__))
        else:
            args.append("%s=%r" % (key, value))
    return "%s(%s)" % (classname, ", ".join(args))


class NodeCore(NodeMixin):
    name: str
    ParentChildNum: int
    __position: list[int]

    def __init__(self, name: str, function: Callable = None, parent: NodeMixin = None, children=None):
        self.name = name

        self.parent = parent

        self.function = function

        if not parent:
            self.position = name

        if children:
            self.children = children

    def get_child_by_name(self, name: str):
        child = self.__get_child_by_name(name)
        if child is None:
            print(f'child with name {name} not found!!')  # TODO:bayad y exception ro ham seda bezane
        return child

    def __get_child_by_name(self, name: str):
        # TODO:bayad hatman bar asas position ham bashe
        for child in self.children:
            if child.name == name:
                return child
            else:
                child_check = child.__get_child_by_name(name)
                if child_check is not None:
                    return child_check
        return None

    def get_child_by_id(self, id_in: int):
        child = self.__get_child_by_id(id_in)
        if child is None:
            print(f'child with id {id_in} not found!!')  # TODO:bayad y exception ro ham seda bezane
        return child

    def __get_child_by_id(self, id_in: int):
        if id_in < len(self.children):
            return self.children[id_in]

        return None

    def __repr__(self):
        args = ["%r" % self.separator.join([""] + [str(node.name) for node in self.path])]
        return _repr(self, args=args, nameblacklist=["name", "function", "ParentChildNum"])

    def render(self):
        print(RenderTree(self))

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, name):
        if name == self.name:
            self.__position = []
        else:
            child = self.get_child_by_name(name)
            if child is not None:
                self.__position = [node.ParentChildNum for node in child.path]

    @position.getter
    def position(self):
        pos = self
        for i in self.__position[1:]:
            pos = pos.children[i]
        return pos

    @NodeMixin.parent.setter
    def parent(self, value):
        if value is not None:
            self.ParentChildNum = len(value.children)
        else:
            self.ParentChildNum = 0
        if value is not None and not isinstance(value, NodeMixin):
            msg = "Parent node %r is not of type 'NodeMixin'." % value
            raise TreeError(msg)
        try:
            parent = self.__parent
        except AttributeError:
            parent = None
        if parent is not value:
            self._NodeMixin__check_loop(value)
            self._NodeMixin__detach(parent)
            self._NodeMixin__attach(value)


class Node(NodeCore):
    position: Optional[list[int]]
    children: tuple[NodeCore]
    parent: Optional[NodeCore]
    name: str

    def __init__(self, name: str, function: Callable = None, parent: NodeCore = None, children: tuple[NodeCore] = None):
        super().__init__(name, function, parent, children)

    def get_child_by_id(self, id_in: int) -> Optional[NodeCore]:
        return NodeCore.get_child_by_id(self, id_in)

    def get_child_by_name(self, name: str) -> Optional[NodeCore]:
        return NodeCore.get_child_by_name(self, name)
