import typing as tp
from abc import ABC, abstractmethod

from data_generator.element import Element
from data_generator import utils


def to_transform(x):

    if isinstance(x, Transformer):
        return x
    elif isinstance(x, list):
        return Compose(x)


class Transformer(ABC):
    @abstractmethod
    def apply(self):
        pass

    def __call__(self, element: Element) -> tp.Iterable[Element]:

        elements = self.apply(element)

        if isinstance(elements, Element):
            elements = [elements]

        return elements

    def __or__(self, other):
        other = to_transform(other)

        return Compose([self, other])


class Compose(Transformer):
    def __init__(self, transformers: tp.List[Transformer]):

        self.transforms = transforms

    def apply(self, element: Element) -> Element:
        elements = [element]

        for transformer in self.transformers:
            elements = utils.flat_map(transformer, elements)

        return elements

