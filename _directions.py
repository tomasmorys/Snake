snake = [(1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (3, 5), (4, 5)]

def direction_(a, b):
    if a == 'tail' or a == 'head': return a
    x1, y1 = a
    x2, y2 = b
    if x1 == x2 - 1: return 'left'
    elif x1 == x2 + 1: return 'right'
    elif y1 == y2 - 1: return 'bottom'
    elif y1 == y2 + 1: return 'top'
    return 'end2'

for a, b, c in zip(['tail'] + snake, snake, snake[1:] + ['head']):
    x, y = b
    u = direction_(a, b)
    v = direction_(c, b)
    print(x, y, u, v)
