import pytest
import functools
from stuff import *
import importlib


def is_installed(modulename):
    """Check if modulename is present"""
    if modulename == "local":
        return True
    try:
        importlib.import_module(modulename)
        return True
    except ImportError:
        return False


def get_tested_schedulers_for(cls):
    """Obtain list of tested schedulers for particular class"""
    possible_schedulers = cls.available_schedulers

    return [
        pytest.param(
            {"scheduler": s, "n_workers": nproc},
            marks=pytest.mark.skipif(
                not is_installed(s), reason=f"{s} is not installed"
            ),
        )
        for s in possible_schedulers
        for nproc in range(1, 3)
    ]


def ensure_test_of_available_schedulers_for(cls):
    tested_schedulers = get_tested_schedulers_for(cls)
    return pytest.mark.parametrize("scheduler_params", tested_schedulers)


# ------------------------------------------------


@pytest.fixture(params=[[1, 2, 3], ["a", True, None]])
def someargs(request):
    return request.param


@pytest.fixture(params=[{"1": 2, "3": 4}, {"a": 2}])
def somekwargs(request):
    return request.param


@ensure_test_of_available_schedulers_for(Good)
def test_Good(someargs, somekwargs, scheduler_params):
    obj = Good(args=someargs, kwargs=somekwargs)
    obj.run(**scheduler_params)


@ensure_test_of_available_schedulers_for(Better)
def test_Better(someargs, somekwargs, scheduler_params):
    obj = Better(args=someargs, kwargs=somekwargs)
    obj.run(**scheduler_params)


@ensure_test_of_available_schedulers_for(Best)
def test_Best(someargs, somekwargs, scheduler_params):
    obj = Best(args=someargs, kwargs=somekwargs)
    obj.run(**scheduler_params)


@ensure_test_of_available_schedulers_for(failing)
def test_failing(someargs, somekwargs, scheduler_params):
    with pytest.raises(ValueError):
        obj = failing(args=someargs, kwargs=somekwargs)
        obj.run(**scheduler_params)
