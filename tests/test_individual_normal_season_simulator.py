""" Unit test IndividualNormalSeasonSimulator """
from copy import deepcopy
import pytest
import pandas as pd
import numpy as np
from ffl_predictor import IndividualNormalSeasonSimulator
from ffl_predictor import Season
from helpers import assert_frames_equal

@pytest.fixture()
def sample_season():
    scores = (pd.DataFrame(np.array([
            ('team1', 1, 1.0), ('team1', 2, 1.0),
            ('team2', 1, 0.0), ('team2', 2, 10.0),
            ('team3', 1, 1.0), ('team3', 2, 2.0),
            ('team4', 1, 3.0), ('team4', 2, 4.0)],
        dtype=[('team', np.str, 8), ('week', np.int), ('score', np.float)]))
        .set_index(['team', 'week']))

    schedule = pd.DataFrame(np.array([
            ('team1', 'team2', 1),
            ('team3', 'team4', 1),
            ('team1', 'team3', 2),
            ('team2', 'team4', 2),
            ('team1', 'team4', 3),
            ('team2', 'team3', 3),
            ('team1', 'team3', 4),
            ('team2', 'team4', 4)],
        dtype=[('t1', np.str, 8), ('t2', np.str, 8), ('week', np.int)]))
    return Season(schedule, scores)

def test_simulate(sample_season):
    expected_scores = (pd.DataFrame(np.array([
            ('team1', 1, 1.0), ('team1', 2, 1.0), ('team1', 3, 1.0), ('team1', 4, 1.0),
            ('team2', 1, 0.0), ('team2', 2, 10.0), ('team2', 3, 1.265262), ('team2', 4, -2.587034),
            ('team3', 1, 1.0), ('team3', 2, 2.0), ('team3', 3, 2.111936), ('team3', 4, -0.127434),
            ('team4', 1, 3.0), ('team4', 2, 4.0), ('team4', 3, 4.733768), ('team4', 4, 2.961745)],
        dtype=[('team', np.str, 8), ('week', np.int), ('score', np.float)]))
        .set_index(['team', 'week']))
    np.random.seed(1)
    actual = IndividualNormalSeasonSimulator(sample_season).simulate()
    assert_frames_equal(actual, expected_scores, use_close=True, atol=.0001)

def test_simulate_different_reuslts(sample_season):
    sample_season_snapshot = deepcopy(sample_season)
    assert not IndividualNormalSeasonSimulator(sample_season).simulate().equals(
            IndividualNormalSeasonSimulator(sample_season).simulate())
    assert sample_season.scores.equals(sample_season_snapshot.scores)
