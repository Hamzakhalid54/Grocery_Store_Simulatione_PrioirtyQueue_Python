"""Assignment 1 - Grocery Store Models (Task 1)

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

This file contains all the classes necessary to model the relevant entities
in a grocery store.
# """
from __future__ import annotations
from typing import TextIO, List
import json

EXPRESS_LIMIT = 7


class NoAvailableLineError(Exception):
    """No available line for a customer to join."""

    def __str__(self) -> str:
        return 'No line available'


class GroceryStore:
    """A grocery store with multiple checkout lines."""

    def __init__(self, config_file: TextIO) -> None:
        config = json.load(config_file)
        self.regular_lines = [CheckoutLine(config['line_capacity'])
                              for _ in range(config['regular_count'])]
        self.express_lines = [ExpressLine(config['line_capacity'])
                              for _ in range(config['express_count'])]
        self.self_serve_lines = [SelfServeLine(config['line_capacity'])
                                 for _ in range(config['self_serve_count'])]
        self.num_lines = config['regular_count'] + config[
            'express_count'] + config['self_serve_count']

    def enter_line(self, customer: Customer) -> int:
        """Enter Line"""
        lines = self._get_appropriate_lines(customer)
        for i, line in enumerate(lines):
            if line.can_accept(customer):
                line.accept(customer)
                return i
        raise NoAvailableLineError()

    def _get_appropriate_lines(self, customer: Customer) -> List[CheckoutLine]:
        """appropriate line"""
        if customer.num_items() <= EXPRESS_LIMIT:
            return self.express_lines + self.regular_lines \
                + self.self_serve_lines
        else:
            return self.regular_lines \
                + self.self_serve_lines

    def next_checkout_time(self, line_number: int) -> int:
        """chekout line"""

        if line_number < len(self.regular_lines):
            return self.regular_lines[line_number].next_checkout_time()
        elif line_number < len(self.regular_lines) + len(self.express_lines):
            index = line_number - len(self.regular_lines)
            return self.express_lines[index].next_checkout_time()
        else:
            index = line_number - len(self.regular_lines)\
                - len(self.express_lines)
            return self.self_serve_lines[index].next_checkout_time()

    def remove_front_customer(self, line_number: int) -> int:
        """remove customer"""

        if line_number < len(self.regular_lines):
            self.regular_lines[line_number].remove_front_customer()
        elif line_number < len(self.regular_lines) \
                + len(self.express_lines):
            index = line_number - len(self.regular_lines)
            self.express_lines[index].remove_front_customer()
        else:
            index = line_number - len(self.regular_lines) \
                - len(self.express_lines)
            self.self_serve_lines[index].remove_front_customer()
        return len(self._get_line_by_number(line_number))

    def close_line(self, line_number: int) -> List[Customer]:
        """close line"""

        return self._get_line_by_number(line_number).close()

    def first_in_line(self, line_number: int) -> Customer | None:
        """first in line"""

        return self._get_line_by_number(line_number).first_in_line()

    def _get_line_by_number(self, line_number: int) -> CheckoutLine:
        "get_lined_by_customer"
        if line_number < len(self.regular_lines):
            return self.regular_lines[line_number]
        elif line_number < len(self.regular_lines) + len(self.express_lines):
            return self.express_lines[line_number - len(self.regular_lines)]
        else:
            return self.self_serve_lines[line_number
                                         - len(self.regular_lines)
                                         - len(self.express_lines)]


class Customer:
    """A grocery store customer."""

    def __init__(self, name: str, items: List[Item]) -> None:
        self.name = name
        self.arrival_time = None
        self._items = items[:]

    def num_items(self) -> int:
        return len(self._items)

    def item_time(self) -> int:
        return sum(item.time for item in self._items)


class Item:
    """An item to be checked out at a grocery store."""

    def __init__(self, name: str, time: int) -> None:
        self.name = name
        self.time = time


class CheckoutLine:
    """A checkout line in a grocery store."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.is_open = True
        self._queue: List[Customer] = []

    def __len__(self) -> int:
        return len(self._queue)

    def can_accept(self, customer: Customer) -> bool:
        return self.is_open and len(self) < self.capacity

    def accept(self, customer: Customer) -> bool:
        print(f"Adding object of type: {type(customer)}")  # Debug print
        if self.can_accept(customer):
            self._queue.append(customer)
            return True
        return False

    def next_checkout_time(self) -> int:
        if not self._queue:
            raise ValueError("Checkout line is empty.")
        # Ensure self._queue[0] is indeed accessing
        # a Customer's _items list correctly
        return sum(item.time for item in self._queue[0]._items)

    def remove_front_customer(self) -> None:
        if self._queue:
            self._queue.pop(0)

    def close(self) -> List[Customer]:
        self.is_open = False
        removed_customers = self._queue[1:]
        self._queue = self._queue[:1] if self._queue else []
        return removed_customers

    def first_in_line(self) -> Customer | None:
        return self._queue[0] if self._queue else None


class RegularLine(CheckoutLine):
    """A regular checkout line."""


class ExpressLine(CheckoutLine):
    """An express checkout line."""

    def next_checkout_time(self) -> int:
        if not self._queue:
            raise ValueError("Express line is empty.")
        return sum(min(EXPRESS_LIMIT, item.time)
                   for item in self._queue[0]._items)


class SelfServeLine(CheckoutLine):
    """A self-serve checkout line."""


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    check_pyta = True
    if check_pyta:
        import python_ta

        python_ta.check_all(config={
            'allowed-import-modules': ['__future__',
                                       'typing', 'json',
                                       'python_ta', 'doctest'],
            'disable': ['W0613']
        })
