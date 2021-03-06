"""
Python version used: 3.8.3
This program extract the longest sequences from the pattern geneated by spmf java code and 
stores in the text file in the same format as the input.
for e.g if the input is
7 10 #SUP: 321
7 10 58 #SUP: 321
7 10 36 #SUP: 323
7 10 36 58 #SUP: 321
7 10 48 #SUP: 324
7 10 48 58 #SUP: 321
7 10 36 48 #SUP: 323
7 10 36 48 58 #SUP: 321
then the output is

7 10 36 48 58 #SUP: 321

Input: a. pattern generated by spmf java code.

Output: longest sequences of the pattern.

How to run: python seq_dict.py <path to pattern file generated by spmf java code>

NOTE: It took close to 4 hours to generate longest sequences for an input file of size 1.2 GB
"""

import os, psutil, sys
import pstats

seq_dict = {}
# class to store information about each sequence.
class sequence:
    def __init__(self, seq, supp):
        self.seq = seq
        self.support = supp
        self.length = len(seq)
        self.set_seq = set(seq)


# checks if the NEW incoming sequence is a subset of already present
# sequence in the dict.
def check_subset(key, seq, supp):
    global seq_dict
    is_add = True

    seq_so_far = seq_dict[key]
    len_seq = len(seq)
    seq_set = set(seq)

    # Iterating in reverse to optimize the execution of the loop since the
    # longest sequneces are at the end.
    for s in seq_so_far[::-1]:
        # when length of seq is less than sequence in the dict.
        if len_seq < s.length:
            if seq_set.issubset(s.set_seq):
                # print(f"len_seq < s.length Subset found: {seq_set=}")
                is_add = False
                break
        # when length of seq is greater than sequence in the dict.
        elif len_seq > s.length:
            if s.set_seq.issubset(seq_set):
                # print(f" len_seq > s.length so removing: {s.set_seq=}")
                # Remove the sequences which are subset of seq
                seq_so_far.remove(s)

    if is_add:
        seq_obj = sequence(seq, supp)
        seq_so_far.append(seq_obj)

    # Update the dict with longest sequences seen so far.
    seq_dict[key] = seq_so_far


# Store the sequences in the dict.
def store_in_dict(seq, supp):
    global seq_dict
    key = seq[0]

    # sequence already present in the dict.
    if key in seq_dict:
        check_subset(key, seq, supp)
    else:
        # This the first sequence with a unique first value.
        seq_obj = sequence(seq, supp)
        seq_dict[key] = [seq_obj]


# seprates sequences and support for each incoming line
# from the input file.
def process_line(line):
    seq, supp = line.split(" #SUP: ")
    seq = list(map(int, seq.split()))
    supp = supp.strip("\n")

    store_in_dict(seq, supp)


def read_file(filename):
    with open(filename, "r+") as FH:
        for line_no, line in enumerate(FH, start=1):
            # Checks memory utilization after every 5 milllion lines of processing.
            if line_no % 5_000_000 == 0:
                print(f"processed {line_no} lines")
                print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 3)
                # break

            process_line(line)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(f"Usage: {sys.argv[0]} " "pattern generated by spmf java code")

    filename = sys.argv[1]
    read_file(filename)

    # Please provide the path to the output file where you would like to
    # store the longest sequences.

    with open("longest_seq_output/ls_out_100_lines.txt", "w+") as FH:

        for key, values in seq_dict.items():
            for val in values:
                seq = " ".join(map(str, val.seq))
                line = f"{seq} #SUP: {val.support}\n"
                FH.write(line)
