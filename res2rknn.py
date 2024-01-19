import argparse
import logging
import os.path

import numpy as np


def set_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_in',
                        default='/media/manu/data/sdks/sigmastar/Tiramisu_DLS00V010-20220107/ipu/SGS_IPU_SDK_vQ_0.1.0/log/output/unknown_acfree_320_fixed.sim_sgsimg.img_students_lt_320.bmp.txt')
    parser.add_argument('--dir_out', default='/home/manu/tmp')
    return parser.parse_args()


def run(args):
    logging.info(args)
    with open(args.path_in, 'r') as f:
        lines = f.readlines()
    i = 0
    db = dict()
    while i < len(lines):
        if 'Tensor:' in lines[i]:
            logging.info(lines[i])
            tensor_name, _ = lines[i].strip().split()
            logging.info(tensor_name)
            while 'Original shape:' not in lines[i]:
                i += 1
            tensor_shape_str = lines[i].strip().split(':')[-1][1:-1]
            while 'tensor data:' not in lines[i]:
                i += 1
            i += 1
            tensor_data = list()
            while '}' not in lines[i]:
                line_lst = lines[i].strip().split()
                # logging.info(line_lst)
                tensor_data.extend(line_lst)
                i += 1
            i += 1
            db[tensor_name + ';' + tensor_shape_str] = tensor_data
        i += 1
    # logging.info(db)
    for key in db.keys():
        data = np.array(db[key]).astype('float')
        tensor_name = key.split(';')[0]
        path_out = os.path.join(args.dir_out, tensor_name + '.txt')
        # np.save(path_out, data)
        tensor_shape_str = key.split(';')[-1].split()
        c = int(tensor_shape_str[-1])
        wh = int((len(data) / c) ** 0.5)
        logging.info((1, wh, wh, c, tensor_name))
        data = np.transpose(data.reshape((1, wh, wh, c)), (0, 3, 1, 2))
        np.savetxt(path_out, data.flatten(), fmt="%f", delimiter="\n")

def main():
    set_logging()
    args = parse_args()
    run(args)


if __name__ == '__main__':
    main()
