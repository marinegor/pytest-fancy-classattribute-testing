import pytest
import functools
from stuff import *
import importlib


def is_installed(modulename):
    """Check if modulename is present"""
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
            (s, nproc),
            marks=pytest.mark.skipif(
                not is_installed(s), reason=f"{s} is not installed"
            ),
        )
        for s in possible_schedulers
        for nproc in range(2)
    ]


def ensure_test_of_available_schedulers_for(cls):
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            scheduler_dict = kwargs.pop("scheduler")
            scheduler = scheduler_dict.get("scheduler")
            func(*args, **kwargs, scheduler=scheduler)

        return wrapper

    tested_schedulers = get_tested_schedulers_for(cls)
    actual_decorator = pytest.mark.parametrize("scheduler", tested_schedulers)

    return actual_decorator


# ------------------------------------------------


@pytest.fixture(params=[[1, 2, 3], ["a", True, None]])
def someargs(request):
    return request.param


@pytest.fixture(params=[{"1": 2, "3": 4}, {"a": 2}])
def somekwargs(request):
    return request.param


@ensure_test_of_available_schedulers_for(Good)
def test_Good(someargs, somekwargs, scheduler):
    obj = Good(args=someargs, kwargs=somekwargs)
    obj.run(scheduler=scheduler)


@ensure_test_of_available_schedulers_for(Better)
def test_Better(someargs, somekwargs, scheduler):
    obj = Better(args=someargs, kwargs=somekwargs)
    obj.run(scheduler=scheduler)


@ensure_test_of_available_schedulers_for(Best)
def test_Best(someargs, somekwargs, scheduler):
    obj = Best(args=someargs, kwargs=somekwargs)
    obj.run(scheduler=scheduler)


@ensure_test_of_available_schedulers_for(failing)
def test_failing(someargs, somekwargs, scheduler):
    with pytest.raises(ValueError):
        obj = failing(args=someargs, kwargs=somekwargs)
        obj.run(scheduler=scheduler)
