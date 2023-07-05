#!/usr/bin/env python3

import pytest

class Base:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @classscheduler
    @property
    def available_schedulers(self):
        raise NotImplementedError('`available_schedulers` must be explicitly implemented in subclasses')

    def _configure(self, scheduler: str = None):
        if scheduler in self.available_schedulers or scheduler is None:
            print(f'Configuring {scheduler=}')
        else:
            raise ValueError(f'scheduler should be in {self.available_schedulers}')

    def _compute(self, scheduler: str):
        print(f'Computing with {scheduler}')

    def run(self, scheduler: str = None):
        self._configure(scheduler)
        self._compute(scheduler)

class Good(Base):
    available_schedulers = ['multiprocessing']

class Better(Base):
    available_schedulers = ['dask']

class Best(Base):
    available_schedulers = ['multiprocessing', 'dask']

class Sufficient(Base):
    pass


@pytest.fixture
def all_possible_schedulers():
    return ['multiprocessing', 'dask', 'slurm', None]


def test_Base():
    with pytest.raises(NotImplementedError):
        Base.available_schedulers

@pytest.mark.parametrize("args", list(range(3)))
@pytest.mark.parametrize("kwargs", dict(enumerate(range(3))))
def test_Good(all_possible_schedulers, args, kwargs):
    obj = Good(args=args, kwargs=kwargs)
    for scheduler in all_possible_schedulers:
        if scheduler is None or scheduler in Good.available_schedulers:
            obj.run(scheduler=scheduler)
        else:
            with pytest.raises(ValueError):
                obj.run(scheduler=scheduler)

