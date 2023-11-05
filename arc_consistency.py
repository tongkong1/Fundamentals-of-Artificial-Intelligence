import util
from sudoku.csp_general import ConstraintSatisfactoryProblem
from sortedcontainers import SortedSet
from operator import eq, neg
from collections import defaultdict, Counter
from external_lib import *


def no_arc_heuristic(csp, queue):
    return queue


def dom_j_up(csp:ConstraintSatisfactoryProblem, queue):
    return SortedSet(queue, key=lambda t: neg(len(csp.curr_domains[t[1]])))


def revise(csp, Xi, Xj, removals, checks=0):
    """Return true if we remove a value."""
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        # if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
        conflict = True
        for y in csp.curr_domains[Xj]:
            if csp.constraints(Xi, x, Xj, y):
                conflict = False
            checks += 1
            if not conflict:
                break
        if conflict:
            csp.prune(Xi, x, removals)
            revised = True
    return revised, checks


def ac1(csp, queue, removals=None, arc_heuristic=None):
    checks = 0
    while True:
        flag = False
        for Xi, Xj in queue:
            revised, checks = revise(csp, Xi, Xj, removals, checks)
            if revised:
                if not csp.curr_domains[Xi]:
                    return False, checks  # CSP is inconsistent
            flag = flag or revised
        if not flag:
            break
    return True, checks


def ac3(csp, queue, removals=None, arc_heuristic=None):
    checks = 0
    if removals is None:
        removals = []
    while queue:
        Xi, Xj = queue.pop()
        revised, checks = revise(csp, Xi, Xj, removals, checks)
        if revised:
            if not csp.curr_domains[Xi]:
                return False, checks  # CSP is inconsistent
            for Xk in csp.neighbors[Xi] - {Xj}:
                queue.add((Xk, Xi))
    return True, checks


def ac4(csp, queue=None, removals=None, arc_heuristic=None):
    checks = 0
    queue.clear()
    S = {}
    counter = {}
    for Xi in csp.variables:
        for Xj in csp.neighbors[Xi]:
            for vik in csp.curr_domains[Xi]:
                counter[(Xi, vik, Xj)] = 0
            for vjm in csp.curr_domains[Xj]:
                S[(Xj, vjm)] = set()

    for Xi in csp.variables:
        for Xj in csp.neighbors[Xi]:
            for vik in csp.curr_domains[Xi]:
                for vjm in csp.curr_domains[Xj]:
                    if csp.constraints(Xi, vik, Xj, vjm):
                        counter[(Xi, vik, Xj)] = counter[(Xi, vik, Xj)] + 1
                        S[(Xj, vjm)].add((Xi, vik))
                if counter[(Xi, vik, Xj)] == 0:
                    queue.add((Xi, vik))
                    csp.prune(Xi, vik, removals)
    while queue:
        Xj, vjm = queue.pop()
        for Xi, vik in S[(Xj, vjm)]:
            if vik in csp.curr_domains[Xi]:
                counter[(Xi, vik, Xj)] = counter[(Xi, vik, Xj)] - 1
                if counter[(Xi, vik, Xj)] == 0:
                    queue.add((Xi, vik))
                    csp.prune(Xi, vik, removals)
    return True, checks
