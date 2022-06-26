from filehole import filehole
import glob

def test_scenario_a():
    df = filehole("./tests/fixtures/positive/scenario_a/*.csv", schedule_start="2022-01-01", schedule_end="2022-01-10")
    assert len(df) == 0, "Should have encounter all files"

def test_scenario_a_negative():
    df = filehole("./tests/fixtures/negative/scenario_a/*.csv", schedule_start="2022-01-01", schedule_end="2022-01-10")
    assert len(df) == 1, "Should have found a missing file item"