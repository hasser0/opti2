import numpy as np
import pytest
from assignment import hungarian_method
from transhipment import transhipment_simplex
@pytest.mark.test_assignment_transhipment
def test_assignment_transhipment():
    t = []
    h = []
    c = []
    for i in range(50):
        size = np.random.randint(low=3, high=6, size=1)[0]
        cost = np.random.randint(0, 50, size = size*size).reshape(size, size)
        c.append(cost)
        supply = np.ones(size)
        demand = np.ones(size)
        t.append(transhipment_simplex(cost, supply, demand))
        h.append(hungarian_method(cost))
    print([True if np.all(tran-hun<=0) else False for hun,tran in zip(h,t)])

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