import pytest
from BFS_methods import northwest_corner
import numpy as np

@pytest.mark.parametrize(
    "supply, demand, expected",
    [
        (
            np.array([5, 1, 3]),
            np.array([2, 4, 2, 1]),
            np.array([
                [2,3,0,0],
                [0,1,0,0],
                [0,0,2,1],
            ])
        ),
        (
            np.array([100, 200, 300]),
            np.array([150, 100, 275, 75]),
            np.array([
                [100,0,0,0],
                [50,100,50,0],
                [0,0,225,75]
            ])
        ),
        (
            np.array([300,400,500]),
            np.array([250,350,400,200]),
            np.array([
                [250,50,0,0],
                [0,300,100,0],
                [0,0,300,200]
            ])
        )
    ]
)
def test_northwest_method(supply, demand, expected):
    assert np.all(np.isclose(northwest_corner(supply,demand), expected))