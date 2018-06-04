#! /usr/bin/env python3.6

from os import listdir
from os.path import isfile, join
import argparse
import operator
import re

#########################
#     Main-Routine      #
#########################
def main():
    (directory, outfile) = ArgumentParser()
    onlyfiles = [join(directory, f) for f in listdir(directory) if isfile(join(directory, f))]
    file_dict = {}

    for f in onlyfiles:
        f_match = re.match(r".*\_(\d+)\_.*", f).groups()
        file_dict[f] = f_match[0]

    sorted_file_dict = sorted(file_dict.items(), key=operator.itemgetter(1))

    with open('{x}'.format(x = outfile), 'w') as out_file:
        for x in sorted_file_dict:
            out_file.write("{a} , {b}\n".format(a = x[0], b = x[1]))

#########################
#     Sub-Routine       #
#########################
def ArgumentParser():
    directory             = ""

    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", "-dir", help="Sorting and listing all the files under the specified directory")
    parser.add_argument("--outfile", "-out", help="Specify the output file name.")

    args = parser.parse_args()
    if args.directory:
        directory = args.directory

    if args.outfile:
        outfile = args.outfile

    return (directory, outfile)

#---------------Execution---------------#
if __name__ == '__main__':
    main()
