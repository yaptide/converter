from pathlib import Path
from math import log10, ceil, isclose


class Parser:
    """Abstract parser, the template for implementing other parsers."""

    def __init__(self) -> None:
        self.info = {
            "version": "",
            "label": "",
            "simulator": "",
        }

    def parse_configs(self, json: dict) -> None:
        """Convert the json dict to the 4 config dataclasses."""
        raise NotImplementedError

    def save_configs(self, target_dir: str):
        """
        Save the configs as text files in the target_dir.
        The files are: beam.dat, mat.dat, detect.dat and geo.dat.
        """
        if not Path(target_dir).exists():
            raise ValueError("Target directory does not exist.")

        for file_name, content in self.get_configs_json().items():
            with open(Path(target_dir, file_name), 'w') as conf_f:
                conf_f.write(content)

    def get_configs_json(self) -> dict:
        """
        Return a dict representation of the config files. Each element has
        the config files name as key and its content as value.
        """
        configs_json = {
            "info.json": str(self.info),
        }
        return configs_json


def format_float(number: float, n: int) -> float:
    """
    Format float to be up to n characters wide, as precise as possible and as short
    as possible (in descending priority). so for example given 12.333 for n=5 you will
    get 12.33, n=7 will be 12.333
    """
    result = number
    # If number is zero we just want to get 0.0 (it would mess up the log10 operation below)
    if isclose(result, 0., rel_tol=1e-9):
        return 0.

    length = n

    # Adjust length for decimal separator ('.')
    length -= 1

    # Sign messes up the log10 we use do determine how long the number is. We use
    # abs() to fix that, but we need to remember the sign and update `n` accordingly
    sign = 1

    if result < 0:
        result = abs(result)
        sign = -1
        # Adjust length for the sign
        length -= 1

    whole_length = ceil(log10(result))

    # Check if it will be possible to fit the number
    if whole_length > length - 1:
        raise ValueError(f"Number is to big to be formatted. Minimum length: {whole_length-sign+1},\
requested length: {n}")

    # Adjust n for the whole numbers, log returns reasonable outputs for values greater
    # than 1, for other values it returns nonpositive numbers, but we would like 1
    # to be returned. We solve that by taking the greater value between the returned and
    # and 1.
    length -= max(whole_length, 1)

    result = float(sign * round(result, length))

    # Check if the round function truncated the number, warn the user if it did.
    if not isclose(result, number):
        print(f'WARN: number was truncated when converting: {number} -> {result}')

    # Formatting negative numbers smaller than the desired precision could result in -0.0 or 0.0 randomly.
    # To avoid this we catch -0.0 and return 0.0.
    if isclose(result, 0., rel_tol=1e-9):
        return 0.

    return result