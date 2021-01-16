
def cross(previous_x1, previous_x2, x1, x2) -> bool:
    return (((x1 <= x2) & (previous_x1 >= previous_x2)) | ((x1 >= x2) & (previous_x1 <= previous_x2)))