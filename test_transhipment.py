import pytest
from transhipment import transhipment_simplex
import numpy as np
M = 4000
@pytest.mark.parametrize(
    "cost, supply, demand, expected",
    [
        (
            np.array([
                [8,6,10,9],
                [9,12,13,7],
                [14,9,16,5]
            ]),
            np.array([35,50,40]),
            np.array([45,20,30,30]),
            np.array([
                [0,10,25,0],
                [45,0,5,0],
                [0,10,0,30]
            ])
        ),
        (
            np.array([2,6,6,2,1,2,5,7]).reshape(2,4),
            np.array([5000,3000]),
            np.array([1400,3200,2000,1400]),
            np.array([1400,200,2000,1400,0,3000,0,0]).reshape(2,4)
        ),
        (
            np.array([
                [4,7,M,M,M,M,0],
                [8,5,M,M,M,M,0],
                [5,6,M,M,M,7,0],
                [0,2,6,4,8,4,0],
                [2,0,3,6,7,7,0]
            ]),
            np.array([450,600,380,1430,1430]),
            np.array([1430,1430,300,300,300,400,130]),
            np.array([
                [320,0,0,0,0,0,130],
                [0,600,0,0,0,0,0],
                [0,0,0,0,0,380,0],
                [1110,0,0,300,0,20,0],
                [0,830,300,0,300,0,0]
            ])
        )
    ]
)
def test_transhipment(cost, supply, demand, expected):
    print(expected)
    print(transhipment_simplex(cost, supply, demand))
    assert np.allclose(transhipment_simplex(cost, supply, demand), expected)