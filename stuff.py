#!/usr/bin/env python3


class Base:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @classmethod
    @property
    def available_schedulers(self):
        return "local"

    def _configure(self, scheduler: str = None):
        scheduler = scheduler if scheduler is not None else 'local'
        if scheduler in self.available_schedulers:
            print(f"Configuring {scheduler=}")
        else:
            raise ValueError(
                f"scheduler {scheduler} not in {self.available_schedulers}"
            )

    def _compute(self, scheduler: str):
        if scheduler != 'local':
            __import__(scheduler)
        print(f"Computing with {scheduler}")
        if not self.__class__.__name__[0].isupper():
            raise ValueError("Class name should be capital")

    def run(self, scheduler: str = None):
        self._configure(scheduler)
        self._compute(scheduler)


class Good(Base):
    available_schedulers = ("local", "multiprocessing")


class Better(Base):
    available_schedulers = ("local", "dask")


class Best(Base):
    available_schedulers = ("local", "multiprocessing", "dask")


class failing(Base):
    available_schedulers = ("local", "multiprocessing", "dask")
