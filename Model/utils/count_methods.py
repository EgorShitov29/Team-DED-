import numpy


def get_center_coords(corners: list[list[np.typing.int32, np.typing.int32]]) -> tuple[int, int]:
    """
    Функция вычисляет координаты центра ббокса
    """
    lnx = round(np.sqrt(abs((corners[1][0] - corners[0][0])**2 - (corners[1][1] - corners[0][1])**2))) // 2
    lny = round(np.sqrt(abs((corners[2][0] - corners[1][0])**2 - (corners[2][1] - corners[1][1])**2))) // 2
    center_coords = (corners[0][0] + lnx), (corners[0][1] + lny) 
    return center_coords