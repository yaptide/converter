import sys
import json
import argparse
import os
from converter import api


def dir_path(string):
    """Helper function that helps argparse check if a given string is a valid directory."""
    if os.path.isdir(string):
        return string
    raise NotADirectoryError(string)


def convert(output_format: str, input_json: dict, output_dir: str, silent: bool):
    """Run conversion and save output to output dir."""
    json_parser = api.get_parser_from_str(output_format)
    api.run_parser(json_parser, json.load(input_json), output_dir, silent=silent)


def main(args=None):
    """Function for running parser as a script."""
    if args is None:
        args = sys.argv[1:]
    arg_parser = argparse.ArgumentParser(description='Parse a json file and return MC simulator input files.')
    arg_parser.add_argument('input_json', type=argparse.FileType('r'))
    arg_parser.add_argument('output_dir', nargs='?', default=os.path.curdir, type=dir_path)
    arg_parser.add_argument('output_format', nargs='?', default='shieldhit', type=str)
    arg_parser.add_argument('-s', '--silent', action='store_true')
    parsed_args = arg_parser.parse_args(args)

    convert(parsed_args.output_format, parsed_args.input_json, parsed_args.output_dir, parsed_args.silent)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
