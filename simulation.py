"""Assignment 1 - Grocery Store Simulation (Task 4)

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

This file drives a simulation of customers checking out at a grocery store.
"""
from __future__ import annotations

from typing import TextIO
from event import Event, create_event_list, CustomerArrival, CheckoutCompleted
from store import GroceryStore
from container import PriorityQueue


class GroceryStoreSimulation:
    """GroceryStore Class"""
    _events: PriorityQueue
    _store: GroceryStore
    stats: dict[str, int]

    def __init__(self, store_file: TextIO) -> None:
        self._events = PriorityQueue()
        self._store = GroceryStore(store_file)
        self.stats = {'num_customers': 0, 'total_time': 0, 'max_wait': 0}

    def run(self, initial_events: list[Event]) -> None:
        # Reset statistics
        """function for run"""
        self.stats = {'num_customers': 0, 'total_time': 0, 'max_wait': 0}

        # Add initial events to self._events
        for event in initial_events:
            self._events.add(event, event.timestamp)

        # Process events while there are events to process
        while not self._events.is_empty():
            event = self._events.remove()
            new_events = event.do(self._store)

            # Update 'total_time' to the current event's timestamp
            self.stats['total_time'] = event.timestamp

            if isinstance(event, CustomerArrival):
                # Update 'num_customers' for each CustomerArrival event
                self.stats['num_customers'] += 1

                # Update the arrival time for the customer
                event.customer.arrival_time = event.timestamp

            if isinstance(event, CheckoutCompleted):
                customer_wait_time = event.timestamp - event.customer\
                    .arrival_time
                self.stats['max_wait'] = max(self.stats['max_wait'],
                                             customer_wait_time)

            # Add any new events to self._events
            for new_event in new_events:
                self._events.add(new_event, new_event.timestamp)


# We have provided a bit of code to help test your work.
if __name__ == '__main__':
    config_file_name = 'input_files/config_111_10.json'
    with open(config_file_name) as config_file:
        sim = GroceryStoreSimulation(config_file)
        config_file.close()

    # By using "with ... as ...", we get Python to automatically close the
    # file for us at the end of the "with" clause.
    event_file_name = 'input_files/events_mixtures.txt'
    with open(event_file_name) as event_file:
        events = create_event_list(event_file)
    sim.run(events)
    print(sim.stats)

    import doctest

    doctest.testmod()

    check_pyta = True
    if check_pyta:
        import python_ta

        python_ta.check_all(config={
            'allowed-import-modules': ['__future__', 'typing', 'event', 'store',
                                       'container', 'python_ta', 'doctest']})
