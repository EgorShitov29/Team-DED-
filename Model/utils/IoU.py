import numpy as np

def iou(box_first: list, box_second: list) -> float:
    xA = max(box_first[0], box_second[0])
    yA = max(box_first[1], box_second[1])
    xB = min(box_first[2], box_second[2])
    yB = min(box_first[3], box_second[3])

    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    boxAArea = (box_first[2] - box_first[0] + 1) * (box_first[3] - box_first[1] + 1)
    boxBArea = (box_second[2] - box_second[0] + 1) * (box_second[3] - box_second[1] + 1)

    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou