"""Turn the input into a connected graph, then traverse the graph."""
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def get_board(input):
  lines = input.splitlines()
  list_board = [list(l) for l in lines]

  num_rows = len(list_board)
  num_cols = len(list_board[0])
  start = (0, 1)
  end = (num_rows - 1, num_cols -2)

  dict_board = {
    (i, j): val
    for i, row in enumerate(list_board)
    for j, val in enumerate(row)
  }
  return dict_board, start, end


def move_by_dir(pos, dir):
  return (pos[0] + dir[0], pos[1] + dir[1])


def is_valid_pos(board, pos, forbidden=None):
  if pos not in board:
    return False
  if board[pos] == "#":
    return False
  if forbidden is not None and pos in forbidden:
    return False
  return True


def get_graph_nodes(board, start, end):
  dict_graph_nodes = {start: {}, end: {}}

  # First get all the nodes.
  for pos, symbol in board.items():
    # Check if a position is a junction. If it is, add it to dict_graph.
    if symbol == "#":
      pass
    elif pos == start or pos == end:
      pass
    else:
      list_neighbors = [move_by_dir(pos, dir) for dir in DIRS]
      list_neighbors = [n for n in list_neighbors if n in board and board[n] != "#"]
      if len(list_neighbors) > 2:
        dict_graph_nodes[pos] = {}

  return dict_graph_nodes


def find_nearest_neighbor(board, dict_graph, source, dir):
    """curr_pos is one of the directions that a node can take."""
    curr_pos = move_by_dir(source, dir)
    visited = {curr_pos}
    path_length = 1
    while curr_pos not in list(dict_graph):
        available_pos = [move_by_dir(curr_pos, dir) for dir in DIRS]
        available_pos = [pos for pos in available_pos if is_valid_pos(board, pos, visited)]
        available_pos = [pos for pos in available_pos if pos != source]
        if len(available_pos) != 1:
          raise ValueError('There should only be one option.')
        curr_pos = available_pos[0]
        visited.add(curr_pos)
        path_length += 1

    # Subtract by 1 because we will count each node as 1 as well so this avoids
    # double counting.
    return curr_pos, path_length - 1


def find_all_nearest_neighbors(board, dict_graph, source):
  """Find all nearest neighbor of a source node."""
  available_dirs = [dir for dir in DIRS if is_valid_pos(board, move_by_dir(source, dir))]
  dict_out = {}
  for dir in available_dirs:
    node, length = find_nearest_neighbor(board, dict_graph, source, dir)
    dict_out[node] = length
  return dict_out


def populate_edges(board, dict_graph):
  for node in list(dict_graph):
    dict_graph[node] = find_all_nearest_neighbors(board, dict_graph, node)
  return dict_graph


def get_path_length(dict_graph, path):
  path_length = 0
  for i, node in enumerate(path):
    if i > 0:
      prev_node = path[i - 1]
      path_length += 1
      path_length += dict_graph[prev_node][node]

  return path_length


def solve(filename):
    input = open(filename, encoding="utf-8").read()
    dict_board, start, end = get_board(input)

    dict_graph = get_graph_nodes(dict_board, start, end)
    dict_graph = populate_edges(dict_board, dict_graph)

    # Now we can traverse for longest path.
    queue = [[start]]
    list_path_length = []
    while len(queue) > 0:
        q = queue.pop()
        last_node = q[-1]

        neighbors = list(dict_graph[last_node])
        neighbors = [n for n in neighbors if n not in q]
        for neighbor in neighbors:
            q_copy = [p for p in q]
            q_copy.append(neighbor)
            if neighbor == end:
                list_path_length.append(get_path_length(dict_graph, q_copy))
            else:
                queue.append(q_copy)

    return max(list_path_length)



def mini_test():
    filename = "input-test.txt"
    assert solve(filename) == 154


if __name__ == "__main__":
    mini_test()

    filename = "input.txt"
    total = solve(filename)

    print(total)
