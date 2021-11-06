import sys
import json
from api import get_parser_from_str, run_parser


def main(json: dict, output_dir: str = '.', output_format: str = 'shieldhit', **kwargs):
    parser = get_parser_from_str(output_format)
    run_parser(parser, json, output_dir)


if __name__ == '__main__':
    main(json.loads(sys.argv[1]), **dict(arg.split('=') for arg in sys.argv[2:]))
