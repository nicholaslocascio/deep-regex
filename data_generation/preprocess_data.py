import re
import random
import sys
import argparse
import os
import csv

def main(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--data_dir', 
        help='Data directory', required=True, type=str)
    parser.add_argument('--targ_separate', 
        help='Data directory', type=int)
    args = parser.parse_args(arguments)
    data_dir = args.data_dir
    print(args)
    targ_separate = True
    if args.targ_separate == 0:
        targ_separate = False
    process_data(data_dir, targ_separate)
    output_kushman_format(data_dir)

def process_data(data_dir , targ_separate=True):
    print(targ_separate)
    desc_lines, regex_lines = process_tokens(data_dir, targ_separate)
    split_data_and_save(desc_lines, regex_lines, data_dir, ratio=0.65)

def process_tokens(data_dir, targ_separate=True):
    desc_file_name = "{}/{}".format(data_dir, "src")
    regex_file_name = "{}/{}".format(data_dir, "targ")

    if targ_separate:
        regex_lines = [" ".join(line.rstrip('\n')) for line in open('{}{}'.format(regex_file_name, '.txt'))]
    else:
        regex_lines = ["".join(line.rstrip('\n')) for line in open('{}{}'.format(regex_file_name, '.txt'))]

    desc_lines = [" " + line.rstrip('\n') + " " for line in open('{}{}'.format(desc_file_name, '.txt'))]

    desc_lines = [line.lower() for line in desc_lines]
    punc = [',', '.', '!', ';']
    for p in punc:
        p_space = '{} '.format(p)
        p_2_space = ' {} '.format(p)
        desc_lines = [line.replace(p_space, p) for line in desc_lines]
        desc_lines = [line.replace(p, p_2_space) for line in desc_lines]


    num_pairs = [(' one ', ' 1 '), (' two ', ' 2 '), (' three ', ' 3 '), (' four ', ' 4 '),
    (' five ', '5'), (' six ', '6'), (' seven ', ' 7 '), (' eight ', ' 8 '), (' nine ', ' 9 '), (' ten ', ' 10 ')]
    for pair in num_pairs:
        desc_lines = [line.replace(pair[0], pair[1]) for line in desc_lines]

    single_quot_regex = re.compile("((?<=\s)'([^']+)'(?=\s))")
    desc_lines = [re.sub(single_quot_regex, r'"\2"', line) for line in desc_lines]

    num_lines = len(regex_lines)
    reps_words = ["dog", "truck", "ring", "lake"]
    reps_tags = ["<M0>", "<M1>", "<M2>", "<M3>"]

    new_regex_lines = ["" for i in range(len(regex_lines))]
    new_desc_lines = ["" for i in range(len(desc_lines))]
    cool = False
    for l_i in range(num_lines):
        desc_line = desc_lines[l_i]
        old_desc = desc_line
        temp_desc_line = ''.join([c for c in desc_line])
        words_replaced = []
        for j in range(4):
            double_quot = re.compile('.*\s"([^"]*)"\s.*')
            double_quot_out = double_quot.match(temp_desc_line)
            if double_quot_out:
                word = double_quot_out.groups()[-1]
                words_replaced.insert(0, word)
                print(words_replaced)
                temp_desc_line = temp_desc_line.replace('"{}"'.format(word), reps_tags[j])

        for j in range(len(words_replaced)):
            desc_line = desc_line.replace('"{}"'.format(words_replaced[j]), reps_tags[j])

        new_desc_lines[l_i] = desc_line
        regex_line = regex_lines[l_i]
        print(regex_line)



        # regex_line = regex_line.replace(" ".join('[AEIOUaeiou]'), "<VOW>")
        # regex_line = regex_line.replace(" ".join('[aeiouAEIOU]'), "<VOW>")
        # regex_line = regex_line.replace(" ".join('[0-9]'), "<NUM>")
        # regex_line = regex_line.replace(" ".join('[A-Za-z]'), "<LET>")
        # regex_line = regex_line.replace(" ".join('[A-Z]'), "<CAP>")
        # regex_line = regex_line.replace(" ".join('[a-z]'), "<LOW>")

        regex_line = regex_line.replace(" ".join('AEIOUaeiou'), "<VOW>")
        regex_line = regex_line.replace(" ".join('aeiouAEIOU'), "<VOW>")
        regex_line = regex_line.replace(" ".join('0-9'), "<NUM>")
        regex_line = regex_line.replace(" ".join('A-Za-z'), "<LET>")
        regex_line = regex_line.replace(" ".join('A-Z'), "<CAP>")
        regex_line = regex_line.replace(" ".join('a-z'), "<LOW>")

        for i in range(len(words_replaced)):
            match = re.compile(re.escape(" ".join(words_replaced[i])), re.IGNORECASE)
            print(match)
            print(match.sub(" ".join(reps_tags[i]), regex_line))
            regex_line = match.sub(reps_tags[i], regex_line)

        for r_i in range(len(reps_words)):
            r_word = reps_words[r_i]
            regex_line = regex_line.replace(" ".join(r_word), reps_tags[r_i])

        new_regex_lines[l_i] = regex_line


    new_desc_lines = [line.strip(" ") for line in new_desc_lines]
    new_regex_lines = [line.strip(" ") for line in new_regex_lines]
    return new_desc_lines, new_regex_lines

