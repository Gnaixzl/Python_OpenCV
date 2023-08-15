import json
import numpy as np
import time

image_json_path = 'data/0620_output/detect_output_0620.json'
cad_json_path = 'data/0620_output/repair_output_front_0620.json'
new_json_path = 'data/0620_output/1.json'


def read_json(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)
        f.close()
    return json_data


def get_number_pt(json_data, x, y, z=None):
    coordinate = 1
    if not z:
        for info_dict in json_data['PCBNUM_FRONT']:
            if info_dict['x'] == x and info_dict['y'] == y:
                coordinate = info_dict['pt']
    for info_dict in json_data['CONNECTPAD_FRONT']:
        # print('x:',x,'y:',y,'z:',z)
        # print(info_dict['x'],info_dict['y'],info_dict['z'])
        if info_dict['x'] == x and info_dict['y'] == y and info_dict['z'] == z:
            coordinate = info_dict['pt']
    return coordinate


def compute_offset(image_json_data, cad_json_data, x, y, z=None):
    """
    param image json:
    param cad json:
    param pad number: pad的位置信息，第几行第几列die中的哪一个pad
    return:
    """
    img_coordinate = get_number_pt(image_json_data, x, y, z)
    cad_coordinate = get_number_pt(cad_json_data, x, y, z)
    offset_x = img_coordinate[0] - cad_coordinate[0]
    offset_y = img_coordinate[1] - cad_coordinate[1]
    return offset_x, offset_y


def align_cad(offset_x, offset_y, cad_json, new_json):
    """"
    param offset_x:
    param offset_y:
    param cad_json:
    return:
    [194, 55944]
    """
    file_in = open(cad_json, "r")
    file_out = open(new_json, "w")
    json_data = json.load(file_in)
    for info_dict in json_data['PCBNUM_FRONT']:
        info_dict['pt'] = [x + y for x, y in zip(info_dict['pt'], [offset_x, offset_y])]
        for i, outline in enumerate(info_dict['outline']):
            info_dict['outline'][i] = [x + y for x, y in zip(info_dict['outline'][i], [offset_x, offset_y])]
    for info_dict in json_data['CONNECTPAD_FRONT']:
        info_dict['pt'] = [x + y for x, y in zip(info_dict['pt'], [offset_x, offset_y])]
        for i, outline in enumerate(info_dict['outline']):
            info_dict['outline'][i] = [x + y for x, y in zip(info_dict['outline'][i], [offset_x, offset_y])]
    file_out.write(json.dumps(json_data))
    file_in.close()
    file_out.close()


def find_index_max(image_json):
    pad_x = []
    pad_y = []
    pad_z = []
    file_in = open(image_json, "r")
    json_data = json.load(file_in)
    for info_dict in json_data['CONNECTPAD_FRONT']:
        pad_x.append(info_dict['x'])
        pad_y.append(info_dict['y'])
        pad_z.append(info_dict['z'])
    pad_x_max = set(np.array(pad_x))
    pad_y_max = set(np.array(pad_y))
    pad_z_max = set(np.array(pad_z))
    return pad_x_max, pad_y_max, pad_z_max


def output_result(image_json, new_cad_json):
    """
    param image_json:
    param new_cad json:
    return:
    """
    image_data = read_json(image_json)
    new_data = read_json(new_cad_json)
    file = open(new_cad_json, "w+")
    pad_x_max, pad_y_max, pad_z_max = find_index_max(image_json)
    for x in range(pad_x_max + 1):
        for y in range(pad_y_max + 1):
            for z in range(pad_z_max + 1):
                offset_x, offset_y = compute_offset(image_data, new_data, x, y, z)
                print(offset_x, offset_y)
                for info_dict in new_data['CONNECTPAD_FRONT']:
                    if info_dict['x'] == x and info_dict['y'] == y and info_dict['z'] == z:
                        info_dict['offset_x'] = offset_x
                        info_dict['offset_y'] = offset_y
    file.write(json.dumps(new_data))
    file.close()


# print(get_number_pt(read_json(path),0,0,0))
# print(compute_offset(read_json(path),read_json(new_path),0,0))
# align_cad(1,1,path,new_path)
# output_result(path, new_path)

# print(find_index_max(new_path))


image_json_data = read_json(image_json_path)
cad_json_data = read_json(cad_json_path)
offset_x, offset_y = compute_offset(image_json_data, cad_json_data, 2,5,    5)
print("offset = ", offset_x, offset_y)

align_cad(offset_x, offset_y, cad_json_path, new_json_path)


