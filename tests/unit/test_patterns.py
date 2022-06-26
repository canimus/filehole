from filehole import filehole
import glob

def test_scenario_a():
    df = filehole(glob, "./tests/fixtures/positive/scenario_a/*.csv")
    assert df.shape[0] == 10, "Didn't find all files in scenario a"

def test_scenario_a_negative():
    df = filehole(glob, "./tests/fixtures/negative/scenario_a/*.csv")
    assert df.query("~found").shape[0] == 1, "Didn't find all non-matches in scenario a"