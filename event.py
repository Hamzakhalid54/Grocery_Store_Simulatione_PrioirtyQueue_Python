"""Assignment 1 - Grocery Store Events (Task 2)

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

When you are done Task 2, this file should contain all the classes
necessary to model the different kinds of events in the simulation.
"""
from __future__ import annotations

from typing import TextIO, List
from store import GroceryStore, Customer, Item, NoAvailableLineError


class Event:
    """Event Class"""
    line_number: int  # Type annotation for line_number
    customer: Customer
    timestamp: int

    def __init__(self, timestamp: int) -> None:
        self.timestamp = timestamp

    def __eq__(self, other: Event) -> bool:
        return self.timestamp == other.timestamp

    def __lt__(self, other: Event) -> bool:
        return self.timestamp < other.timestamp

    def __le__(self, other: Event) -> bool:
        return self.timestamp <= other.timestamp

    def do(self, store: GroceryStore) -> List[Event]:
        """Do"""
        raise NotImplementedError


class CustomerArrival(Event):
    """CustomerArrival Class"""
    customer: Customer
    line_number: int

    def __init__(self, timestamp: int, customer: Customer) -> None:
        super().__init__(timestamp)
        self.customer = customer
        self.customer.arrival_time = timestamp

    def do(self, store: GroceryStore) -> List[Event]:
        try:
            line_number = store.enter_line(self.customer)
            return [CheckoutStarted(self.timestamp, line_number)]
        except NoAvailableLineError:
            return []


class CheckoutStarted(Event):
    """CustomerStarted Class"""

    def __init__(self, timestamp: int, line_number: int) -> None:
        super().__init__(timestamp)
        self.line_number = line_number

    def do(self, store: GroceryStore) -> List[Event]:
        customer = store.first_in_line(self.line_number)
        if customer:
            return [CheckoutCompleted(self.timestamp
                                      + store.next_checkout_time
                                      (self.line_number), self.line_number,
                                      customer)]
        return []


class CheckoutCompleted(Event):
    """CheckoutCompleted Class"""

    def __init__(self, timestamp: int,
                 line_number: int,
                 customer: Customer) -> None:
        super().__init__(timestamp)
        self.line_number = line_number
        self.customer = customer

    def do(self, store: GroceryStore) -> List[Event]:
        store.remove_front_customer(self.line_number)
        next_customer = store.first_in_line(self.line_number)
        if next_customer:
            return [CheckoutStarted(self.timestamp, self.line_number)]
        return []


class CloseLine(Event):
    """Closeline Class"""

    def __init__(self, timestamp: int, line_number: int) -> None:
        super().__init__(timestamp)
        self.line_number = line_number

    def do(self, store: GroceryStore) -> List[Event]:
        removed_customers = store.close_line(self.line_number)
        events = []
        for customer in removed_customers:
            try:
                new_line = store.enter_line(customer)
                events.append(CheckoutStarted(self.timestamp, new_line))
            except NoAvailableLineError:
                pass
        return events


def create_event_list(event_file: TextIO) -> List[Event]:
    """Create Even Listen Fucntion"""
    events = []
    for line in event_file:
        parts = line.strip().split()
        timestamp = int(parts[0])
        event_type = parts[1]

        if event_type == "Arrive":
            names = parts[2]
            # Example of creating Customer and Item instances from event data
            items = [(parts[i], int(parts[i + 1]))
                     for i in range(3, len(parts), 2)]
            customer_items = [Item(name, time)
                              for name,
                              time in items]  # Ensure this is done correctly
            customer = Customer(names, customer_items)
            events.append(CustomerArrival(timestamp, customer))
        elif event_type == "Close":
            line_number = int(parts[2])
            events.append(CloseLine(timestamp, line_number))
    return events


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    check_pyta = True
    if check_pyta:
        import python_ta

        python_ta.check_all(config={
            'allowed-import-modules': ['__future__', 'typing',
                                       'store1', 'python_ta',
                                       'doctest', 'io']
        })
