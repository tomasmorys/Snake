'''
{# snake = [(1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (3, 5), (4, 5)]

def direction(a, b): if a is None: return 'end' if b is None: return 'end' x1, y1 = a x2, y2 = b if x1 == x2 - 1: return 'left' elif x1 == x2 + 1: return 'right' elif y1 == y2 - 1: return 'bottom' elif y1 == y2 + 1: return 'top' return 'end'

for a, b, c in zip([None] + snake, snake, snake[1:] + [None]): x, y = b u = direction(a, b) v = direction(c, b) print(x, y, u, v) #}

1 2 tail right
2 2 left right
3 2 left top
3 3 bottom top
3 4 bottom top
3 5 bottom right
4 5 left head
'''
coordinates = [(1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (3, 5), (4, 5)]
direction_x = []
direction_y = []

def direction(x, y):
    if x < x2 : return 'right'


for i in range(len(coordinates)-1):
    direction_x.append('tail')
    x, y = coordinates[i]
    x2, y2 = coordinates[i + 1]
    if x < x2:
        direction_x.append('right')
    elif x < x2:
        direction_x.append('left')
    elif x = x2:
        direction_x.append('bottom')
        
    elif y < y2:
        direction.append('')
        

    
    print(x, y)
    
