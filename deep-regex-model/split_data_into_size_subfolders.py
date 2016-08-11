import sys
import argparse
import subprocess
import os
import errno
import math

def main(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--data_dir', 
        help='Data directory', required=True, type=str)
    parser.add_argument('-l','--splits', nargs='+', 
        help='List of splits.', required=True)
    parser.add_argument('--targ_num_lines', type=int, 
        help='List of splits.', default=10000)
    args = parser.parse_args(arguments)
    data_dir = args.data_dir
    splits = [int(s) for s in args.splits]
    optimal = args.targ_num_lines
    print(splits)
    make_splits(data_dir, splits, optimal)

def make_splits(data_dir, splits, optimal):
  for split in splits:
    dir_path = '{}/data_{}/'.format(data_dir, split)
    mkdir_p(dir_path)
    process_file('src-train.txt', data_dir, split, optimal=optimal)
    process_file('targ-train.txt', data_dir, split, optimal=optimal)
    process_file_copy('src-val.txt', data_dir, split)
    process_file_copy('targ-val.txt', data_dir, split)
    process_file_copy('src-train.txt', data_dir, split, 'original_')
    process_file_copy('targ-train.txt', data_dir, split, 'original_')

def process_file_copy(fname, dir_path, split, suffix=''):
    new_path = '{}/data_{}/{}{}'.format(dir_path, split, suffix, fname)
    f_path = '{}/{}'.format(dir_path, fname)
    content = ""
    all_lines = []
    with open(f_path) as f:
      all_lines = f.readlines()

    open(new_path, 'w').close()
    with open(new_path, "a") as f:
      for l in all_lines:
        f.write(l)

def process_file(fname, dir_path, split, optimal=10000, percentage=True):
    new_path = '{}/data_{}/{}'.format(dir_path, split, fname)
    f_path = '{}/{}'.format(dir_path, fname)
    content = ""
    all_lines = []
    with open(f_path) as f:
      all_lines = f.readlines()
    with open(f_path) as f:
      content = f.read()
    split_length = -1
    if percentage:
      split_decimal = float(split)/100.0
      split_length = split_decimal * len(all_lines)
    else:
      split_length = split

    split_length = int(split_length)
    lines_to_keep = all_lines[:split_length]
    num_repeats = int(round(float(optimal)/split_length))

    open(new_path, 'w').close()
    with open(new_path, "a") as f:
      for i in range(0, num_repeats):
        for l in lines_to_keep:
          f.write(l)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
