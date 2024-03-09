"""Assignment 1 - Tests for class PriorityQueue  (Task 3a)

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory are
Copyright (c) Jonathan Calver, Diane Horton, Sophia Huynh, Joonho Kim and
Jacqueline Smith.

Module Description:
This module will contain tests for class PriorityQueue.
"""
import pytest
from container import PriorityQueue


def test_add_single_item():
    pq = PriorityQueue()
    pq.add('item1', 1)
    assert not pq.is_empty()


def test_remove_single_item():
    pq = PriorityQueue()
    pq.add('item1', 1)
    assert pq.remove() == 'item1'
    assert pq.is_empty()


def test_priority_order():
    pq = PriorityQueue()
    pq.add('item1', 2)
    pq.add('item2', 1)
    assert pq.remove() == 'item2'
    assert pq.remove() == 'item1'


def test_tie_priority_order():
    pq = PriorityQueue()
    pq.add('item1', 1)
    pq.add('item2', 1)
    assert pq.remove() == 'item1'
    assert pq.remove() == 'item2'


def test_remove_from_empty_raises_exception():
    pq = PriorityQueue()
    with pytest.raises(Exception):
        pq.remove()
