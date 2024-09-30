from minimax import Game,GameState,Board,random_player,strategic_player,minimax_heuristic_search

class Isolation(Game):
    def __init__(self,width=8,height=8,players = ("X","O"),to_move="X"):
        self.players = players
        player_squares = {players[0]:(1,1),players[1]:(width,height)}
        board = IsolationBoard(width,height)
        for player,square in player_squares.items():
            board[square] = player
        self.initial = IsolationState(board = board,player_squares = player_squares,to_move=to_move)

    def moves(self,state):
        return state.open_moves(state.to_move)
    
    def transition(self,state,move):
        if move not in self.moves(state):
            return state
        player = state.to_move
        board = state.board.new()
        board.update({move:player,state.player_squares[player]:"*"})
        player_squares = state.player_squares.copy()
        player_squares.update({player:move})
        to_move = self.opponent(player)
        return IsolationState(board=board,player_squares=player_squares,to_move=to_move)
    
    def utility(self,state,player):
        if player == state.to_move:
            return -1
        else:
            return 1


class IsolationState(GameState):
    def __init__(self,board,player_squares,to_move):
        self.board=board
        self.player_squares = player_squares
        self.to_move = to_move
    
    def open_moves(self,player):
        return self.board.open_squares(self.player_squares[player])
    
class IsolationBoard(Board):
    def open_squares(self,squares):
        open_squares = []
        for delta in ((0,1),(1,0),(1,1),(1,-1)):
            (delta_x,delta_y) = delta
            x,y = squares
            x,y = x +delta_x,y+delta_y
            if self.in_board((x,y)) and not self.get((x,y)):
                open_squares.append((x,y))
            x,y = squares
            x,y=x-delta_x,y-delta_y
            if self.in_board((x,y)) and not self.get((x,y)):
                open_squares.append((x,y))
        return open_squares
    
    def in_board(self,square):
        x,y = square
        return (x >= 1 and x <= self.width and y >= 1 and y <= self.height)


def center(game, state, player):
    square = state.player_squares[player]
    board = state.board
    center_x, center_y = ((board.width + 1) / 2), ((board.height + 1) / 2)
    return -(abs(square[0] - center_x)) + abs((square[1] - center_y))

def open_eva(game,state,player):
    if player == game.players[0]:
        v=1
    else:
        v=-1
    board = state.board
    a = len(state.open_moves(player))
    return v*a

mixed_state = True
def mixed(game,state,player):
    if len(state.board.blank_square()) > len(state.board.squares) * 0.7:
        return center(game, state, player)
    return open_eva(game, state, player)


if __name__ =="__main__":
    open_p = strategic_player(minimax_heuristic_search,depth_limit=4,eval_fn=open_eva)
    center_p = strategic_player(minimax_heuristic_search,depth_limit=4,eval_fn=center)
    mix_p = strategic_player(minimax_heuristic_search,depth_limit=4,eval_fn=mixed)
    iso = Isolation(players=("X","O"),to_move="X")
    end = iso.play_game(dict(X=mix_p,O=random_player),verbose=True)
    print(iso.utility(end,"X"))
    #iso.show_process(0.15)