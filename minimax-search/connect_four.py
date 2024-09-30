from minimax import strategic_player,minimax_search,minimax_heuristic_search
from tic_tak_toe import TicTacToe
import random

class ConnectFour(TicTacToe):
    def __init__(self,width=7,height=6,k=4,players=('X','O'),to_move='X'):
        super().__init__(width=width,height=height,k=k,players=players,to_move=to_move)
    
    def moves(self,state):
        return [(x,y) for (x,y) in state.board.blank_square() if y == state.board.height or (x,y+1) in state.board]

def novice_eva(game,state,player):
    return random.choice([float("inf"),-float("inf")])

def improved_eva(game,state,player):
    v=0
    board=state.board
    center_x,center_y = ((board.width+1)/2),((board.height+1)/2)
    for s,p in board.items():
        distance = abs(s[0]-center_x)+abs(s[1] - center_y)
        if p == player:
            v -= distance
        else:
            v += distance
    return v

if __name__ == "__main__":
    np = strategic_player(minimax_heuristic_search,depth_limit=4,eval_fn=novice_eva)
    ip = strategic_player(minimax_heuristic_search,
                          depth_limit=4, eval_fn=improved_eva)
    c4 = ConnectFour(players=('X', 'O'), to_move='X')
    end = c4.play_game(dict(X=np, O=ip), verbose=True)
    print(c4.utility(end, "X"))