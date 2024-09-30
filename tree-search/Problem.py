class Problem:
    """这是一个基类，用于定义搜索问题的基本组成结构，你需要继承这个类,
    并实现具体的'actions', 'transition', 'goal_test' 方法. '__init__'
    方法可能也需要具体的定制, 在定义完具体的问题类后, 你就可以实例化具体的
    问题, 然后将问题实例传入实现了搜索算法的函数，来解决问题.
    """


    def __init__(self, initial, goal=None):
        """这个构造方法制定了搜索问题的初始状态和目标状态, 你可以根据需求
        继承或者覆写自己的构造方法
        """
        self.initial = initial
        self.goal = goal


    def actions(self, state):
        """返回在给定的状态下， 可以采取的动作, 结果一般是一个列表"""
        raise NotImplementedError


    def transition(self, state, action):
        """返回执行给定动作后达到的状态, 动作必须是在允许动作列表中"""
        raise NotImplementedError


    def goal_test(self, state):
        """如果给定的状态是目标状态则返回True, 你可以覆写这方法, 定义自己的目标测试方法"""
        return state == self.goal


class Node:
    """Node 类表示搜索树中的一个节点, 它包含了该节点代表的实际状态, 他有一个指向
    父节点的指针，它还会记录是哪个动作让我们进入这个状态的.
    """
    def __init__(self, state, parent = None, action = None):
        """这个构造方法会创建一个节点, 并记录当前状态, 父节点和采取的动作"""
        self.state = state
        self.parent = parent
        self.action = action


    def expand(self, problem):
        """展开所有可以从当前节点可以到达的节点"""
        child_nodes = []
        # 获取当前状态下可以采取的动作，遍历每个动作
        for action in problem.actions(self.state):
            next_state = problem.transition(self.state, action)#计算出执行动作后到达的状态
            child_nodes.append(Node(next_state, self, action))#实例化对应的节点，添加到子节点列表中
        return child_nodes


    def path(self):
        """返回一个节点列表, 这个列表形成一条从根节点到达该节点的路径.
        如果该节点没有父节点，那么就是父节点"""
        if self.parent is None:
            return [self]#返回该节点本身
        #如果不是父节点，那他的路径就是父节点的路径拼接它本身
        return self.parent.path() + [self]


def tree_search(problem):#接收一个problem实例作为参数
    # 实现树搜索算法
    '''一个节点表示一条路径，所以在前沿列表只需要存储路径的末端节点
    在刚开始的时候，前沿列表只有一个根节点，通过Node类实例化一个根节点,
    根节点的状态是初始状态，没有父节点，没有动作，parent和action都留空
    while 前沿列表不为空
        从前沿列表取出一条路径
        if 该路径抵达了目标状态 then return 该路径
        else 将该路径展开, 并将展开后的路径添加到前沿列表
    return 失败
    '''
    frontier = [Node(problem.initial)]


    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
    return None