def split_data_and_save(desc_lines, regex_lines, data_dir, ratio=0.65):
    regex_lines = [line.rstrip('\n') for line in regex_lines]
    # desc_lines = [line.rstrip('\n') + " <HALF> " + line.rstrip('\n') for line in desc_lines]
    desc_lines = [line.rstrip('\n') for line in desc_lines]

    zipped = zip(regex_lines, desc_lines)
    random.seed(0)
    random.shuffle(zipped)
    regex_lines_shuffled, desc_lines_shuffled = zip(*zipped)

    regex_train, regex_val, regex_test = split_train_test_val(regex_lines_shuffled, ratio)
    desc_train, desc_val, desc_test = split_train_test_val(desc_lines_shuffled, ratio)

    with open('{}{}{}.txt'.format(data_dir, "/", "src-train"), "w") as out_file:
        out_file.write("\n".join(desc_train))

    with open('{}{}{}.txt'.format(data_dir, "/", "src-val"), "w") as out_file:
        out_file.write("\n".join(desc_val))

    with open('{}{}{}.txt'.format(data_dir, "/", "src-test"), "w") as out_file:
        out_file.write("\n".join(desc_test))

    with open('{}{}{}.txt'.format(data_dir, "/", "targ-train"), "w") as out_file:
        out_file.write("\n".join(regex_train))

    with open('{}{}{}.txt'.format(data_dir, "/", "targ-val"), "w") as out_file:
        out_file.write("\n".join(regex_val))

    with open('{}{}{}.txt'.format(data_dir, "/", "targ-test"), "w") as out_file:
        out_file.write("\n".join(regex_test))

    print("Done!")


def split_train_test_val(ar, ratio):
    train_set = ar[:int(len(ar)*ratio)]
    not_train_set = ar[int(len(ar)*ratio):]
    val_set = not_train_set[int(len(not_train_set)*(5.0/7.0)):]
    test_set = not_train_set[:int(len(not_train_set)*(5.0/7.0))]

    return train_set, val_set, test_set

def output_kushman_format(data_dir):
    desc_lines = [line.rstrip('\n') for line in open('{}/{}'.format(data_dir, 'src.txt'))]
    regex_lines = [line.rstrip('\n') for line in open('{}/{}'.format(data_dir, 'targ.txt'))]
    # desc_lines = [line.replace('"', '""') for line in desc_lines]

    csv_lines = ['"{}","{}","{}","p","p","p","p","p","n","n","n","n","n"'.format(str(i+1), desc_lines[i], regex_lines[i]) for i in range(len(regex_lines))]
    with open('{}/{}'.format(data_dir, "data_kushman_format.csv"), "w") as out_file:
        out_file.write("\n".join(csv_lines))


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
