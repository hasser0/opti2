import pytest
from BFS_methods import northwest_corner, minium_cost, voguels
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
    assert np.allclose(northwest_corner(supply, demand), expected)


@pytest.mark.parametrize(
    "supply, demand, cost, expected",
    [
        (
            np.array([5, 10, 15]),
            np.array([12, 8, 4, 6]),
            np.array([
                [2, 3, 5, 6],
                [2, 1, 3, 5],
                [3, 8, 4, 6]
            ]),
            np.array([
                [5, 0, 0, 0],
                [2, 8, 0, 0],
                [5, 0, 4, 6]
            ])
        )
    ]
)
def test_minium_cost_method(supply, demand, cost, expected):
    assert np.allclose(minium_cost(supply, demand, cost), expected)

@pytest.mark.parametrize(
    "supply, demand, cost, expected",
    [
        (
            np.array([10,15]),
            np.array([15,5,5]),
            np.array([
                [6,7,8],
                [15,80,78]
            ]),
            np.array([
                [0,5,5],
                [15,0,0]
            ])
        )
    ]
)
def test_voguels(supply, demand, cost, expected):
    assert np.allclose(voguels(supply, demand, cost), expected)