from minimax import Game, GameState, Board, random_player, strategic_player, minimax_search


class TicTacToe(Game):
    def __init__(self, width=3, height=3, k=3, players=("X", "O"), to_move="X"):
        self.k = k
        self.players = players
        self.initial = GameState(board=Board(width, height), to_move=to_move, score=0)

    def moves(self, state):
        return state.board.blank_square()

    def transition(self, state, move):
        if move not in self.moves(state):
            return state
        player = state.to_move
        board = state.board.new()
        board[move] = player
        to_move = self.opponent(player)
        score = 0
        if board.k_in_line(self.k, player, move):
            score = 1 if (player == self.initial.to_move) else -1
        return GameState(board=board, to_move=to_move, score=score)

    def terminal_test(self, state):
        return (not self.moves(state)) or (state.score != 0)

    def utility(self, state, player):
        if player == self.initial.to_move:
            return state.score
        else:
            return -state.score


if __name__ == "__main__":
    minimax_player = strategic_player(minimax_search)
    ttt = TicTacToe(players=("X", "O"), to_move="X")
    end = ttt.play_game(dict(X=random_player, O=minimax_player), verbose=True)
    print(ttt.utility(end, "X"))
