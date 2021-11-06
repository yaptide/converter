import sys
import json
import argparse
import os
from api import get_parser_from_str, run_parser


def dir_path(string):
    """Hleper function that helps argparse check if a given string is a valid directory."""
    if os.path.isdir(string):
        return string
    raise NotADirectoryError(string)


def main(args):
    """Function for running parser as a script."""
    arg_parser = argparse.ArgumentParser(
        description='Parse a json file and return input files for a particle simulator.')
    arg_parser.add_argument('script_path', type=argparse.FileType())
    arg_parser.add_argument('input_json', type=argparse.FileType('r'))
    arg_parser.add_argument('output_dir', nargs='?', default=os.path.curdir, type=dir_path)
    arg_parser.add_argument('output_format', nargs='?', default='shieldhit', type=str)
    parsed_args = arg_parser.parse_args(args)

    json_parser = get_parser_from_str(parsed_args.output_format)
    run_parser(json_parser, json.load(parsed_args.input_json), parsed_args.output_dir)


if __name__ == '__main__':
    main(sys.argv)
