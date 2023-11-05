from pacman.game import Directions
from pacman.util import raiseNotDefined
import util
from heuristics import nullHeuristic
import external_lib


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):

    # raiseNotDefined()  # DONT FORGET TO COMMENT THIS LINE AFTER YOU IMPLEMENT THIS FUNCTION!!!!!!
    """
        Search the deepest nodes in the search tree first.

        Your search algorithm needs to return a list of actions that reaches the
        goal. Make sure to implement a graph search algorithm.

        To get started, you might want to try some of these simple commands to
        understand the search problem that is being passed in:

        print("Start:", problem.getStartState())
        print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
        print("Start's successors:", problem.getSuccessors(problem.getStartState()))
        """
    "*** YOUR CODE HERE ***"
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    # util.raiseNotDefined()

    path = util.Path([problem.getStartState()], [], 0)
    if problem.isGoalState(problem.getStartState()):
        return []

    fringe = util.Stack()
    fringe.push(path)

    while not fringe.isEmpty():
        current_path = fringe.pop()
        current_loc = current_path.locations[-1]
        if problem.isGoalState(current_loc):
            return current_path.actions
        else:
            successors = problem.getSuccessors(current_loc)
            for successor in successors:
                next_loc = successor[0]
                next_action = successor[1]
                next_cost = successor[2]
                if next_loc not in current_path.locations:
                    locations = current_path.locations[:]
                    locations.append(next_loc)
                    all_actions = current_path.actions[:]
                    all_actions.append(next_action)
                    next_cost = current_path.cost + next_cost
                    path = util.Path(locations, all_actions, next_cost)
                    fringe.push(path)

    return []


def breadthFirstSearch(problem):
    """
    使用广度优先搜索算法解决问题。

    """

    path = util.Path([problem.getStartState()], [], 0)
    if problem.isGoalState(problem.getStartState()):
        return []

    fringe = util.Queue()
    fringe.push(path)

    visited = set()

    while not fringe.isEmpty():
        current_path = fringe.pop()
        current_loc = current_path.locations[-1]
        if problem.isGoalState(current_loc):
            return current_path.actions
        if current_loc not in visited:
            visited.add(current_loc)
            successors = problem.getSuccessors(current_loc)
            for successor in successors:
                next_loc = successor[0]
                next_action = successor[1]
                next_cost = successor[2]
                if next_loc not in visited:
                    locations = current_path.locations[:]
                    locations.append(next_loc)
                    all_actions = current_path.actions[:]
                    all_actions.append(next_action)
                    next_cost = current_path.cost + next_cost
                    path = util.Path(locations, all_actions, next_cost)
                    fringe.push(path)
    return []


def uniformCostSearch(problem):
    """
    使用 UCS 搜索算法解决问题。

    """

    path = util.Path([problem.getStartState()], [], 0)
    if problem.isGoalState(problem.getStartState()):
        return []

    fringe = util.PriorityQueue()
    fringe.push(path, 0)

    visited = set()

    while not fringe.isEmpty():
        current_path = fringe.pop()
        current_loc = current_path.locations[-1]
        if problem.isGoalState(current_loc):
            return current_path.actions
        if current_loc not in visited:
            visited.add(current_loc)
            successors = problem.getSuccessors(current_loc)
            for successor in successors:
                next_loc = successor[0]
                next_action = successor[1]
                next_cost = successor[2]
                if next_loc not in visited:
                    locations = current_path.locations[:]
                    locations.append(next_loc)
                    all_actions = current_path.actions[:]
                    all_actions.append(next_action)
                    next_cost = current_path.cost + next_cost
                    path = util.Path(locations, all_actions, next_cost)
                    fringe.push(path, path.cost)
    return []


def aStarSearch(problem, heuristic):
    """
    使用 A* 搜索算法解决问题。

    """

    path = util.Path([problem.getStartState()], [], 0)
    if problem.isGoalState(problem.getStartState()):
        return []

    fringe = util.PriorityQueue()
    fringe.push(path, heuristic(path, problem))

    visited = set()

    while not fringe.isEmpty():
        current_path = fringe.pop()
        current_loc = current_path.locations[-1]
        if problem.isGoalState(current_loc):
            return current_path.actions
        if current_loc not in visited:
            visited.add(current_loc)
            successors = problem.getSuccessors(current_loc)
            for successor in successors:
                next_loc = successor[0]
                next_action = successor[1]
                next_cost = successor[2]
                if next_loc not in visited:
                    locations = current_path.locations[:]
                    locations.append(next_loc)
                    all_actions = current_path.actions[:]
                    all_actions.append(next_action)
                    next_cost = current_path.cost + next_cost
                    path = util.Path(locations, all_actions, next_cost)
                    priority = next_cost + heuristic(next_loc, problem)
                    fringe.update(path, priority)
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
