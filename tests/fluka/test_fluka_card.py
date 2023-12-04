from converter.fluka.cards.card import Card


def test_beam_line() -> None:
    """Test if BEAM line is formatted properly."""
    assert str(Card("BEAM", ["-0.15"], "PROTON")) == "BEAM           -0.15                                                  PROTON"
    assert str(Card("BEAM", ["200.0", "0.2", "1.5", "1.2", "0.7", "1.0"], "PROTON")) == "BEAM           200.0       0.2       1.5       1.2       0.7       1.0PROTON"
    assert str(Card("BEAM", ["10.0", "0.2", "0.0", "-2.36", "-1.18", "1.0"], "PROTON")) == "BEAM            10.0       0.2       0.0     -2.36     -1.18       1.0PROTON"
    assert str(Card("BEAM", ["-661.7E-06", "0.0", "1.0E4", "0.0", "0.0", "1.0"], "PHOTON")) == "BEAM      -0.0006617       0.0   10000.0       0.0       0.0       1.0PHOTON"
    assert str(Card("BEAM", ["-2.0", "0.0", "3.0", "0.0", "0.0", "1.0"], "MUON-")) == "BEAM            -2.0       0.0       3.0       0.0       0.0       1.0MUON-"
    assert str(Card("BEAM", ["120000000000000.0", "3.02", "-30.4234"], "PROTON")) == "BEAM       1.200E+14      3.02  -30.4234                              PROTON"


def test_start_line() -> None:
    """Test if START line is formatted properly."""
    assert str(Card("START", ["10000"])) == "START        10000.0"
    assert str(Card("START", ["5000"])) == "START         5000.0"
    assert str(Card("START", ["200000"])) == "START       200000.0"
    assert str(Card("START", ["1234567"])) == "START      1234567.0"


def test_usrbin_card() -> None:
    """Test if USRBIN card is formatted properly"""
    assert str(Card("USRBIN", ["10.0", "DOSE", "-21.0", "7.0", "7.0", "12.1"], "verythin")) == "USRBIN          10.0      DOSE     -21.0       7.0       7.0      12.1verythin"
    assert str(Card("USRBIN", ["-7.0", "-7.0", "12.0", "35.0", "35.0", "1.0"], "&")) == "USRBIN          -7.0      -7.0      12.0      35.0      35.0       1.0&"
