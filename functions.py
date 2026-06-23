def draw_floor(matrix):
    for i in matrix:
        for j in i:
            if isinstance(j, dict):
                pass 
            else:
                j.draw()