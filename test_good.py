import pytest
import functools

def make_scheduler_decorator(cls):
    def actual_decorator(func):
        possible_schedulers = cls.available_schedulers

        @functools.wraps(func)
        def wrapper(all_possible_schedulers, *args, **kwargs):
            scheduler = all_possible_schedulers.get('scheduler')
            n_workers = all_possible_schedulers.get('n_workers')
            if scheduler in possible_schedulers:
                func(*args, **kwargs, **all_possible_schedulers)
        return wrapper

    return actual_decorator

#------------------------------------------------

do_scheduler_testing = make_scheduler_decorator(Base)

@pytest.parametrize('rv', list(range(3)))
@pytest.fixture
def someargs(rv):
    return rv

@pytest.parametrize('rv', {str(i):i for i in range(3)})
@pytest.fixture
def someargs(rv):
    return rv

@do_scheduler_testing
def test_some_things(someargs, somekwargs):
    obj = Base(args=someargs, kwargs=somekwargs)
    obj.run()


@pytest.mark.parametrize("args", list(range(3)))
@pytest.mark.parametrize("kwargs", dict(enumerate(range(3))))
def test_Good(args, kwargs, possible_schedulers):
    obj = Good(args=args, kwargs=kwargs)

    for scheduler in possible_schedulers:
        if scheduler is None or method in Good.available_methods:
            obj.run(scheduler=scheduler)
        else:
            with pytest.raises(ValueError):
                obj.run(scheduler=scheduler)
