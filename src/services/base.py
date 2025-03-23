from abc import ABC
from dataclasses import dataclass

from repositories.base import AbstractRepository


@dataclass
class AbstractService(ABC):
    repository: AbstractRepository
