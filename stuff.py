#!/usr/bin/env python3


class Base:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @classmethod
    @property
    def available_schedulers(self):
        return "local"

    def _configure(self, scheduler: str, n_workers: int):
        if scheduler in self.available_schedulers:
            print(f"Configuring {scheduler=} with {n_workers=}")
            return {"scheduler": scheduler, "n_workers": n_workers}
        else:
            raise ValueError(
                f"scheduler {scheduler} not in {self.available_schedulers}"
            )

    def _compute(self, scheduler: str, n_workers: int):
        if scheduler != "local":
            __import__(scheduler)

        if not self.__class__.__name__[0].isupper():
            raise ValueError("Class name should be capital")
        if n_workers < 1:
            raise ValueError("Should have >0 workers")

        print(f"Computing with {scheduler=} and {n_workers=}")
        for _ in range(int(1e7)):
            pass
        return 42

    def run(self, scheduler: str = None, n_workers: int = None):
        scheduler = scheduler if scheduler is not None else "local"
        n_workers = n_workers if n_workers is not None else 1

        scheduler_dict = self._configure(scheduler=scheduler, n_workers=n_workers)
        results = self._compute(**scheduler_dict)
        return results


class Good(Base):
    available_schedulers = ("local", "multiprocessing")


class Better(Base):
    available_schedulers = ("local", "dask")


class Best(Base):
    available_schedulers = ("local", "multiprocessing", "dask")


class failing(Base):
    available_schedulers = ("local", "multiprocessing", "dask")
