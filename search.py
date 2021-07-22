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

from game import Directions
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
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    moves = util.Stack()
    frontier = util.Stack()
    path = util.Stack()
    visited = []

    curr_state = problem.getStartState()
    curr_succ = problem.getSuccessors(curr_state)
    exp = {
        curr_state:curr_succ
    }
    appendSuccessors(frontier,curr_succ)
    while(not frontier.isEmpty() or curr_state not in visited):
        curr_goal = problem.isGoalState(curr_state)

        if curr_goal:
            return moves.list

        if curr_state in exp:
            curr_succ = exp[curr_state]
        else:
            curr_succ =  problem.getSuccessors(curr_state)
            exp[curr_state] = curr_succ

        curr_succ = [succ for succ in curr_succ if succ[0] not in visited]
        
        if len(curr_succ) == 0:
            if curr_state not in visited:
                visited.append(curr_state)
            moves.pop()
            curr_state = path.pop()
        else:
            path.push(curr_state)
            visited.append(curr_state)
            appendSuccessors(frontier,curr_succ)
            node = frontier.pop()
            moves.push(node[1])
            curr_state = node[0]
    return []


def breadthFirstSearch(problem):
    frontier = util.Queue()
    visited = []
    curr_state = problem.getStartState()
    frontier.push((curr_state, []))
    while(not frontier.isEmpty()):
        node = frontier.pop()
        curr_state = node[0]
        moves = node[1]

        if curr_state in visited:
            continue

        visited.append(curr_state)

        if problem.isGoalState(curr_state):
            return moves

        for successor in problem.getSuccessors(curr_state):
            if successor[0] not in visited: 
                frontier.push((successor[0], moves+[successor[1]]))
    return []


def uniformCostSearch(problem):
    frontier = util.PriorityQueue()
    visited = []
    curr_state = problem.getStartState()
    frontier.push((curr_state, [], 0),0)
    while(not frontier.isEmpty()):
        node = frontier.pop()
        curr_state = node[0]
        moves = node[1]
        cost = node[2]

        if curr_state in visited:
            continue

        visited.append(curr_state)

        if problem.isGoalState(curr_state):
            return moves
        for successor in problem.getSuccessors(curr_state):
            if successor[0] not in visited:
                new_cost = cost+successor[2]
                frontier.push((successor[0], moves+[successor[1]], new_cost), new_cost)
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def greedySearch(problem, heuristic=nullHeuristic):
    frontier = util.PriorityQueue()
    visited = []
    curr_state = problem.getStartState()
    frontier.push((curr_state, []), heuristic(curr_state,problem))
    while(not frontier.isEmpty()):
        node = frontier.pop()
        curr_state = node[0]
        moves = node[1]

        if curr_state in visited:
            continue

        visited.append(curr_state)

        if problem.isGoalState(curr_state):
            return moves
        for successor in problem.getSuccessors(curr_state):
            if successor[0] not in visited:
                new_cost = heuristic(successor[0], problem)
                frontier.push((successor[0], moves+[successor[1]]), new_cost)
    return []


def aStarSearch(problem, heuristic=nullHeuristic):
    frontier = util.PriorityQueue()
    visited = []
    curr_state = problem.getStartState()
    frontier.push((curr_state, [], 0), heuristic(curr_state,problem))
    while(not frontier.isEmpty()):
        node = frontier.pop()
        curr_state = node[0]
        moves = node[1]
        cost = node[2]

        if curr_state in visited:
            continue

        visited.append(curr_state)

        if problem.isGoalState(curr_state):
            return moves
        for successor in problem.getSuccessors(curr_state):
            if successor[0] not in visited:
                new_cost = cost+successor[2]
                frontier.push((successor[0], moves+[successor[1]], cost+successor[2]), new_cost+heuristic(successor[0], problem))
    return []

def foodHeuristic(state, problem):
    position, food_grid = state
    goals = food_grid.asList()
    max_ = 0

    for goal in goals:
        dist = aux_bfs(position,problem.walls,goal)
        if dist > max_: max_ = dist

    return max_


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
ucs = uniformCostSearch
gs = greedySearch
astar = aStarSearch

def appendSuccessors(frontier, successors):
    for successor in successors:
        if successor not in frontier.list:
            frontier.push(successor)

def appendEarlyGoal(frontier, successors, problem, moves):
    for successor in successors:
        if successor not in frontier.list:
            if problem.isGoalState(successor[0]):
                print(successor[0])
                moves.push(successor[1])
                print(moves.list)
                return True
            frontier.push(successor)
    return False

def neighbours(position, walls):
    x = position[0]
    y = position[1]
    options = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    neighbours = []
    
    for option in options:
        if not walls[option[0]][option[1]]:
            neighbours.append(option)
    return neighbours

def aux_bfs(position, walls, goal):
    frontier = util.Queue()
    visited = []
    curr_state = position
    frontier.push((curr_state, 0,[]))
    while(not frontier.isEmpty()):
        node = frontier.pop()
        curr_state = node[0]
        cost = node[1]
        path = node[2]

        if curr_state in visited:
            continue

        visited.append(curr_state)

        if curr_state == goal:

            return cost

        for successor in neighbours(curr_state,walls):
            if successor not in visited: 
                frontier.push((successor, cost+1,path+[curr_state]))
    return 0


def aux_travel(position, walls, goals, cutoff):
    frontier = util.Queue()
    curr_state = position
    reached = []
    frontier.push((curr_state, 0,[],[]))
    while(not frontier.isEmpty()):
        node = frontier.pop()
        curr_state = node[0]
        cost = node[1]
        path = node[2]
        reached = node[3]
  
        if path.count(curr_state) >= 4:
            continue

        if curr_state in goals:
            if curr_state not in reached:
                reached = reached + [curr_state]
                
                if len(goals) == len(reached):
                    print(cost,path,reached)
                    return cost

        for successor in neighbours(curr_state,walls):
            if path.count(successor) < 4 and cost < cutoff:
                frontier.push((successor, cost+1,path+[curr_state], reached+[]))
    return 0