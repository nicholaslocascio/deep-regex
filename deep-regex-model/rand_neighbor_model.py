import sys
import argparse
import subprocess
import numpy as np
from regexDFAEquals import regex_equiv_from_raw
import random

def main(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--data_dir', help="data_dir", 
                          type=str, required=True)
    parser.add_argument('--alt_eval', help="data_dir", 
                          type=bool, default=False)
    args = parser.parse_args(arguments)

    train_x_lines = [line.rstrip('\n') for line in open("{}/{}".format(args.data_dir, "src-train.txt"))]
    train_y_lines = [line.rstrip('\n') for line in open("{}/{}".format(args.data_dir, "targ-train.txt"))]

    if args.alt_eval:
        eval_x_lines = [line.rstrip('\n') for line in open("{}/{}".format(args.data_dir, "src-test.txt"))]
        eval_y_lines = [line.rstrip('\n') for line in open("{}/{}".format(args.data_dir, "targ-test.txt"))]
    else:
        eval_x_lines = [line.rstrip('\n') for line in open("{}/{}".format(args.data_dir, "src-val.txt"))]
        eval_y_lines = [line.rstrip('\n') for line in open("{}/{}".format(args.data_dir, "targ-val.txt"))]

    do_classify(train_x_lines, train_y_lines, eval_x_lines, eval_y_lines)

def do_classify(train_x, train_y, test_x, test_y):
    train_x_bow, test_x_bow = get_all_bow(train_x, test_x)
    indices = [random.randint(0, len(train_x)-1) for x_bow in test_x_bow]
    exact = 0.0
    dfa_equal = 0.0
    for row_index in range(len(test_x_bow)):
        gold = test_y[row_index]
        pred_index = indices[row_index]
        pred = train_y[pred_index]
        print("PRED: {}".format(pred))
        print("GOLD: {}".format(gold))
        if pred == gold:
            exact += 1.0
            print("string equal")
        if regex_equiv_from_raw(pred, gold):
            dfa_equal += 1.0
            print("dfa equal")
        print("")

    print("{} String-Equal Correct".format(exact/len(test_x_bow)))
    print("{} DFA-Equal Correct".format(dfa_equal/len(test_x_bow)))


def get_all_bow(train_x, test_x):
    bow_word_set = {'<UNK>'}

    for data in [train_x, test_x]:
        for line in data:
            for word in line.split(' '):
                bow_word_set.add(word)

    print(bow_word_set)

    train_all_bow = []
    test_all_bow = []

    for line in train_x:
        bow = get_bow(line, bow_word_set)
        train_all_bow.append(bow)

    for line in test_x:
        bow = get_bow(line, bow_word_set)
        test_all_bow.append(bow)

    return np.array(train_all_bow), np.array(test_all_bow)

def get_bow(line, bow_word_set):
    bow = {word : 0 for word in bow_word_set}

    for word in line.split(' '):
        bow[word] += 1

    return bow.values()

if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))