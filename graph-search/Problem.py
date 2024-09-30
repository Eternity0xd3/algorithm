class Problem:
    def __init__(self,initial,goal=None):
        self.initial = initial
        self.goal = goal
    
    def actions(self,state):
        raise NotImplementedError
    def transition(self,state,action):
        raise NotImplementedError
    def goal_test(self,state):
        return state == self.goal
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
    
    def __eq__(self,other):
        return isinstance(other,Node) and self.state == other.state

def graph_search(problem):
    frontier = [Node(problem.initial)]
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        frontier.extend([n for n in node.expend(problem) if n.state not in explored])
    return None