class Position(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y

def multiply(matrix, position):
  new_x = matrix[0][0]*position.x + matrix[0][1]*position.y
  new_y = matrix[1][0]*position.x + matrix[1][1]*position.y
  return Position(new_x, new_y)

# rotations around origin
matrices = [[[1, 0], [0, 1]], [[0, 1],[-1, 0]], [[-1, 0], [0, -1]], [[0, -1], [1, 0]]]

def rotate(position, angle):
  index = int(angle/90)
  return multiply(matrices[index], position)

def flip_parallel(position):
  return Position(position.x, -position.y)

def flip_diagonal(position):
  return Position(position.y, position.x)

def pos_to_num(position):
  return int(3*(position.y+1)+position.x+1)

def num_to_pos(num):
  return Position(num%3-1, int(num/3)-1)

def str_to_bin(bin_str):
  x = 0
  for c in bin_str:
    x = 2*x + int(c)
  return x

def apply_fn(coloring, fn_name, angle=0):
  equiv_coloring = [0 for _ in range(9)]
  for pos, color in enumerate(coloring):
    pos_repr = num_to_pos(pos)
    if fn_name=="rotate":
      new_pos = rotate(pos_repr, angle)
      equiv_coloring[pos_to_num(new_pos)] = color
    elif fn_name=="flip_parallel":
      new_pos = flip_parallel(pos_repr)
    else:
      new_pos = flip_diagonal(pos_repr)
    encode_pos = pos_to_num(new_pos)
    equiv_coloring[encode_pos] = color
  return str_to_bin(equiv_coloring)

def merge_equiv_classes(equiv_classes, new_equiv_class):
  added = False
  for equiv_class in equiv_classes:
    if equiv_class.intersection(new_equiv_class):
      equiv_class = equiv_class.union(new_equiv_class)
      added = True
      break
  if not added:
    equiv_classes.append(new_equiv_class)

def gen_equiv_classes():
  equiv_classes = []
  for i in range(512):
    cursor_equiv_class = set([i])
    coloring = str(bin(i))[2:].rjust(9, "0")
    for angle in [90, 180, 270]:
      cursor_equiv_class.add(apply_fn(coloring, "rotate", angle=angle))
    cursor_equiv_class.add(apply_fn(coloring, "flip_parallel"))
    cursor_equiv_class.add(apply_fn(coloring, "flip_diagonal"))
    merge_equiv_classes(equiv_classes, cursor_equiv_class)
  return equiv_classes

if __name__ == "__main__":
  equiv_classes = gen_equiv_classes()
  print(equiv_classes)
  print(len(equiv_classes))
