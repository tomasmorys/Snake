rozmer_hriste_x = 5
rozmer_hriste_y = 5
snake = [(0, 3),(0, 4), (0, 0)]
#snake = [(3, 0),(4, 0), (0, 0)]  #  5
def direction_(a, b):
    if a == 'tail' or a == 'head': return a
    x1, y1 = a
    x2, y2 = b
    if x1 == x2 - 1: return 'left'
    elif x1 == x2 + 1: return 'right'
    elif y1 == y2 - 1: return 'bottom'
    elif y1 == y2 + 1: return 'top'
    
    # x pro kam při pohybu mimo hřiště
    elif x1 + rozmer_hriste_x - 1 == x2: return 'right2'
    # x odkud při pohybu mimo hřiště
    elif x1 == x2 + rozmer_hriste_x - 1: return 'left2'

    # y pro kam při pohybu mimo hřiště
    elif y1 + rozmer_hriste_y - 1 == y2: return 'top2'
    # y odkud při pohybu mimo hřiště
    elif y1 == y2 + rozmer_hriste_y - 1: return 'bottom2'
        
    return 'error'

for a, b, c in zip(['tail'] + snake, snake, snake[1:] + ['head']):
    x, y = b
    u = direction_(a, b)
    v = direction_(c, b)
    print(x, y, u, v)
