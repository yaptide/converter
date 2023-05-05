from pathlib import Path
from typing import Union
from converter.shieldhit.parser import DummyParser as SHDummyParser, ShieldhitParser
from converter.topas.parser import TopasParser
from converter.common import Parser
from converter.fluka.parser import FlukaParser


def get_parser_from_str(parser_type: str) -> Parser:
    """Get a converter object based on the provided type."""
    # This is temporary, suggestions on how to do this better appreciated.
    if parser_type.lower() == 'sh_dummy':
        return SHDummyParser()
    if parser_type.lower() == 'shieldhit':
        return ShieldhitParser()
    if parser_type.lower() == 'topas':
        return TopasParser()
    if parser_type.lower() == 'fluka':
        return FlukaParser()

    print(f"Invalid parser type \"{parser_type}\".")
    raise ValueError("Parser type must be either 'sh_dummy', 'shieldhit', 'topas' or 'fluka'.")


def run_parser(parser: Parser, input_data: dict, output_dir: Union[Path, None] = None, silent: bool = True) -> dict:
    """
    Convert the configs and return a dict representation of the config
    files. Can save them in the output_dir directory if specified.
    """
    parser.parse_configs(input_data)

    if not silent:
        for key, value in parser.get_configs_json().items():
            print(f'File {key}:')
            print(value)

    if output_dir:
        if not output_dir.exists():
            output_dir.mkdir(parents=True)
        elif not output_dir.is_dir():
            print(f'Output path {output_dir} is not a directory.')
            raise NotADirectoryError(output_dir)
        parser.save_configs(output_dir)

    return parser.get_configs_json()
