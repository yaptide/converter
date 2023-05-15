from pathlib import Path
from converter.api import run_parser


def test_generated_beam_dat(project_shieldhit_json, sh12a_parser, tmpdir) -> None:
    """Check if beam.dat file created properly"""
    output_dir = Path(tmpdir)
    run_parser(sh12a_parser, project_shieldhit_json, output_dir)
    with open(output_dir / 'beam.dat') as f:
        input_text = f.read()
        assert input_text
        assert "STRAGG          2" in input_text
        assert "MSCAT           2" in input_text
        assert "NUCRE           1" in input_text