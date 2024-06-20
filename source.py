from copy import deepcopy
from queue import PriorityQueue


class StablePriorityQueue:
    def __init__(self):
        self.queue = PriorityQueue()
        self.counter = 0

    def put(self, item, priority):
        self.queue.put((priority, self.counter, item))
        self.counter += 1

    def get(self):
        _, _, item = self.queue.get()
        return item

    def empty(self):
        return self.queue.empty()


class Node:
    def __init__(self, table, parent, cost):
        self.table = table
        self.parent = parent
        self.cost = cost
        self.dir = None
        self.depth = 0


def input_format_transform(input_string):
    return eval(input_string)


def find_location(board, element):
    for i in range(len(board)):
        if element in board[i]:
            location = [i, board[i].index(element)]
            return location
        else:
            continue


def calculate_list_distance(list1, list2):
    list_distance = 0
    for i in range(len(list1)):
        hamming_distance = abs(list1[i] - list2[i])
        list_distance += hamming_distance
    return list_distance


def h_n(board):
    standard_location = {1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1]}
    distance_hn = 0
    for i in range(1, 6):
        current_location = find_location(board, i)
        location_distance = calculate_list_distance(current_location, standard_location[i])
        distance_hn += location_distance
    return distance_hn


def exchange_elements(board, pos1, pos2):
    new_board = deepcopy(board)
    trans = board[pos1[0]][pos1[1]]
    new_board[pos1[0]][pos1[1]] = board[pos2[0]][pos2[1]]
    new_board[pos2[0]][pos2[1]] = trans
    return new_board


def checkflag(closed, new_board):
    for e in closed:
        if e.table == new_board:
            return closed.index(e)
    return False


def a_star_search(init_board, goal_board):
    frontier = StablePriorityQueue()
    closed = []

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    map1 = {(0, -1): 1, (-1, 0): 2, (0, 1): 3, (1, 0): 4}

    start_cost = h_n(init_board) + 0
    start_node = Node(init_board, None, start_cost)
    start_node.dir = 0

    frontier.put(start_node, start_cost)   # cost, dir, count, step, node

    while not frontier.empty():
        current_node = frontier.get()
        closed.append(current_node)

        current_step = current_node.depth
        current_board = current_node.table
        new_step = current_step + 1
        zero_pos = find_location(current_board, 0)

        for dx, dy in directions:
            x, y = zero_pos[0] + dx, zero_pos[1] + dy
            if 0 <= x < len(current_board) and 0 <= y < len(current_board[0]):
                new_board = exchange_elements(current_board, zero_pos, [x, y])
                new_cost = h_n(new_board) + new_step
                new_dir = map1[(dx, dy)]

                if new_board == goal_board:
                    print(new_cost)
                    print(find_path(current_node, standard_board))
                    return

                flag = checkflag(closed, new_board)
                if flag is False:
                    e = find_in_frontier(frontier, new_board)
                    if e is False:
                        new_node = Node(new_board, current_node, new_cost)
                        new_node.dir = new_dir
                        new_node.depth = new_step
                        frontier.put(new_node, new_cost)
                    else:
                        if new_cost < e.cost:
                            new_node = Node(new_board, current_node, new_cost)
                            new_node.dir = new_dir
                            new_node.depth = new_step
                            frontier.put(new_node, new_cost)

    print(-1)
    print(None)
    return


def find_in_frontier(q, board):
    items = list(q.queue.queue)
    items.sort()
    for _, _, item in items:
        if item.table == board:
            return item
    return False


def find_path(node, standard_board):
    path = []
    while node:
        path.append(node.table)
        node = node.parent
    path = path[::-1]
    path.append(standard_board)
    moving = []

    map2 = {(0, -1): "l", (-1, 0): "u", (0, 1): "r", (1, 0): "d"}
    for i in range(len(path)-1):
        j = i+1
        i_x, i_y = find_location(path[i], 0)
        j_x, j_y = find_location(path[j], 0)
        dx, dy = j_x-i_x, j_y-i_y
        moving.append(map2[(dx, dy)])

    moving_str = ''.join(moving)
    return moving_str


if __name__ == "__main__":
    input_board = input()
    board = input_format_transform(input_board)
    standard_board = [[1, 2, 3], [4, 5, 0]]
    a_star_search(board, standard_board)
