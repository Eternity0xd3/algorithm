from ProblemImpl import Problem,tree_search

class River(Problem):
    def __init__(self,states = set()):
        super().__init__(initial=(1,1,1,1),goal=(-1,-1,-1,-1))
        self.forbidden_states = set(states)
    
    def actions(self,state):
        if state in self.forbidden_states:
            return []
        allowed_actions = [(-1,1,1,1)]
        for n in range(1,len(state)):
            if state[n] == state[0]:
                action = tuple(-1 if i in [0,n] else 1 for i in range(4))
                allowed_actions.append(action)
        return allowed_actions

    def transition(self,state,action):
        return tuple(s * a for s,a in zip(state,action))

if __name__ == "__main__":
    forbidden = {(1,1,-1,-1),(1,-1,-1,1),(1,-1,-1,-1),(-1,1,1,1),(-1,1,1,-1),(-1,-1,1,1)}
    river = River(forbidden)
    result = tree_search(river)
    if result:
        for node in result.path():
            print(" ".join(["N" if s==1 else "F" for s in node.state]))
    else:
        print("NO")