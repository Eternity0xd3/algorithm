from Problem import Problem
class Forward(Problem):
    def __init__(self,road=(),allowed_steps=()):
        self.road = road
        self.allowed_steps = allowed_steps
        super().__init__(initial=1,goal=len(self.road))
    
    def actions(self,state):
        if self.road[state-1] == 0:
            return []
        return [s for s in self.allowed_steps if (state+s <= self.goal)]

    def transition(self,state,action):
        return state + action

class Node:
    def __init__(self,state,parent = None,action = None):
        self.state = state
        self.parent = parent
        self.action = action
    
    def expend(self,problem):
        child_nodes = []
        for action in problem.actions(self.state):
            next_state = problem.transition(self.state,action)
            child_nodes.append(Node(next_state,self,action))
        return child_nodes

    def path(self):
        if self.parent is None:
            return [self]
        return self.parent.path() + [self]

def tree_search(problem):
    frontier = [Node(problem.initial)]
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
    return
    