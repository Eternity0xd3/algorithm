import random, time


class Game:
    def __init__(self, initial, players=()):
        self.initial = initial
        self.players = players

    def opponent(self, player):
        return self.players[(self.players.index(player) + 1) % 2]

    def moves(self, player):
        raise NotImplementedError

    def transition(self, state, move):
        raise NotImplementedError

    def terminal_test(self, state):
        return not self.moves(state)

    def utility(self, state, player):
        raise NotImplementedError

    def play_game(self, strategies: dict, verbose=False):
        state = self.initial
        self.process = []
        if verbose:
            print("初始：")
            print(state)
            print()
        while not self.terminal_test(state):
            player = state.to_move
            move = strategies[player](self, state)
            state = self.transition(state, move)
            if verbose:
                print("玩家：", player, "行动：", move)
                print(state)
                self.process.append(state)
                print()
        return state

    def show_process(self, t):
        for i in self.process:
            print("\n\n\n\n\n\n")
            print(i)
            time.sleep(t)


class GameState:
    def __init__(self, board, to_move, score=None):
        self.board = board
        self.to_move = to_move
        self.score = score

    def __repr__(self):
        return self.board.__repr__()


class Board(dict):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.squares = {
            (x, y) for x in range(1, width + 1) for y in range(1, height + 1)
        }

    def blank_square(self):
        return self.squares - set(self)

    def new(self):
        new_board = self.__class__(width=self.width, height=self.height)
        new_board.update(self)
        return new_board

    def k_in_line(self, k, player, move):
        def in_line(move, delta):
            (delta_x, delta_y) = delta
            x, y = move
            n = 0
            while self.get((x, y)) == player:
                n += 1
                x, y = x + delta_x, y + delta_y
            x, y = move
            while self.get((x, y)) == player:
                n += 1
                x, y = x - delta_x, y - delta_y
            n -= 1
            return n >= k

        return any(in_line(move, delta) for delta in ((0, 1), (1, 0), (1, 1), (1, -1)))

    def __repr__(self):
        rows = []
        for y in range(1, self.height + 1):
            row = []
            for x in range(1, self.width + 1):
                row.append(self.get((x, y), "."))
            rows.append(" ".join(row))
        return "\n".join(rows)


def minimax_search(game, state):
    player = state.to_move

    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -float("inf")
        for m in game.moves(state):
            v = max(v, min_value(game.transition(state, m)))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = float("inf")
        for m in game.moves(state):
            v = min(v, max_value(game.transition(state, m)))
        return v

    return max(game.moves(state), key=lambda m: min_value(game.transition(state, m)))


def random_player(game, state):
    if game.moves(state):
        return random.choice(tuple(game.moves(state)))
    else:
        return None


def strategic_player(search_algorithm, *args, **kwargs):
    return lambda game, state: search_algorithm(game, state, *args, **kwargs)


def minimax_heuristic_search(game, state, depth_limit, eval_fn):
    player = state.to_move

    def max_value(state, depth):
        if game.terminal_test(state):
            return game.utility(state, player)
        if depth > depth_limit:
            return eval_fn(game, state, player)
        v = -float("inf")
        for m in game.moves(state):
            v = max(v, min_value(game.transition(state, m), depth + 1))
        return v

    def min_value(state, depth):
        if game.terminal_test(state):
            return game.utility(state, player)
        if depth > depth_limit:
            return eval_fn(game, state, player)
        v = float("inf")
        for m in game.moves(state):
            v = min(v, max_value(game.transition(state, m), depth + 1))
        return v

    return max(game.moves(state), key=lambda m: min_value(game.transition(state, m), 1))
