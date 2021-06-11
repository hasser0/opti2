import numpy as np
import pytest
from assignment import hungarian_method

@pytest.mark.parametrize(
    "cost, expected",
    [
        (
            np.array([
                [47, 50, 57, 57, 0],
                [48, 52, 52, 62, 0],
                [50, 55, 54, 59, 0],
                [52, 54, 55, 60, 0],
                [51, 51, 53, 58, 0]
            ]),
            np.array([
                [1,0,0,0,0],
                [0,0,1,0,0],
                [0,0,0,1,0],
                [0,0,0,0,1],
                [0,1,0,0,0]
            ])
        )
    ]
)
def test_hungarian_method(cost, expected):
    result = hungarian_method(cost)
    assert np.all((expected-result)<=0)
