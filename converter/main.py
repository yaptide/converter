from pathlib import Path
import sys
import json
import argparse
import os
from converter import api


def dir_path(path : str):
    """Helper function that helps argparse check if a given string is a valid directory."""
    if os.path.isdir(path):
        return path
    raise NotADirectoryError(path)


def convert(output_format: str, json_file: Path, output_dir: Path, silent: bool):
    """Run conversion and save output to output dir."""
    json_parser = api.get_parser_from_str(output_format)
    try:
        input_data = {}
        if not json_file.exists():
            print(f'File {json_file} does not exist.')
            raise FileNotFoundError(json_file)
        with open(json_file, 'r') as file:
            input_data = json.load(file)
        api.run_parser(json_parser, input_data, output_dir, silent=silent)
    except NotADirectoryError as e:
        print(f'Invalid output directory: {e}')
        sys.exit(1)


def main(args=None):
    """Function for running parser as a script."""
    if args is None:
        args = sys.argv[1:]
    arg_parser = argparse.ArgumentParser(description='Parse a json file and return MC simulator input files.')
    arg_parser.add_argument('input_json_file', type=Path)
    arg_parser.add_argument('output_dir', nargs='?', default=Path.cwd(), type=Path)
    arg_parser.add_argument('output_format', nargs='?', default='shieldhit', type=str)
    arg_parser.add_argument('-s', '--silent', action='store_true')
    parsed_args = arg_parser.parse_args(args)

    try:
        convert(parsed_args.output_format, parsed_args.input_json_file, parsed_args.output_dir, parsed_args.silent)
    except FileNotFoundError as e:
        print(f'File {e} does not exist.')
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
