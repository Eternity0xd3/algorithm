import random
from ProblemImpl import Problem,tree_search
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



if __name__ == '__main__':
    allowed_steps = (2,3,4)
    road = [1]
    for i in range(11):
        road.append(random.choice([0,1]))
    road.append(1)
    leap_fd = Forward(road,allowed_steps)
    result = tree_search(leap_fd)
    display = ["_" if s==1 else "^" for s in road]
    if result:
        for node in result.path():
            copy_road = display.copy()
            copy_road[node.state-1] = "@"
            print(" ".join(copy_road))
    else:
        print("NO!")
