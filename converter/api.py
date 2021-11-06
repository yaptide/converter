from converter import shieldhit
from converter import topas
from converter.common import Parser


def get_parser_from_str(parser_type: str) -> Parser:
    """Get a converter object based on the provided type."""
    # This is temporary, suggestions on how to do this better appreciated.
    if parser_type.lower() == 'dummy':
        return shieldhit.parser.DummmyParser()
    if parser_type.lower() == 'shieldhit':
        return shieldhit.parser.ShieldhitParser()
    if parser_type.lower() == 'topas':
        return topas.parser.DummyParser()

    print(f"Invalid parser type \"{parser_type}\".")
    raise ValueError("Parser type must be either 'dummy', 'shieldhit' or 'topas'")


def run_parser(parser: Parser, input_data: dict, output_dir: str) -> None:
    """Convert the configs and save them in the output_dir directory."""
    parser.parse_configs(input_data)
    parser.save_configs(output_dir)
