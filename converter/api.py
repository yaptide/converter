from shieldhit.parser import Parser, DummmyParser, ShieldhitParser


def get_parser_from_str(parser_type: str):
    """Get a converter object based on the provided type."""
    # This is temporary, suggestions on how to do this better appreciated.
    if parser_type.lower() == 'dummy':
        return DummmyParser()
    elif parser_type.lower() == 'shieldhit':
        return ShieldhitParser()
    else:
        print(f"Invalid parser type \"{parser_type}\".")
        raise


def run_parser(parser: Parser, input_data: dict, output_dir: str) -> None:
    """Convert the configs and save them in the output_dir directory."""

    parser.parse_configs(input_data)
    parser.save_configs(output_dir)
