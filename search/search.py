# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import pdb
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    """
    stk = util.Stack()
    start_state = problem.getStartState()
    stk.push(start_state)
    visited, parent, goal_state = {}, {}, ""
    parent[start_state] = (-1, "")
    while stk:
        temp_state = stk.pop()
        if problem.isGoalState(temp_state):
            goal_state = temp_state
            break
        if visited.get(temp_state, False) == True: continue
        visited[temp_state] = True
        successors = problem.getSuccessors(temp_state)
        for state, action, reward in successors:
            if visited.get(state, False) == False:
                stk.push(state)
                parent[state] = (temp_state, action)
    actions = []
    while True:
        temp, action = parent.get(goal_state)
        if action == '': break
        actions.append(action)
        goal_state = temp
    return actions[::-1]

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    q = util.Queue()
    closed = set()
    start = (problem.getStartState(), 0, [])
    q.push(start)
    while not q.isEmpty():
        (node, cost, path) = q.pop()
        if problem.isGoalState(node): 
            return path
        if not node in closed:
            closed.add(node)
            for child_node, child_action, child_cost in problem.getSuccessors(node):
                new_cost = cost + child_cost
                new_path = path + [child_action]
                new_state = (child_node, new_cost, new_path)
                q.push(new_state)
    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    q = util.PriorityQueue()
    distances, INF = {}, int(10e18)
    start_state = problem.getStartState()
    distances[start_state] = 0
    q.push(start_state, distances[start_state])
    visited, parent, goal_state = {}, {}, ""
    parent[start_state] = (-1, "")
    while not q.isEmpty():
        temp_state = q.pop()
        if problem.isGoalState(temp_state):
            goal_state = temp_state
            break
        if visited.get(temp_state, False) == True: continue
        visited[temp_state] = True
        successors = problem.getSuccessors(temp_state)
        for state, action, reward in successors:
            if visited.get(state, False) == True: continue
            if distances.get(temp_state) + reward < distances.get(state, INF):
                distances[state] = distances[temp_state] + reward
                q.push(state, distances[state])
                parent[state] = (temp_state, action)
    actions = []
    while True:
        temp, action = parent.get(goal_state)
        if action == '': break
        actions.append(action)
        goal_state = temp
    return actions[::-1]
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    q = util.PriorityQueue()
    distances, INF = {}, int(10e18)
    start_state = problem.getStartState()
    g_scores, f_scores = {}, {}
    g_scores[start_state], f_scores[start_state] = 0, heuristic(start_state, problem)
    q.push(start_state, f_scores[start_state])
    visited, parent, goal_state = {}, {}, ""
    parent[start_state] = (-1, "")
    while not q.isEmpty():
        temp_state = q.pop()
        if problem.isGoalState(temp_state):
            goal_state = temp_state
            break
        if visited.get(temp_state, False) == True: continue
        visited[temp_state] = True
        successors = problem.getSuccessors(temp_state)
        for state, action, reward in successors:
            if visited.get(state, False) == True: continue
            temp_g_score = g_scores[temp_state] + reward
            if temp_g_score < g_scores.get(state, INF):
                g_scores[state] = temp_g_score
                f_scores[state] = g_scores[state] + heuristic(state, problem)
                q.push(state, f_scores[state])
                parent[state] = (temp_state, action)
    actions = []
    while True:
        temp, action = parent.get(goal_state)
        if action == '': break
        actions.append(action)
        goal_state = temp
    return actions[::-1]
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
