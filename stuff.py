#!/usr/bin/env python3

from typing import Iterable, Callable

import datetime


class Scheduler(object):
    pass


class Results(list):
    pass


class Delayed:
    pass


class Base:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @classmethod
    @property
    def available_schedulers(self):
        return "local"

    def _configure(self, scheduler: str, n_workers: int) -> Scheduler:
        if scheduler in self.available_schedulers:
            print(f"Configuring {scheduler=} with {n_workers=}")
            return f"{scheduler}:{n_workers}"
        else:
            raise ValueError(
                f"scheduler {scheduler} not in {self.available_schedulers}"
            )

    def _setup_frames(self, start: int, stop: int, step: int) -> int:
        """Determines amount of frames in Results object"""
        return len(range(start, stop, step))

    def _prepare(self, result_size: int) -> Results:
        """Prepares empty results object"""
        return Results([0 for _ in range(result_size)])

    def _single_frame(self, location: int, results_container: Results) -> None:
        """Performs computations on a single frame"""
        results_container[location] = datetime.datetime.now()

    def _conclude(self) -> int:
        self.results = (max(self.results) - min(self.results)).toordinal()

    def _build_computations(
        self,
        n_workers: int,
        empty_results: Results,
    ) -> list[Delayed]:
        ...

    def _compute(self, computations: list, scheduler: Scheduler) -> list["Base"]:
        if scheduler != "local":
            __import__(scheduler)

        print(f"Computing with {scheduler=}")
        results = computations.compute(scheduler)  # FIXME
        return results

    def _parallel_conclude(self, worker_objects: list["Base"]) -> set:
        rv = {}
        for obj in worker_objects:
            rv.update(obj.results)
        return rv

    def run(
        self,
        scheduler: str = None,
        n_workers: int = None,
        start: int = None,
        stop: int = None,
        step: int = None,
    ):
        scheduler = scheduler if scheduler is not None else "local"
        n_workers = n_workers if n_workers is not None else 1

        configured_scheduler: Scheduler = self._configure(
            scheduler=scheduler, n_workers=n_workers
        )

        result_size: int = self._setup_frames(start=start, stop=stop, step=step)
        empty_results: Results = self._prepare(result_size=result_size)

        computations: list[Delayed] = self._build_computations(
            n_workers=n_workers, empty_results=empty_results
        )
        remote_results = self._compute(
            computations=computations, scheduler=configured_scheduler
        )
        flat_results = self._parallel_conclude(remote_results)
        conclusion = self._conclude(flat_results)

        return conclusion


class Good(Base):
    available_schedulers = ("local", "multiprocessing")


class Better(Base):
    available_schedulers = ("local", "dask")


class Best(Base):
    available_schedulers = ("local", "multiprocessing", "dask")


class failing(Base):
    available_schedulers = ("local", "multiprocessing", "dask")
