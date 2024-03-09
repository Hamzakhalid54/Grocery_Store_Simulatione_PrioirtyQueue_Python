"""Assignment 1 - Container (Task 3)

CSC148 Winter 2024
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory are
Copyright (c) Jonathan Calver, Diane Horton, Sophia Huynh, Joonho Kim and
Jacqueline Smith.

Module Description:

This file contains the classes representing the Container and Priority Queue
abstract data types.
"""

from __future__ import annotations
from typing import Any, List, Tuple


class Container:
    """A container that holds objects. This is an abstract class."""

    def add(self, item: Any) -> None:
        """Function for add"""
        raise NotImplementedError

    def remove(self) -> Any:
        """Function for remove"""
        raise NotImplementedError

    def is_empty(self) -> bool:
        """Function for checking empty"""
        raise NotImplementedError


class PriorityQueue(Container):
    "Class for PriorityQueue"

    def __init__(self) -> None:
        super().__init__()
        self._items: List[Tuple[int, Any]] = []

    def add(self, item: Any, priority: int = 0) -> None:
        new_item = (priority, item)
        inserted = False
        for i in range(len(self._items)):
            # if new item's priority higher than current item's priority
            if priority < self._items[i][0]:
                self._items.insert(i, new_item)
                inserted = True
                break
        if not inserted:
            self._items.append(new_item)

    def remove(self) -> Any:
        if self.is_empty():
            raise Exception("PriorityQueue is empty")
        return self._items.pop(0)[1]

    def is_empty(self) -> bool:
        return len(self._items) == 0


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    check_pyta = True
    if check_pyta:
        import python_ta

        python_ta.check_all(config={
            'allowed-import-modules': ['__future__',
                                       'typing', 'python_ta', 'doctest']
        })
