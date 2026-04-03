from dataclasses import dataclass, field
from typing import Generic, Iterator, TypeVar

T = TypeVar("T")


@dataclass
class BaseList(Generic[T]):
    items: list[T] = field(default_factory=list)

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, index: int) -> T:
        return self.items[index]
