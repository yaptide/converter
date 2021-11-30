from converter.shieldhit.parser import DummmyParser as SHDummyParser, ShieldhitParser
from converter.topas.parser import DummmyParser as TopasDummyParser
from converter.common import Parser


def get_parser_from_str(parser_type: str) -> Parser:
    """Get a converter object based on the provided type."""
    # This is temporary, suggestions on how to do this better appreciated.
    if parser_type.lower() == 'sh_dummy':
        return SHDummyParser()
    if parser_type.lower() == 'shieldhit':
        return ShieldhitParser()
    if parser_type.lower() == 'topas':
        return TopasDummyParser()

    print(f"Invalid parser type \"{parser_type}\".")
    raise ValueError("Parser type must be either 'dummy', 'shieldhit' or 'topas'")


def run_parser(parser: Parser, input_data: dict, output_dir: str) -> None:
    """Convert the configs and save them in the output_dir directory."""
    parser.parse_configs(input_data)
    parser.save_configs(output_dir)
