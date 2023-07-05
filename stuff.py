#!/usr/bin/env python3

import pytest

class Base:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @classmethod
    @property
    def available_schedulers(self):
        raise NotImplementedError('`available_schedulers` must be explicitly implemented in subclasses')

    def _configure(self, scheduler: str = None):
        if scheduler in self.available_schedulers or scheduler is None:
            print(f'Configuring {scheduler=}')
        else:
            raise ValueError(f'scheduler {scheduler} not in {self.available_schedulers}')

    def _compute(self, scheduler: str):
        print(f'Computing with {scheduler}')
        if not self.__class__.__name__[0].isupper():
            raise ValueError('Class name should be capital')

    def run(self, scheduler: str = None):
        self._configure(scheduler)
        self._compute(scheduler)

class Good(Base):
    available_schedulers = ['multiprocessing']

class Better(Base):
    available_schedulers = ['dask']

class Best(Base):
    available_schedulers = ['multiprocessing', 'dask']

class failing(Base):
    available_schedulers = ['multiprocessing', 'dask']


@pytest.fixture
def all_possible_schedulers():
    return ['multiprocessing', 'dask', 'slurm', None]

