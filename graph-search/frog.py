from Problem import Problem,graph_search

class Frog(Problem):
    def __init__(self,n=3):
        self.initial = n*'L'+'.'+n*'R'
        self.goal = self.initial[::-1]
    
    def actions(self,state):
        idxs = range(len(state))
        return ({(i,i+1) for i in idxs if state[i:i+2] == 'L.'}|
                {(i,i+2) for i in idxs if state[i:i+3] == 'LR.'}|
                {(i,i+1) for i in idxs if state[i:i+2] == '.R'}|
                {(i,i+2) for i in idxs if state[i:i+3] == '.LR'})
    
    def transition(self,state,action):
        new_state = list(state)
        new_state[action[0]] = state[action[1]]
        new_state[action[1]] = state[action[0]]
        final = ""
        for i in new_state:
            final = final + i
        return final


if __name__ == '__main__':
    frog = Frog()
    result=graph_search(frog)
    if result:
        for node in result.path():
            print(node.state)
    else:
        print("no")