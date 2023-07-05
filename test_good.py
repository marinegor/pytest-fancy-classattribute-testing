import pytest
import functools
from stuff import *
import traceback

def ensure_test_of_available_schedulers_for(cls):
    def actual_decorator(func):
        possible_schedulers = cls.available_schedulers

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            scheduler_dict = kwargs.pop('scheduler')
            scheduler = scheduler_dict.get('scheduler')
            if scheduler in possible_schedulers or scheduler is None:
                func(*args, **kwargs, scheduler=scheduler)
            else: # scheduler not in possible_schedulers
                try:
                    func(*args, **kwargs, scheduler=scheduler)
                except ValueError as e:
                    last_method_name =  traceback.extract_tb(e.__traceback__)[-1].name
                    if last_method_name != '_configure':
                        raise e
                    else:
                        pass
        return wrapper

    return actual_decorator

#------------------------------------------------


@pytest.fixture(params=[[1,2,3], ['a', True, None]])
def someargs(request):
    return request.param

@pytest.fixture(params=[{'1':2, '3':4}, {'a':2}])
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
    obj = failing(args=someargs, kwargs=somekwargs)
    obj.run(scheduler=scheduler)

