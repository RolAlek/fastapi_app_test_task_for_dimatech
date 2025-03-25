from abc import ABC
from dataclasses import dataclass


@dataclass
class AbstractCreateDTO(ABC):
    pass


@dataclass
class AbstractUpdateDTO(ABC):
    pass
