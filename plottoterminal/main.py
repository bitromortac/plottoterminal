#!/usr/bin/env python
import sys
import argparse

from plottoterminal.lib import cli


class Parser(object):
    """
    Parses command line arguments.
    """
    def __init__(self):
        # setup the command line parser
        self.parser = argparse.ArgumentParser(
            prog='plottoterminal',
            description='Plot data to the terminal'
        )
        self.parser.add_argument("file", help="file containing xy data")

    def parse_arguments(self):
        return self.parser.parse_args()


def main():
    """
    Main command line interface for plotting files directly from terminal.
    """
    parser = Parser()

    # take arguments from sys.argv
    args = parser.parse_arguments()
    with open(args.file, 'r') as f:
        cli.plot_file(f)


if __name__ == '__main__':
    main()
