import os
import numpy as np
import orjson
import cv2
import math

def sort_points_clockwise(points):
    cent = (
        sum([p[0] for p in points]) / len(points),
        sum([p[1] for p in points]) / len(points))
    points.sort(key=lambda p: math.atan2(p[1] - cent[1], p[0] - cent[0]))
    return points

cad_path = "data/HT1-0627/HT-0420-1/front.json"
output_path = "data/output_front.json"
json_file = open(cad_path, "r").read()
wafer_json = orjson.loads(json_file)
pcb_num = wafer_json["PCBNUM_FRONT"]
pcb_num2 = wafer_json["CONNECTPAD_FRONT"]

# mm2pixel_ratio = 389
x_scale = 400
y_scale = 400
for pcb in pcb_num:
    # print(">>>>> draw no: ", pcb["no"])
    outline = pcb["outline"]
    p_outline = np.asarray(np.around(np.array(outline) * [x_scale, y_scale], 0), dtype=np.intp)

    # p_outline = np.asarray(outline)
    # # print("1111111 = ", p_outline[:, 1])
    # p_outline[:, 0] *= x_scale
    # p_outline[:, 1] *= y_scale
    # p_outline = np.around(p_outline, 0)
    # # print("2222222 = ", p_outline[:, 1])

    p_outline = p_outline.tolist()
    p_outline = sort_points_clockwise(p_outline)
    pcb_idx = wafer_json["PCBNUM_FRONT"].index(pcb)
    wafer_json["PCBNUM_FRONT"][pcb_idx]["outline"] = p_outline

for pcb in pcb_num2:
    # print(">>>>> draw no: ", pcb["no"])
    outline = pcb["outline"]
    p_outline = np.asarray(np.around(np.array(outline) * [x_scale, y_scale], 0), dtype=np.intp)

    # p_outline = np.asarray(outline)
    # p_outline[:, 0] *= x_scale
    # p_outline[:, 1] *= y_scale
    # p_outline = np.around(p_outline, 0)

    p_outline = p_outline.tolist()
    p_outline = sort_points_clockwise(p_outline)
    pcb_idx = wafer_json["CONNECTPAD_FRONT"].index(pcb)
    wafer_json["CONNECTPAD_FRONT"][pcb_idx]["outline"] = p_outline

json_str = orjson.dumps(wafer_json)
with open(output_path, 'w') as f:
    f.write(json_str.decode('utf-8'))
# print("write image...")
# cv2.imwrite("output_json.png", background)
