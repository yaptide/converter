# Tests layout

## General tests

The general tests cover aspects of the converter common to all simulators.
Currently only the Figures part of geometry is tested here.
There is also `conftests.py` which contains fixture with location and content of a reference JSON project file.
As for now this file is based on the SHIELD-HIT12A simualator, but could be used as well for Fluka and Topas tests.

### Reference files

The reference JSON file is located in `tests/shieldhit/resources/project.json` together with the expected output files.

## Simulator specific tests

The simulator specific tests cover aspects of the converter specific to a given simulator. They are located in the `shieldhit`, `fluka` and `topas` directories.
