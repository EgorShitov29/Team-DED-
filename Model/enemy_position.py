from typing import List, Tuple

def bbox_centers(
    bboxes: List[Tuple[int, int, int, int]]
) -> List[Tuple[int, int]]:
    """
    Преобразует список bbox (x1, y1, x2, y2) в список центров (cx, cy).
    """
    centers = []
    for x1, y1, x2, y2 in bboxes:
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        centers.append((cx, cy))
    return centers
